import sys
import os
import threading
import subprocess
import time

from optparse import OptionParser

server_process = None
pid = None


class Checker(threading.Thread):

    def __init__(self, delta):
        threading.Thread.__init__(self)
        self.delta = delta
        self.die = False

    def run(self):
        while not self.die:
            self._check()
            time.sleep(self.delta)
        server_process.terminate()

    def _check(self):
        try:
            global pid
            os.kill(int(pid), 0)
        except OSError:
            self.die = True

if __name__ == '__main__':
    opt_parser = OptionParser(usage=(
        'usage: %prog <sublime_pid> <port> <solution_file> '
    ))

    options, args = opt_parser.parse_args()
    if len(args) != 3:
        opt_parser.error('please pass all arguments')

    pid = args[0]
    port = args[1]
    solution_file = args[2]

    if os.name == 'nt':
        mono_dir_candidate_paths = os.environ['PATH'].split(';')
        mono_dir_candidate_paths += [
           'C:/Program Files (x86)/Mono-3.2.3/bin'
        ]
        mono_exe_candidate_paths = [os.path.join(mono_dir_path, 'mono.exe')
                for mono_dir_path in mono_dir_candidate_paths]
        mono_exe_paths = [mono_exe_candidate_path 
                for mono_exe_candidate_path in mono_exe_candidate_paths 
                if os.access(mono_exe_candidate_path, os.R_OK)]
    else:
        mono_dir_candidate_paths = os.environ['PATH'].split(':')
        mono_dir_candidate_paths += [
            '/usr/local/bin',
            '/opt/usr/local/bin',
            '/opt/usr/bin',
        ]
        mono_exe_candidate_paths = [os.path.join(mono_dir_path, 'mono') 
                for mono_dir_path in mono_dir_candidate_paths]
        mono_exe_paths = [mono_exe_candidate_path 
                for mono_exe_candidate_path in mono_exe_candidate_paths 
                if os.access(mono_exe_candidate_path, os.R_OK)]


    if not mono_exe_paths:
        sys.stderr.write('Check your mono executable path.\n')
        sys.stderr.write(repr(os.environ))
        sys.exit(-1)

    mono_exe_path = mono_exe_paths[0]

    if os.name == 'nt':
        server_file_path = __file__.replace('\\', '/')
    else:
        server_file_path = __file__

    server_dir_path = os.path.dirname(server_file_path)
    plugin_dir_path = os.path.dirname(server_dir_path) 
    
    omnisharp_server_path = os.path.join(
        plugin_dir_path,
        'OmniSharpServer/OmniSharp/bin/Debug/OmniSharp.exe')

    args = [
        mono_exe_path, 
        omnisharp_server_path, 
        '-p', port,
        '-s', solution_file
    ]

    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    else:
        startupinfo = None
    
    try:
        server_process = subprocess.Popen(args, startupinfo=startupinfo)
    except Exception as e:
        sys.stderr.write(
                'Check your solution file, OmniSharpServer'
                ' and mono environment.\n')
        sys.stderr.write(repr(e) + '\n')

        sys.exit(-1)

    checker = Checker(5)
    checker.start()

    server_process.wait()
