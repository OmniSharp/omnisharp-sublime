import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpShowServerOutput(sublime_plugin.TextCommand):
    
    def run(self, edit, testtype='all'):
        sublime.active_window().run_command("show_panel", {"panel": "output.exec"})

    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())

