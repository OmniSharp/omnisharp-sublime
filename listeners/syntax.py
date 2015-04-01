import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp


class OmniSharpSyntaxEventListener(sublime_plugin.EventListener):
    data = None
    view = None
    outputpanel = None

    def on_post_save(self, view):
        if not helpers.is_csharp(view):
            return
        
        self.view = view

        sublime.active_window().run_command("hide_panel",{"panel": "output.variable_get"})
        self.outputpanel = self.view.window().create_output_panel("variable_get")
        self.outputpanel.run_command('erase_view')

        self.view.erase_regions("oops")
        if bool(helpers.get_settings(view, 'omnisharp_onsave_codecheck')):
            omnisharp.get_response(view, '/codecheck', self._handle_codeerrors)

        print('file changed')

    def _handle_codeerrors(self, data):
        print('handling Errors')
        if data is None:
            print('no data')
            return
        
        self.data = data
        self.underlines = []
        oops_map = {}

        if "QuickFixes" in self.data and self.data["QuickFixes"] != None and len(self.data["QuickFixes"]) > 0:
            for i in self.data["QuickFixes"]:
                point = self.view.text_point(i["Line"]-1, i["Column"])
                reg = self.view.word(point)
                self.underlines.append(reg)
                logline = i["LogLevel"] + " : " + i["Text"].strip() + " - (" + str(i["Line"]) + ", " + str(i["Column"]) + ")\n"
                oops_map[str(i["Line"]-1) + "@" + self.view.substr(reg)] = i["Text"].strip()
                self.outputpanel.run_command('append', {'characters': logline})
            if len(self.underlines) > 0:
                print('underlines')
                self.view.settings().set("oops", oops_map)
                self.view.add_regions("oops", self.underlines, "illegal", "", sublime.DRAW_NO_FILL + sublime.DRAW_NO_OUTLINE + sublime.DRAW_SQUIGGLY_UNDERLINE)

        self.data = None


