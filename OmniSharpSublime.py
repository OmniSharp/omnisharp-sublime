import sys
import sublime
import os
import stat
from package_control import events

from .lib.helpers import get_plugin_path
from .lib.helpers import get_settings
from .lib.helpers import *
from .listeners import *
from .commands import *
from .lib.urllib3 import *
package_name = 'OmniSharp'

if sys.version_info < (3, 3):
    raise RuntimeError('OmniSharpSublime works with Sublime Text 3 only')


def plugin_loaded():
    print('omnisharp plugin_loaded')

    if os.name == 'posix':
        # give omnisharp.exe executable permissions
        settings = sublime.load_settings('OmniSharpSublime.sublime-settings')
        omni_exe_path = get_omni_path(active_view())
        st = os.stat(omni_exe_path)
        os.chmod(omni_exe_path, st.st_mode | 0o111)


def plugin_unloaded():
    if events.pre_upgrade('OmniSharp'):
        print('About to upgrade OmniSharp')
        if os.name != 'posix':
            # kill the exe before the update complains about exe in use
            os.system('taskkill /f /im ' + get_omni_path(active_view()))

    print('omnisharp plugin_unloaded')
