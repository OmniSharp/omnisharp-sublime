import time
import sublime
import sublime_plugin
import fnmatch
import os

from ..lib import omnisharp
from ..lib import helpers

class OmniSharpAddReference(sublime_plugin.TextCommand):
    
    def run(self, edit):
        parentpath =  sublime.active_window().folders()[0]
        matches = []
        for root, dirnames, filenames in os.walk(parentpath):
          if 'bin' not in root or 'obj' not in root:
            for filename in fnmatch.filter(filenames, '*.dll'):
              matches.append(os.path.join(root, filename))

        def on_done(i):
            if i is not -1:
                params = {'reference': matches[i]}
                omnisharp.get_response(
                    self.view, '/addreference', self._process_addref, params)

        if len(matches) > 0:
            sublime.active_window().show_quick_panel(matches, on_done)
        else:
            sublime.status_message('No libraries found to add reference to')


    def _process_addref(self, data):
        sublime.status_message(data['Message'])

    def is_enabled(self):
        return helpers.is_csharp(self.view)
