import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpRunUnitTests(sublime_plugin.TextCommand):
    
    def run(self, edit, testtype='all'):
        sublime.active_window().run_command("save_all")
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
            "shell": "true"
        }
        sublime.active_window().run_command('exec',build)

