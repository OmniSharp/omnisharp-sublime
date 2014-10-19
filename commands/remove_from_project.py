import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpRemoveFromProject(sublime_plugin.WindowCommand):
    def run(self):
        omnisharp.get_response(sublime.active_window().active_view(), '/removefromproject', self._handle_removetoproject)

    def is_enabled(self):
        return helpers.is_csharp(sublime.active_window().active_view())

    def _handle_removetoproject(self, data):
        print('file removed from project')