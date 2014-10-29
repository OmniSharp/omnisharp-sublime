import time
import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpRename(sublime_plugin.TextCommand):
    data = None

    def run(self, edit):
        if self.data is None:
            location = self.view.word(self.view.sel()[0].begin())
            old_name = self.view.substr(location)
            sublime.active_window().show_input_panel(
                "Replace with:", old_name,
                self._replacement_inputed, None, None
            )
        else:
            self._process_rename(edit)

    def _replacement_inputed(self, replacement):
        params = {'renameto': replacement}
        omnisharp.get_response(
            self.view, '/rename', self._rename_response_received, params)

    def _rename_response_received(self, data):
        self.data = data
        self.view.run_command('omni_sharp_rename')

    def _process_rename(self, edit):
        data = self.data
        for item in data['Changes']:
            filename = item['FileName']
            text = item['Buffer']
            view = sublime.active_window().open_file(
                '{}:0:0'.format(filename),
                sublime.ENCODED_POSITION
            )
            sublime.active_window().run_command("omni_sharp_replace_file",{"args":{'text':item['Buffer'],'filename':filename}})
            
        self.data = None

    def is_enabled(self):
        return helpers.is_csharp(self.view)

class OmniSharpReplaceFile(sublime_plugin.TextCommand):

    def run(self,edit,args):
        foundview = sublime.active_window().find_open_file(args['filename'])
        if not foundview.is_loading():
            region = sublime.Region(0, foundview.size())
            foundview.replace(edit,region,args['text'])
        else:
            sublime.set_timeout(lambda: self._try_again(args['text'],args['filename']), 10)

    def _try_again(self, text, filename):
        sublime.active_window().run_command("omni_sharp_replace_file",{"args":{'text':text,'filename':filename}})
 
