import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpHidePanel(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().run_command("hide_panel",{"panel": "output.variable_get"})