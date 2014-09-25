import sublime
import sublime_plugin
import re

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpOverrideTargets(sublime_plugin.TextCommand):
    data = None
    quickitems = None
    runtargetdata = None
    currentedit = None

    def run(self, edit):
        if self.data is None:
            location = self.view.sel()[0]
            cursor = self.view.rowcol(location.begin())
            row = cursor[0] 
            col = cursor[1] 
            point = self.view.text_point(row,col)
            self.lineregion = self.view.full_line(point)

            omnisharp.get_response(self.view, '/getoverridetargets', self._handle_overridetargets)
        else:
            self._show_override_targets(edit)

    def _handle_overridetargets(self, data):
        print(data)
        if data is None:
            return
        self.data = data
        self.view.run_command('omni_sharp_override_targets')

    def _show_override_targets(self, edit):
        print('overridetargets is :')
        print(self.data)
        self.quickitems = [];
        if len(self.data) > 0:
            for i in self.data:
                print(i['OverrideTargetName'])
                self.quickitems.append(i["OverrideTargetName"].strip())
        if len(self.quickitems) > 0:
            self.currentedit = edit
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
        print(item)

        params = {}
        params['overrideTargetName'] = item["OverrideTargetName"].strip()
        omnisharp.get_response(self.view, '/runoverridetarget', self._handle_runtarget, params)
        self.data = None
        
    def _handle_runtarget(self, data):
        print('runtarget is:')
        print(data)
        if data is None:
            return
        
        self.view.run_command("omni_sharp_run_target",{"args":{'text':data['Buffer'], 'a':self.lineregion.a, 'b':self.lineregion.b}})

class OmniSharpRunTarget(sublime_plugin.TextCommand):
  def run(self, edit, args):
    region = sublime.Region(0, self.view.size())
    self.view.replace(edit, region, args['text'])
    
    lineregion = sublime.Region(args['a'], args['b'])
    self.view.erase(edit,lineregion)