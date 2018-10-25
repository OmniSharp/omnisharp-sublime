import os
import sublime
import sublime_plugin
from time import time

from ..lib import helpers
from ..lib import omnisharp
from ..lib.view import OutputPanel


class OmniSharpSyntaxEventListener(sublime_plugin.EventListener):
    data = None
    view = None
    outputpanel = None
    next_run_time = 0

    def on_activated(self, view):
        if bool(helpers.get_settings(view, 'omnisharp_onload_codecheck')):
            self._run_codecheck_after_delay(view)

    def on_modified(self, view):
        if bool(helpers.get_settings(view, 'omnisharp_onedit_codecheck')):
            self._run_codecheck(view)

    def on_post_save(self, view):
        if bool(helpers.get_settings(view, 'omnisharp_onsave_codecheck')):
            self._run_codecheck_after_delay(view)

    def _run_codecheck_after_delay(self, view):
        timeout_ms = 500
        self.next_run_time = time() + 0.0009 * timeout_ms
        sublime.set_timeout(lambda:self._run_codecheck_after_delay_callback(view), timeout_ms)

    def _run_codecheck_after_delay_callback(self, view):
        if self.next_run_time <= time():
            self._run_codecheck(view)

    def _run_codecheck(self, view):
        if not helpers.is_csharp(view):
            return
        
        self.view = view

        sublime.active_window().run_command("hide_panel",{"panel": "output.variable_get"})
        self.outputpanel = OutputPanel(sublime.active_window(),"variable_get", r"File: (.+)$",r"\((\d+), (\d+)\)$")
        self.outputpanel.clear()
        self.outputpanel.view.set_syntax_file("Packages/OmniSharp/OutputPanel.hidden-tmLanguage")
        self.outputpanel.view.settings().set("color_scheme", 'Packages/OmniSharp/BuildConsole.hidden-tmTheme')

        self.view.erase_regions("oops")
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
            self.data["QuickFixes"].sort(key = lambda a:(a['Line'],a['Column']))
            self.outputpanel.write_line("File: "+self.data["QuickFixes"][0]["FileName"]+"\n")
            for i in self.data["QuickFixes"]:
                point = self.view.text_point(i["Line"]-1, i["Column"]-1)
                reg = self.view.word(point)
                region_that_would_be_looked_up = self.view.word(reg.begin())
                if region_that_would_be_looked_up.begin() != reg.begin() or region_that_would_be_looked_up.end() != reg.end():
                    reg = sublime.Region(point, point+1)
                # self.underlines.append(reg)
                if i["LogLevel"] == "Warning" :
                    self.warninglines.append(reg)
                if i["LogLevel"] == "Error" :
                    self.errlines.append(reg)
                key = "%s,%s" % (reg.a, reg.b)
                oops_map[key] = i["Text"].strip()
                self.outputpanel.write_line(i["LogLevel"] + " : " + i["Text"].strip() + " - (" + str(i["Line"]) + ", " + str(i["Column"]) + ")")
            showErrorPanel = bool(helpers.get_settings(self.view,'omnisharp_showerrorwindows'))
            showWarningPanel = bool(helpers.get_settings(self.view,'omnisharp_showwarningwindows'))
            haveError = len(self.errlines) > 0
            if haveError:
                # print('underlines')
                self.view.settings().set("oops", oops_map)
                self.view.add_regions("oops", self.errlines, "sublimelinter.mark.error", "circle",  sublime.DRAW_NO_FILL|sublime.DRAW_NO_OUTLINE|sublime.DRAW_SOLID_UNDERLINE )
                if showErrorPanel:
                    self.view.window().run_command("show_panel", {"panel": "output.variable_get"})
            if len(self.warninglines) > 0:
                # print('underlines')
                self.view.settings().set("oops", oops_map)
                self.view.add_regions("oops", self.warninglines, "sublimelinter.mark.warning", "dot", sublime.DRAW_NO_FILL + sublime.DRAW_NO_OUTLINE + sublime.DRAW_SQUIGGLY_UNDERLINE )
                if (not haveError or not showErrorPanel) and showWarningPanel:
                    self.view.window().run_command("show_panel", {"panel": "output.variable_get"})

        self.data = None

        # Make error panel be scrolled to top so that we can see the first error:
        self.outputpanel.view.set_viewport_position((0,0))

