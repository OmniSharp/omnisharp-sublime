import os
import time
import errno
import ctypes
import subprocess
import threading

from argparse import ArgumentParser

IS_NT_CONSOLE_VISIBLE = False

# http://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid
def is_pid_alive(pid):
    if os.name == 'posix':
        if pid < 0:
            return False
        try:
            os.kill(pid, 0)
        except OSError as e:
            return e.errno == errno.EPERM
        else:
                return True
    else:
        kernel32 = ctypes.windll.kernel32
        SYNCHRONIZE = 0x100000

        process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
        if process != 0:
            kernel32.CloseHandle(process)
            return True
        else:
            return False

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


def start_omni_sharp_server(omni_exe_path, solution_path, port, config_file):
    if os.name == 'posix':
        source_file_path = os.path.realpath(__file__)
        source_dir_path = os.path.dirname(source_file_path)
        launch_sh = '/'.join((source_dir_path, 'launch.sh'))
        args = [
            launch_sh,
            omni_exe_path, 
            '-s', solution_path,
            '-p', str(port),
            '-config', config_file
        ]

        startupinfo = None
    else:
        args = [
            omni_exe_path, 
            '-s', solution_path,
            '-p', str(port),
            '-config', config_file
        ]

        if IS_NT_CONSOLE_VISIBLE:
            startupinfo = None
        else:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

    print(' '.join(args))
    return subprocess.Popen(args, startupinfo=startupinfo)

def run(omni_port, solution_path, config_file=None):
    omni_exe_paths = find_omni_exe_paths()
    if not omni_exe_paths:
        sys.stderr.write('NOT_FOUND_OMNI_EXE\n')
        return -1002

    omni_exe_path = omni_exe_paths[0]
            
    try: 
        omni_proc = start_omni_sharp_server(
            omni_exe_path,
            solution_path,
            omni_port,
            config_file)
    except Exception as e:
        print('NOT_STARTED_OMNI_SHARP_SERVER:%s' % repr(e)) 
        return -2001

    return omni_proc