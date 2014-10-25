import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpTypeLookup(sublime_plugin.TextCommand):
    outputpanel = None
    
    def run(self, edit):
        
        sublime.active_window().run_command("hide_panel",{"panel": "output.variable_get"})
        self.outputpanel = self.view.window().create_output_panel("variable_get")
        self.outputpanel.run_command('erase_view')

        params = {}
        params["includedocumentation"] = True
        omnisharp.get_response(self.view, '/typelookup', self._handle_typelookup, params)

    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())

    def _handle_typelookup(self, data):
        sublime.status_message('' if data["Type"] is None else data["Type"])
        if data["Documentation"] is not None:
            self.outputpanel.run_command('append', {'characters': "Type : " + '' if data["Type"] is None else data["Type"] + "\n" + "Documentation : " + '' if data["Documentation"] is None else data["Documentation"]})
            self.view.window().run_command("show_panel", {"panel": "output.variable_get"})
