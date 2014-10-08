import os
import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpGoToFile(sublime_plugin.TextCommand):
    data = None

    def run(self, edit):
        if self.data is None:
            print("getting files")
            omnisharp.get_response_from_empty_httppost(
               self.view, '/gotofile', self._handle_findfiles)
        else:
            self._show_files(edit)

    def _handle_findfiles(self, data):
        print('findfiles response is:')
        print(data)
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_go_to_file')

    def _show_files(self, edit):
        print('findfiles is :')
        print(self.data)
        self.quickitems = [];
        if "QuickFixes" in self.data and self.data["QuickFixes"] != None:
            for i in self.data["QuickFixes"]:
                print(i)
                self.quickitems.append(i["FileName"] + os.linesep)
        if len(self.quickitems) > 0:
            if len(self.quickitems) == 1:
               self.on_done(0) 
            else:
                self.view.window().show_quick_panel(self.quickitems, self.on_done)

    def is_enabled(self):
        return helpers.is_csharp(self.view)

    def on_done(self, index):
        values = self.data["QuickFixes"]
        item = values[index]
        v = self.view.window().open_file(item["FileName"])
        # sublime.set_timeout(lambda: self.file_opened(v, item), 10)

    # def file_opened(self, view, item):
    #     if not view.is_loading():
    #         print('loaded')
    #         view.run_command("goto_line", {"line": item["Line"]})
    #     else:
    #         print('not loaded, trying again')
    #         sublime.set_timeout(lambda: self.file_opened(view, item), 10)
    
    def is_enabled(self):
        return helpers.is_csharp(self.view)
