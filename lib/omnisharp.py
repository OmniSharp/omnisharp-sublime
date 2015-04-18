import os
import sublime
import threading
import json
import urllib
import urllib.parse
import socket
import subprocess
import traceback
import sys
import signal

from .helpers import quote_path
from .helpers import get_settings
from .helpers import current_solution_filepath_or_project_rootpath
from .urllib3 import PoolManager

IS_EXTERNAL_SERVER_ENABLE = False

launcher_procs = {
}

server_ports = {
}

pool = PoolManager(headers={'Content-Type': 'application/json; charset=UTF-8'})

class WorkerThread(threading.Thread):
    def __init__(self, url, data, callback, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.callback = callback
        self.timeout = timeout

    def run(self):
        try:
            print('======== request ======== \n Url: %s \n Data: %s' % (self.url, self.data))

            response = pool.urlopen('POST', self.url, body=self.data, timeout=self.timeout).data
            
            if not response:
                print('======== response ======== \n response is empty')
                self.callback(None)
            else:
                decodeddata = response.decode('utf-8')
                print('======== response ======== \n %s' % decodeddata)
                self.callback(json.loads(decodeddata))
                
            print('======== end ========')
        except Exception as ex:
            if "checkalivestatus" not in self.url:
                print(str(ex))
                set_omnisharp_status("Error talking to " + self.url)
            else:
                set_omnisharp_status("Server Not Running")


def get_response(view, endpoint, callback, params=None, timeout=None):
    solution_path =  current_solution_filepath_or_project_rootpath(view)

    print('solution path: %s' % solution_path)
    if solution_path is None or solution_path not in server_ports:
        callback(None)
        return
        
    location = view.sel()[0]
    cursor = view.rowcol(location.begin())

    parameters = {}
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

    url = "http://%s:%s%s" % (host, port, endpoint)
    data = json.dumps(parameters)

    thread = WorkerThread(url, data, callback, timeout)  
    thread.start()

def _available_port():
    if IS_EXTERNAL_SERVER_ENABLE:
        return 2000

    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()

    return port

def create_omnisharp_server_subprocess(view):
    solution_path = current_solution_filepath_or_project_rootpath(view) 
    if solution_path in launcher_procs:
        print("already_bound_solution:%s" % solution_path)
        return

    print("solution_path:%s" % solution_path)

    omni_port = _available_port()
    print('omni_port:%s' % omni_port)
    
    
    config_file = get_settings(view, "omnisharp_server_config_location")

    if IS_EXTERNAL_SERVER_ENABLE:
        launcher_proc = None
        omni_port = 2000
    else:
        try:
            omni_exe_paths = find_omni_exe_paths()
            omni_exe_path = quote_path(omni_exe_paths[0])

            args = [
                omni_exe_path, 
                '-s', quote_path(solution_path),
                '-p', str(omni_port),
                '-config', quote_path(config_file),
                '--hostPID', str(os.getpid())
            ]

            cmd = ' '.join(args)
            print(cmd)
            
            view.window().run_command("exec",{"cmd":cmd,"shell":"true","quiet":"true"})
            view.window().run_command("hide_panel", {"panel": "output.exec"})

            set_omnisharp_status("Loading Project")
            sublime.set_timeout(lambda:check_solution_ready_status(view), 5000)

        except Exception as e:
            print('RAISE_OMNI_SHARP_LAUNCHER_EXCEPTION:%s' % repr(e))
            set_omnisharp_status("Error Launching Server")
            return

    launcher_procs[solution_path] = True
    server_ports[solution_path] = omni_port

def find_omni_exe_paths():
    if os.name == 'posix':
        source_file_path = os.path.realpath(__file__)
        script_name = 'omnisharp'
    else:
        source_file_path = os.path.realpath(__file__).replace('\\', '/')
        script_name = 'omnisharp.cmd'

    source_dir_path = os.path.dirname(source_file_path)
    plugin_dir_path = os.path.dirname(source_dir_path)
    print(plugin_dir_path)

    omni_exe_candidate_rel_paths = [
        'omnisharp-roslyn/artifacts/build/omnisharp/' + script_name,
        'PrebuiltOmniSharpServer/' + script_name,
    ]

    omni_exe_candidate_abs_paths = [
        '/'.join((plugin_dir_path, rel_path))
        for rel_path in omni_exe_candidate_rel_paths
    ]

    return [omni_exe_path 
        for omni_exe_path in omni_exe_candidate_abs_paths
        if os.access(omni_exe_path, os.R_OK)]

def set_omnisharp_status(statusmsg):
    sublime.active_window().active_view().set_status("OmniSharp", "OmniSharp : " + statusmsg)

def check_solution_ready_status(view):
    get_response(view, "/checkreadystatus", ready_status_handler)

readycount = 0

def ready_status_handler(data):
    print("ready is " + str(data))
    if data == False:
        readycount += 1
        if readycount < 5:
            sublime.set_timeout(lambda:check_solution_ready_status(sublime.active_window().active_view()), 5000)
        else:
            set_omnisharp_status("Error Loading Project")
            readycount = 0
    elif data == True:
        readycount = 0
        set_omnisharp_status("Project Loaded")
        sublime.set_timeout(lambda:check_server_alive_status(sublime.active_window().active_view()), 5000)

def check_server_alive_status(view):
    get_response(view, "/checkalivestatus", alive_status_handler)    

def alive_status_handler(data):
    if data == False:
        # I don't expect this to get hit because if its not running it wil throw exception
        set_omnisharp_status("Server Not Running")
    elif data == True:
        set_omnisharp_status("Server Running")
        sublime.set_timeout(lambda:check_server_alive_status(sublime.active_window().active_view()), 5000)
