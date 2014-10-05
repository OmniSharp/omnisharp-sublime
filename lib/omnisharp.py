import os
import sublime
import threading
import json
import urllib
import urllib.parse
import urllib.request
import socket
import subprocess
import queue
import traceback
import sys
import signal

from .helpers import get_settings
from .helpers import current_solution_or_folder
from .helpers import current_project_folder

from queue import Queue

IS_EXTERNAL_OMNI_SHARP_ENABLE = False
IS_OMNI_SHARP_NT_CONSOLE_VISIBLE = False

server_procs = {
}

server_ports = {
}

class WorkerThread(threading.Thread):
    _worker_threads = []
    _worker_queue = Queue()

    def run(self):
        while True:
            url, data, timeout, callback = self._worker_queue.get()
            try:
                response = urllib.request.urlopen(url, data, timeout)
                callback(response.read())
            except:
                traceback.print_exc(file=sys.stdout)
                callback(None)

    @classmethod
    def make_worker_threads(cls, count):
        while len(cls._worker_threads) < count:
            new_worker_thread = cls()
            new_worker_thread.start()
            cls._worker_threads.append(new_worker_thread)

    @classmethod
    def add_work(cls, url, data, timeout, callback):
        cls._worker_queue.put((url, data, timeout, callback))

WorkerThread.make_worker_threads(1)

def urlopen_async(url, callback, data, timeout):
    WorkerThread.add_work(url, data, timeout, callback)

def get_response(view, endpoint, callback, params=None, timeout=None):
    solution_path =  current_solution_or_folder(view)

    print('response:', solution_path)
    if solution_path is None or solution_path not in server_ports:
        callback(None)
        return
        
    parameters = {}
    location = view.sel()[0]
    cursor = view.rowcol(location.begin())

    parameters['line'] = str(cursor[0] + 1)
    parameters['column'] = str(cursor[1] + 1)
    parameters['buffer'] = view.substr(sublime.Region(0, view.size()))
    parameters['filename'] = view.file_name()

    if params is not None:
        parameters.update(params)
    if timeout is None:
        timeout = int(get_settings(view, 'omnisharp_response_timeout'))

    host = 'localhost'
    port = server_ports[solution_path]

    httpurl = "http://%s:%s/" % (host, port)

    target = urllib.parse.urljoin(httpurl, endpoint)
    data = urllib.parse.urlencode(parameters).encode('utf-8')
    print('request: %s' % target)
    print('======== request params ======== \n %s' % json.dumps(parameters))

    def urlopen_callback(data):
        print('======== response ========')
        if data is None:
            print(None)
            # traceback.print_stack(file=sys.stdout)
            print('CALLBACK_ERROR')
            callback(None)

            if solution_path in server_procs:
                print('TERMINATE_OMNI_SHARP')
                server_procs[solution_path].terminate();

                del server_procs[solution_path]
                del server_ports[solution_path]

        else:
            jsonStr = data.decode('utf-8')
            print(jsonStr)
            jsonObj = json.loads(jsonStr)
            # traceback.print_stack(file=sys.stdout)
            print('callback data')
            callback(jsonObj)

    urlopen_async(
        target,
        urlopen_callback,
        data,
        timeout)


def get_response_from_empty_httppost(view, endpoint, callback, timeout=None):
    solution_path =  current_solution_or_folder(view)

    print(solution_path)
    print(server_ports)
    if solution_path is None or solution_path not in server_ports:
        callback(None)
        return
    parameters = {}
    location = view.sel()[0]
    cursor = view.rowcol(location.begin())

    if timeout is None:
        timeout = int(get_settings(view, 'omnisharp_response_timeout'))

    host = 'localhost'
    port = server_ports[solution_path]

    httpurl = "http://%s:%s/" % (host, port)

    target = urllib.parse.urljoin(httpurl, endpoint)
    data = urllib.parse.urlencode(parameters).encode('utf-8')
    print('request: %s' % target)
    print('======== no request params ======== \n')

    def urlopen_callback(data):
        print('======== response ========')
        if data is None:
            print(None)
            # traceback.print_stack(file=sys.stdout)
            print('callback none')
            callback(None)
        else:
            jsonStr = data.decode('utf-8')
            print(jsonStr)
            jsonObj = json.loads(jsonStr)
            # traceback.print_stack(file=sys.stdout)
            print('callback data')
            callback(jsonObj)
    urlopen_async(
        target,
        urlopen_callback,
        data,
        timeout)


def _available_port():
    if IS_EXTERNAL_OMNI_SHARP_ENABLE:
        return 2000

    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()

    return port

