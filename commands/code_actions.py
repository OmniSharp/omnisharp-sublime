import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpCodeActions(sublime_plugin.TextCommand):
    data = None
    selectionStartColumn = 0
    selectionStartLine = 0
    selectionEndColumn = 0
    selectionEndLine = 0

    def run(self, edit):
        if self.data is None:

            selection = self.view.sel()
            
            params = {}

            if len(selection) > 0:
                print('length is : ' + str(len(selection)))
                location = selection[0]
                cursor = self.view.rowcol(location.begin())
                
                self.selectionStartLine = cursor[0] + 1
                self.selectionStartColumn = cursor[1] + 1

                othercursor = self.view.rowcol(location.end())
                self.selectionEndLine = othercursor[0] + 1
                self.selectionEndColumn = othercursor[1] + 1

                params['selectionStartColumn'] = self.selectionStartColumn
                params['selectionStartLine'] = self.selectionStartLine
                params['selectionEndColumn'] = self.selectionEndColumn
                params['selectionEndLine'] = self.selectionEndLine

            omnisharp.get_response(
                self.view, '/getcodeactions', self._handle_codeactions, params)
        else:
            self._show_code_actions_view(edit)

    def _handle_codeactions(self, data):
        print(data)
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_code_actions')

    def _show_code_actions_view(self, edit):
        print('codeactions is :')
        print(self.data)
        self.quickitems = [];
        if "CodeActions" in self.data and self.data["CodeActions"] != None:
            for i in self.data["CodeActions"]:
                print(i)
                self.quickitems.append(i.strip())
        if len(self.quickitems) > 0:
            self.view.window().show_quick_panel(self.quickitems, self.on_done)
        else:
            self.data = None
            self.selectionEndLine = 0
            self.selectionEndColumn = 0
            self.selectionStartLine = 0
            self.selectionStartColumn = 0

    def is_enabled(self):
        return helpers.is_csharp(self.view)

    def on_done(self, index):
        if index == -1:
            self.data = None
            self.selectionEndLine = 0
            self.selectionEndColumn = 0
            self.selectionStartLine = 0
            self.selectionStartColumn = 0
            return

        print("run index: " + str(index))

        params = {}
        params['codeAction'] = index
        params['selectionStartColumn'] = self.selectionStartColumn
        params['selectionStartLine'] = self.selectionStartLine
        params['selectionEndColumn'] = self.selectionEndColumn
        params['selectionEndLine'] = self.selectionEndLine
        omnisharp.get_response(self.view, '/runcodeaction', self._handle_runcodeaction, params)
        self.data = None
        self.selectionEndLine = 0
        self.selectionEndColumn = 0
        self.selectionStartLine = 0
        self.selectionStartColumn = 0
        
    def _handle_runcodeaction(self, data):
        print('runcodeaction is:')
        print(data)
        if data is None:
            return
        
        self.view.run_command("omni_sharp_run_code_action",{"args":{'text':data['Text']}})

class OmniSharpRunCodeAction(sublime_plugin.TextCommand):
  def run(self, edit, args):
    region = sublime.Region(0, self.view.size())
    self.view.replace(edit, region, args['text'])
