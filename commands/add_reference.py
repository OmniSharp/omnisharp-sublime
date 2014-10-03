import time
import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpAddReference(sublime_plugin.TextCommand):
    data = None

    def run(self, edit):
        if self.data is None:
            sublime.active_window().show_input_panel("Add Reference:", "", 
                self._addref_inputed, None, None
            )
        else:
            self._process_addref(edit)

    def _addref_inputed(self, reffilename):
        params = {'reference': reffilename}
        omnisharp.get_response(
            self.view, '/addreference', self._addref_response_received, params)

    def _addref_response_received(self, data):
        self.data = data
        self.view.run_command('omni_sharp_add_reference')

    def _process_addref(self, edit):
        data = self.data
        sublime.status_message(data['Message'])
        self.data = None

    def is_enabled(self):
        return helpers.is_csharp(self.view)
