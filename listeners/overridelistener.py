import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp


class OmniSharpOverrideListener(sublime_plugin.EventListener):
    data = None
    view = None
    semanticdata = None
    outputpanel = None

    def on_modified(self, view):
        if not helpers.is_csharp(view):
            return
        if bool(helpers.get_settings(view, 'omnisharp_show_override_completion')) == False:
            return;
        pos = view.sel()[0].begin()
        if pos > 9: #override
            reg = sublime.Region(pos-9, pos)
            keyword = view.substr(reg).strip();
            if keyword == 'override':
                view.run_command('omni_sharp_override_targets')


