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

from .helpers import get_settings
from .helpers import current_solution

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
            self.callback(None)


def urlopen_async(url, callback, data, timeout):
    thread = ThreadUrl(url, callback, data, timeout)
    thread.start()


def get_response(view, endpoint, callback, params=None, timeout=None):
    solution_path = current_solution(view)
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

    def urlopen_callback(data):
        if data is None:
            callback(None)
        else:
            jsonStr = data.decode('utf-8')
            jsonObj = json.loads(jsonStr)
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


def create_omnisharp_server_subprocess(view):
    solution_path = current_solution(view)

    # no solution file
    if solution_path is None or not os.path.isfile(solution_path):
        return

    # server is running
    if solution_path in server_subprocesses:
        return

    omnisharp_server_path = os.path.join(
        os.path.dirname(__file__),
        '../server/server.py')

    port = _available_prot()
    args = [
        'python', omnisharp_server_path, str(os.getpid()), str(port), solution_path
    ]

    print('open_solution_server:%s' % (solution_path))
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

