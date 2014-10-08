import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp


class OmniSharpServerRunnerEventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if not helpers.is_csharp(view):
            return
            
        omnisharp.create_omnisharp_server_subprocess(view)

