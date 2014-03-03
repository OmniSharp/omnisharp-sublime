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

    global pid
    pid = args[0]
    port = args[1]
    solution_file = args[2]

    omnisharp_server_path = os.path.join(
        os.path.dirname(__file__),
        '../OmniSharpServer/OmniSharp/bin/Debug/OmniSharp.exe')
    args = [
        'mono', omnisharp_server_path, '-p', port,
        '-s', solution_file
    ]

    global server_process
    try:
        server_process = subprocess.Popen(args)
    except:
        print('Check your solution file, OmniSharpServer'
              ' and mono environment.')
        sys.exit(1)

    checker = Checker(5)
    checker.start()

    server_process.wait()
