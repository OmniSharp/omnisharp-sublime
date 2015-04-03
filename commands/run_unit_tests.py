import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpRunUnitTests(sublime_plugin.TextCommand):
    
    def run(self, edit, testtype='all'):
        helpers.save_all_files(sublime.active_window())
        params = {}
        params["type"] = testtype
        omnisharp.get_response(self.view, '/gettestcontext', self._handle_rununittests, params)

    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())

    def _handle_rununittests(self, data):
        self.testcommand = data["TestCommand"]

        params = {}
        params["type"] = "build"
        omnisharp.get_response(self.view, '/buildtarget', self._handle_build, params)    
    
    def _handle_build(self, data):
        self.buildcommand = data["Command"]
        build = {
            "cmd": self.buildcommand + " && " + self.testcommand,
            "shell": "true",
            "syntax": "Packages/OmniSharp/BuildConsole.hidden-tmLanguage",
            "file_regex": "(?:^| |\"|'|\\(|\\[)((?:[A-Za-z]:)?[\\/][^\n \"':\\(\\)\\[\\]]+\\.\\w{0,4})(?=[\n \"':\\(\\)\\[\\]])\\((\\d+),\\d+\\)"
        }
        sublime.active_window().run_command('exec',build)

