import os
import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpFindUsage(sublime_plugin.TextCommand):
    data = None

    def run(self, edit):
        if self.data is None:
            omnisharp.get_response(
               self.view, '/findusages', self._handle_findusage)
        else:
            self._show_usage_view(edit)

    def _handle_findusage(self, data):
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_find_usage')

    def _show_usage_view(self, edit):
        if "QuickFixes" in self.data and self.data["QuickFixes"] is not None:
            usages = self.data["QuickFixes"]
            items = [[u["Text"].strip(), u["FileName"]] for u in usages]
            window = self.view.window()
            window.show_quick_panel(items,
                lambda i: window.open_file('{}:{}:{}'.format(usages[i]["FileName"], usages[i]["Line"] or 0, usages[i]["Column"] or 0), sublime.ENCODED_POSITION))

        self.data = None

    def is_enabled(self):
        return helpers.is_csharp(self.view)
