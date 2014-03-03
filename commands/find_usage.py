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
        print(data)
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_find_usage')

    def _show_usage_view(self, edit):
        view = self.view.window().new_file()
        view.set_name('Find Results')
        view.set_scratch(True)
        view.set_syntax_file('Packages/Default/Find Results.hidden-tmLanguage')
        text = ''
        region = sublime.Region(0, view.size())
        view.replace(edit, region, text)
        print(self.data)
        self.data = None

    def is_enabled(self):
        return helpers.is_csharp(self.view)
