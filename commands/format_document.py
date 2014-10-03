import os
import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpFormatDocument(sublime_plugin.TextCommand):
    data = None

    def run(self, edit):
        if self.data is None:
            omnisharp.get_response(
               self.view, '/codeformat', self._handle_formatdocument)
        else:
            self._formatdoc(edit)

    def _handle_formatdocument(self, data):
        print('formatdocument response is:')
        print(data)
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_format_document')

    def _formatdoc(self, edit):
        print('formatdocument is :')
        print(self.data)
        if self.data != None:
            region = sublime.Region(0, self.view.size())
            self.view.replace(edit, region, self.data["Buffer"])
        self.data = None

    def is_enabled(self):
        return helpers.is_csharp(self.view)
