import os
import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpFixUsings(sublime_plugin.TextCommand):
    data = None

    def run(self, edit):
        if self.data is None:
            omnisharp.get_response(
               self.view, '/fixusings', self._handle_fixusings)
        else:
            self._fixusings(edit)

    def _handle_fixusings(self, data):
        print('fixusings response is:')
        print(data)
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_fix_usings')

    def _fixusings(self, edit):
        print('fixusings is :')
        print(self.data)
        if self.data != None:
            region = sublime.Region(0, self.view.size())
            self.view.replace(edit, region, self.data["Buffer"])
        self.data = None

    def is_enabled(self):
        return helpers.is_csharp(self.view)
