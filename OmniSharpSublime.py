import sys
import sublime
import os

from .listeners import *
from .commands import *

if sys.version_info < (3, 3):
    raise RuntimeError('OmniSharpSublime works with Sublime Text 3 only')

def plugin_loaded():
    print('omnisharp plugin_loaded')
    settings = sublime.load_settings('OmniSharpSublime.sublime-settings')
    configpath = settings.get("omnisharp_server_config_location")
    if not configpath:
        settings.set("omnisharp_server_config_location", sublime.packages_path() + os.path.sep + "OmniSharp" + os.path.sep + "PrebuiltOmniSharpServer" + os.path.sep + "config.json")
        sublime.save_settings('OmniSharpSublime.sublime-settings')

    if os.name == 'posix':
        # give the launch script executable permissions
        os.chmod('PrebuiltOmniSharpServer/omnisharp', st.st_mode | 0o111)

    from package_control import events
    print('got events')
    print(events)
    if events.install('OmniSharp'):
        print('Installing OmniSharp')
        if os.name == 'posix':
            # give the launch script executable permissions
            os.chmod('PrebuiltOmniSharpServer/omnisharp', st.st_mode | 0o111)
    elif events.post_upgrade('OmniSharp'):
        print('Upgrading OmniSharp')
        if os.name == 'posix':
            # give the launch script executable permissions
            os.chmod('PrebuiltOmniSharpServer/omnisharp', st.st_mode | 0o111)


def plugin_unloaded():
    from package_control import events

    if events.pre_upgrade('OmniSharp'):
        print('About to upgrade OmniSharp')
        if os.name != 'posix':
            # kill the exe before the update complains about exe in use
            os.system('taskkill /f /im PrebuiltOmniSharpServer/OmniSharp.exe')

    print('omnisharp plugin_unloaded')
