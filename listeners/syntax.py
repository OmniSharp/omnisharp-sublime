import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp


class OmniSharpSyntaxEventListener(sublime_plugin.EventListener):
    data = None
    view = None
    semanticdata = None

    def on_modified(self, view):
        if not helpers.is_csharp(view):
            return
        
        self.view = view

        # omnisharp.get_response(view, '/syntaxerrors', self._handle_syntaxerrors)
        omnisharp.get_response(view, '/semanticerrors', self._handle_semanticerrors)
        # if self.data is None:
        #     omnisharp.get_response(view, '/syntaxerrors', self._handle_syntaxerrors)
        # else:
        #     self._show_errors()
        
        print('file changed')


    def _handle_semanticerrors(self, data):
        print('handling semantic Errors')
        if data is None:
            return
        self.view.erase_regions("semanticoops")

        
        sublime.active_window().run_command("hide_panel",{"panel": "output.variable_get"})
        self.semanticdata = data
        self.semanticunderlines = []
        if "Errors" in self.semanticdata and self.semanticdata["Errors"] != None and len(self.semanticdata["Errors"]) > 0:
            output = self.view.window().create_output_panel("variable_get")
            output.run_command('erase_view')
            for i in self.semanticdata["Errors"]:
                point = self.view.text_point(i["Line"]-1, i["Column"])
                reg = self.view.word(point)
                self.semanticunderlines.append(reg)
                output.run_command('append', {'characters': i["Message"].strip() + " - (" + str(i["Line"]) + ", " + str(i["Column"]) + ")" + os.linesep})

            self.view.add_regions("semanticoops", self.semanticunderlines, "illegal", "", sublime.DRAW_NO_FILL + sublime.DRAW_NO_OUTLINE + sublime.DRAW_SQUIGGLY_UNDERLINE)
            self.view.window().run_command("show_panel", {"panel": "output.variable_get"})

        self.semanticdata = None

    def _handle_syntaxerrors(self, data):
        print('handling Errors')
        if data is None:
            return
        self.view.erase_regions("oops")
        self.quickitems = []
        self.data = data
        self.underlines = []
        if "Errors" in self.data and self.data["Errors"] != None:# and len(self.data["Errors"]) > 0:
            for i in self.data["Errors"]:
                # reg = sublime.Region(i["Column"], i["Column"])
                point = self.view.text_point(i["Line"]-1, i["Column"])
                reg = self.view.word(point)
                self.underlines.append(reg)
                self.quickitems.append(i["Message"].strip() + " - (" + str(i["Line"]) + ", " + str(i["Column"]) + ")")
        if len(self.quickitems) > 0:
            # pt = self.view.window().get_output_panel("paneltest")
            # pt.set_read_only(False)
            # edit = pt.begin_edit()
            # pt.insert(edit, pt.size(), "Writing...")
            # pt.end_edit(edit)
            # self.view.window().run_command("show_panel", {"panel": "output.paneltest"})
            #             self.view.window().show_quick_panel(self.quickitems, None)#self.on_done)
            self.view.add_regions("oops", self.underlines, "illegal", "", sublime.DRAW_NO_FILL+sublime.DRAW_NO_OUTLINE+sublime.DRAW_SQUIGGLY_UNDERLINE)

        self.data = None

    def on_done(self, index):
        print('this wont fix it')

        

