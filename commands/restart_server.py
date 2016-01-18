import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpRestartServer(sublime_plugin.TextCommand):
    def run(self, edit):
        omnisharp.restart_omnisharp_server_subprocess(helpers.active_view())
