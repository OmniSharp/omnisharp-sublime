import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpGoToDefinition(sublime_plugin.TextCommand):
    def run(self, text):
        omnisharp.get_response(
            self.view, '/gotodefinition', self._handle_gotodefinition)

    def _handle_gotodefinition(self, data):
        if data is None or data['FileName'] is None:
            return

        filename = data['FileName']
        line = data['Line']
        column = data['Column']

        sublime.active_window().open_file(
            '{}:{}:{}'.format(filename, line or 0, column or 0),
            sublime.ENCODED_POSITION)

    def is_enabled(self):
        return helpers.is_csharp(self.view)
