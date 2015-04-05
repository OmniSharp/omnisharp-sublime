import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpBuildProject(sublime_plugin.TextCommand):
    
    def run(self, edit, buildtype='build'):
        print('building')
        options = {}
        options['build'] = self.build
        options['rebuild'] = self.rebuild
        options['clean'] = self.clean
        helpers.save_all_files(sublime.active_window())
        options[buildtype]()

    def build(self):
        self.getbuild('build')

    def rebuild(self):
        self.getbuild('rebuild')

    def clean(self):
        self.getbuild('clean')

    def getbuild(self, buildtype):
        params = {}
        params['type'] = buildtype
        omnisharp.get_response(self.view, '/buildtarget', self._handle_build, params)    
    
    def _handle_build(self, data):
        self.buildcommand = data["Command"]
        build = {
            "cmd": self.buildcommand,
            "shell": "true",
            "syntax": "Packages/OmniSharp/BuildConsole.hidden-tmLanguage",
            "file_regex": "(?:^| |\"|'|\\(|\\[)((?:[A-Za-z]:)?[\\/][^\n \"':\\(\\)\\[\\]]+\\.\\w{0,4})(?=[\n \"':\\(\\)\\[\\]])\\((\\d+),\\d+\\)"
        }
        sublime.active_window().run_command('exec',build)
