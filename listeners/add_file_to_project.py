import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp


class OmniSharpAddFileToProjectEventListener(sublime_plugin.EventListener):

    def on_post_save(self, view):
        if not helpers.is_csharp(view):
            return

        # omnisharp.get_response(view, '/addtoproject', self._handle_addtoproject)


    def _handle_addtoproject(self, data):
        print('file added to project')
        print(data)


