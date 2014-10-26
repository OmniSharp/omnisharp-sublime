import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpRunUnitTests(sublime_plugin.TextCommand):
    
    def run(self, edit, testtype='all'):
        print(testtype)
        params = {}
        params["type"] = testtype
        omnisharp.get_response(self.view, '/gettestcontext', self._handle_rununittests, params)

    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())

    def _handle_rununittests(self, data):
        testcommand = data["TestCommand"]
        sublime.active_window().run_command('exec',{"cmd":[testcommand], "shell":"true"})
