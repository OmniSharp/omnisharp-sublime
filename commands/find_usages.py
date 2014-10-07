import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpFindUsages(sublime_plugin.TextCommand):
    def run(self, edit):
        omnisharp.get_response(self.view, '/findusages', lambda data: self._show_usages(data))

    def _show_usages(self, data):
        if "QuickFixes" in data and data["QuickFixes"] is not None:
            usages = data["QuickFixes"]
            items = [[u["Text"].strip(), u["FileName"]] for u in usages]
            window = self.view.window()

            def on_done(i):
                if i is not -1:
                    window.open_file('{}:{}:{}'.format(usages[i]["FileName"], usages[i]["Line"] or 0, usages[i]["Column"] or 0), sublime.ENCODED_POSITION)

            window.show_quick_panel(items, on_done)

    def is_enabled(self):
        return helpers.is_csharp(self.view)
