import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpFindUsage(sublime_plugin.TextCommand):
    def run(self, text):
        omnisharp.get_response(
            self.view, '/findusages', self._handle_findusage)

    def _handle_findusage(self, data):
        if data is None:
            return
        print(data)

    def is_enabled(self):
        return helpers.is_csharp(self.view)
