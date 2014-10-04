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

from .helpers import get_settings
from .helpers import current_solution_or_folder
from .helpers import current_project_folder


server_subprocesses = {
}
server_ports = {
}


class ThreadUrl(threading.Thread):

    def __init__(self, url, callback, data, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.timeout = timeout
        self.callback = callback

    def run(self):
        try:
            response = urllib.request.urlopen(
                self.url, self.data, self.timeout)
            self.callback(response.read())
        except:
            traceback.print_exc(file=sys.stdout)
            self.callback(None)


def urlopen_async(url, callback, data, timeout):
    thread = ThreadUrl(url, callback, data, timeout)
    thread.start()


def get_response(view, endpoint, callback, params=None, timeout=None):
    solution_path =  current_solution_or_folder(view)

    print(solution_path)
    print(server_ports)
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


def _available_prot():
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

    mono_exe_candidate_paths = [os.path.join(mono_dir_path, mono_exe_name)
            for mono_dir_path in mono_dir_candidate_paths]

    mono_exe_paths = [mono_exe_candidate_path 
            for mono_exe_candidate_path in mono_exe_candidate_paths 
            if os.access(mono_exe_candidate_path, os.R_OK)]

    if os.name == 'nt':
        return [mono_exe_path.replace('\\', '/')
            for mono_exe_path in mono_exe_paths]
    else:
        return mono_exe_paths


def _find_omni_sharp_server_exe_path():
    if os.name == 'nt':
        source_file_path = __file__.replace('\\', '/')
    else:
        source_file_path = __file__

    source_dir_path = os.path.dirname(source_file_path)
    plugin_dir_path = os.path.dirname(source_dir_path) 
    
    return os.path.join(
        plugin_dir_path,
        'OmniSharpServer/OmniSharp/bin/Debug/OmniSharp.exe') 

def create_omnisharp_server_subprocess(view):
    solution_path = current_solution_or_folder(view)

    print("current_solution:%s" % solution_path)

    # no solution file
    #if solution_path is None or not os.path.isfile(solution_path):
        #return

    # server is running
    if solution_path in server_subprocesses:
        return

    mono_exe_paths = _find_mono_exe_paths()
    if len(mono_exe_paths) == 0:
        print('NOT_FOUND_MONO_EXE')
        print('Install MRE(Mono Runtime Environment) from <http://www.mono-project.com/download/>')
        return

    mono_exe_path = mono_exe_paths[0]
    print('mono:%s' % mono_exe_path)

    omni_exe_path = _find_omni_sharp_server_exe_path()
    if not os.access(omni_exe_path, os.R_OK):
        print('NOT_FOUND_OMNI_SHARP_SERVER_EXE')
        print('Browse Packages and run ./build.sh in OmniSharpSublime Directory')
        return

    print('omni:%s' % omni_exe_path)

    return

    omnisharp_server_path = os.path.join(
        os.path.dirname(__file__),
        '../server/server.py')

    print("omnisharp_server:%s" % omnisharp_server_path)

    port = _available_prot()

    # for windows
    if os.name == 'nt':
        solution_path = solution_path.replace('\\', '/')
        omnisharp_server_path = os.path.normpath(omnisharp_server_path).replace('\\', '/')        
        python_path = 'pythonw'
    else:
        python_path = 'python'


    args = [
        python_path, omnisharp_server_path, str(os.getpid()), str(port), solution_path
    ]

    print('open_solution_server:%s' % repr(args))
    server_process = subprocess.Popen(args, stderr=subprocess.PIPE)
    server_thread = threading.Thread(target=communicate_server, args=(server_process, solution_path))
    server_thread.daemon = True
    server_thread.start()

    server_subprocesses[solution_path] = server_process
    server_ports[solution_path] = port

def communicate_server(target_process, target_name):
    print('start_solution_server:%s' % (target_name))
    stdin_data, stderr_data = target_process.communicate()
    if stderr_data:
        for stderr_line in stderr_data.splitlines():
            print('exit_solution_server:%s error:%s' % (target_name, stderr_line))
    else:
        print('exit_solution_server:%s' % (target_name))

