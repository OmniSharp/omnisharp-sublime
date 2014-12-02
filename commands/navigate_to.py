import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpNavigateTo(sublime_plugin.TextCommand):
    data = None


    def run(self, edit):
        if self.data is None:
            params = {}
            params['ShowAccessModifiers'] = False
            omnisharp.get_response(
                self.view, '/currentfilemembersasflat', self._handle_file_members, params)
        else:
            self._show_file_members(edit)

    def _handle_file_members(self, data):
        print(data)
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_navigate_to')

    def _show_file_members(self, edit):

        self.quickitems = [];
        
        for i in self.data:
            self.quickitems.append(i['Text'].strip())

        if len(self.quickitems) > 0:
            self.view.window().show_quick_panel(self.quickitems, self.on_done)
        else:
            self.data = None

    def is_enabled(self):
        return helpers.is_csharp(self.view)

    def on_done(self, index):
        if index == -1:
            self.data = None
            return

        item = self.data[index]

        self.view.run_command("goto_line", {"line": item["Line"]})