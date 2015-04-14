import os
import sublime
import sublime_plugin
from time import time

from ..lib import helpers
from ..lib import omnisharp


class OmniSharpSyntaxEventListener(sublime_plugin.EventListener):
    data = None
    view = None
    outputpanel = None
    next_run_time = 0

    def on_post_save(self, view):
        self._run_codecheck(view)

    def on_modified(self, view):
        timeout_ms = 500
        self.next_run_time = time() + 0.0009 * timeout_ms
        sublime.set_timeout(lambda:self._run_codecheck_after_delay(view), timeout_ms)

    def _run_codecheck_after_delay(self, view):
        if self.next_run_time <= time():
            self._run_codecheck(view)

    def _run_codecheck(self, view):
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
        self.warninglines = []
        self.errlines = []
        oops_map = {}

        if "QuickFixes" in self.data and self.data["QuickFixes"] != None and len(self.data["QuickFixes"]) > 0:
            for i in self.data["QuickFixes"]:
                point = self.view.text_point(i["Line"]-1, i["Column"])
                reg = self.view.word(point)
                # self.underlines.append(reg)
                if i["LogLevel"] == "Warning" :
                    self.warninglines.append(reg)
                if i["LogLevel"] == "Error" :
                    self.errlines.append(reg)
                key = "%s,%s" % (reg.a, reg.b)
                oops_map[key] = i["Text"].strip()
                self.outputpanel.run_command('append', {'characters': i["LogLevel"] + " : " + i["Text"].strip() + " - (" + str(i["Line"]) + ", " + str(i["Column"]) + ")\n"})
            if len(self.errlines) > 0:
                # print('underlines')
                self.view.settings().set("oops", oops_map)
                self.view.add_regions("oops", self.errlines, "illegal", "",  sublime.DRAW_EMPTY )
                if bool(helpers.get_settings(self.view,'omnisharp_onsave_showerrorwindows')):
                    self.view.window().run_command("show_panel", {"panel": "output.variable_get"})
            if len(self.warninglines) > 0:
                # print('underlines')
                self.view.settings().set("oops", oops_map)
                self.view.add_regions("oops", self.warninglines, "illegal", "", sublime.DRAW_NO_FILL + sublime.DRAW_NO_OUTLINE + sublime.DRAW_SQUIGGLY_UNDERLINE )

        self.data = None


