import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpFindUsages(sublime_plugin.TextCommand):
    def run(self, edit):
        omnisharp.get_response(self.view, '/findusages', self._show_usages)

    def _show_usages(self, data):
        if data is None or data['QuickFixes'] is None:
            return

        usages = data["QuickFixes"]
        items = [[u["Text"].strip(), u["FileName"] + " Line : " + str(u["Line"])] for u in usages]
        window = sublime.active_window()

        def on_done(i):
            if i is not -1:
                window.open_file('{}:{}:{}'.format(usages[i]["FileName"], usages[i]["Line"] or 0, usages[i]["Column"] or 0), sublime.ENCODED_POSITION)

        def on_highlight(i):
            if i is not -1:
                window.open_file('{}:{}:{}'.format(usages[i]["FileName"], usages[i]["Line"] or 0, usages[i]["Column"] or 0), sublime.ENCODED_POSITION | sublime.TRANSIENT)

        window.show_quick_panel(items, on_done, on_highlight=on_highlight)

    def is_enabled(self):
        return helpers.is_csharp(self.view)
