# TODO: Omnisharp server가 sublime이 꺼지면 같이 꺼져야함.
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

def plugin_unloaded():
    print('omnisharp plugin_unloaded')