def _find_mono_exe_paths():
    if os.name == 'nt':
        mono_dir_candidate_paths = os.environ['PATH'].split(';')
        mono_dir_candidate_paths += [
           'C:/Program Files (x86)/Mono-3.2.3/bin'
        ]
        mono_exe_name = "mono.exe"
    else:
        mono_dir_candidate_paths = os.environ['PATH'].split(':')
        mono_dir_candidate_paths += [
            '/usr/local/bin',
            '/opt/usr/local/bin',
            '/opt/usr/bin',
        ]
        mono_exe_name = "mono"

    mono_exe_candidate_paths = ['/'.join((mono_dir_path, mono_exe_name))
            for mono_dir_path in mono_dir_candidate_paths]

    mono_exe_paths = [mono_exe_candidate_path 
            for mono_exe_candidate_path in mono_exe_candidate_paths 
            if os.access(mono_exe_candidate_path, os.R_OK)]

    if os.name == 'nt':
        return [mono_exe_path.replace('\\', '/')
            for mono_exe_path in mono_exe_paths]
    else:
        return mono_exe_paths


def _find_omni_sharp_server_exe_paths():
    if os.name == 'nt':
        source_file_path = __file__.replace('\\', '/')
    else:
        source_file_path = __file__

    source_dir_path = os.path.dirname(source_file_path)
    plugin_dir_path = os.path.dirname(source_dir_path)

    omni_exe_candidate_rel_paths = [
        'OmniSharpServer/OmniSharp/bin/Debug/OmniSharp.exe',
        'OmniSharpServer/OmniSharp/bin/Release/OmniSharp.exe',
        'server/OmniSharp.exe',
    ]

    omni_exe_candidate_abs_paths = [
        '/'.join((plugin_dir_path, rel_path))
        for rel_path in omni_exe_candidate_rel_paths
    ]

    return [omni_exe_path 
        for omni_exe_path in omni_exe_candidate_abs_paths
        if os.access(omni_exe_path, os.R_OK)]


def _open_pid_file(solution_path, mode):
    solution_name = os.path.basename(solution_path)
    solution_dir_path = os.path.dirname(solution_path)
    pid_path = '/'.join((solution_dir_path, solution_name + ".pid"))
    return open(pid_path, mode)

def _start_omni_sharp_server(mono_exe_path, omni_exe_path, solution_path, port):
    try:
        old_pid = int(_open_pid_file(solution_path, "r").read())
        print('kill_old_omni_proc:', old_pid)
        os.kill(old_pid, signal.SIGTERM)
    except IOError:
        pass

    if os.name == 'nt':
        args = [
            omni_exe_path, 
            '-s', solution_path,
            '-p', str(port),
        ]

        if IS_OMNI_SHARP_NT_CONSOLE_VISIBLE:
            startupinfo = None
        else:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

    else:
        args = [
            mono_exe_path, 
            omni_exe_path, 
            '-s', solution_path,
            '-p', str(port),
        ]

        startupinfo = None
    
    new_proc = subprocess.Popen(args, startupinfo=startupinfo)

    try:
        server_thread = threading.Thread(
            target=_communicate_omni_sharp_server, 
            args=(new_proc, solution_path))

        server_thread.start()
   
        _open_pid_file(solution_path, "w").write(str(new_proc.pid))

    except Exception as e:
        new_proc.terminate()
        raise e

    return new_proc

def _communicate_omni_sharp_server(server_proc, solution_path):
    print('start_omni_sharp_communication:%s' % solution_path)
    stdin_data, stderr_data = server_proc.communicate()
    if not stderr_data:
        print('exit_omni_sharp_communication:%s' % solution_path)
        return

    for stderr_line in stderr_data.splitlines():
        print('stop_omni_sharp_communication:%s error:%s' % (target_name, stderr_line))


def create_omnisharp_server_subprocess(view):
    solution_path = current_solution_or_folder(view)

    # no solution file
    #if solution_path is None or not os.path.isfile(solution_path):
        #return

    # server is running
    if solution_path in server_procs:
        print("already_bound_solution:%s" % solution_path)
        return

    print("solution:%s" % solution_path)

    mono_exe_paths = _find_mono_exe_paths()
    if not mono_exe_paths:
        print('NOT_FOUND_MONO_EXE')
        print('Install MRE(Mono Runtime Environment) from <http://www.mono-project.com/download/>')
        return

    mono_exe_path = mono_exe_paths[0]
    print('mono_exe:%s' % mono_exe_path)

    omni_exe_paths = _find_omni_sharp_server_exe_paths()
    if not omni_exe_paths:
        print('NOT_FOUND_OMNI_EXE')
        print('Browse Packages and run ./build.sh in OmniSharpSublime directory or')
        print('Build the solution with xamarin(or visual studio)')
        return

    omni_exe_path = omni_exe_paths[0]
    print('omni_exe:%s' % omni_exe_path)

    omni_port = _available_port()
    print('omni_port:%s' % omni_port)

    if IS_EXTERNAL_OMNI_SHARP_ENABLE:
        omni_proc = None
        omni_port = 2000
    else:
        try:
            omni_proc = _start_omni_sharp_server(
                mono_exe_path,
                omni_exe_path,
                solution_path,
                omni_port)
        except Exception as e:
            print('RAISE_OMNISHARP_SERVER_EXCEPTION:%s' % repr(e))
            return

    server_procs[solution_path] = omni_proc
    server_ports[solution_path] = omni_port

