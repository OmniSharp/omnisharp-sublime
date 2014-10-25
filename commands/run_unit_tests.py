import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpRunUnitTests(sublime_plugin.TextCommand):
    def run(self, edit):
        omnisharp.get_response(self.view, '/gettestcontext', self._handle_rununittests)

    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())

    def _handle_rununittests(self, data):
    	
        testcommand = data["TestCommand"]
        commands = testcommand.split(' ')
        if os.name == 'posix':
        	sublime.active_window().run_command('exec',{"cmd":['mono',commands[0], commands[1].replace('"','')]})
        # else:
        #     sublime.active_window().run_command('exec','')