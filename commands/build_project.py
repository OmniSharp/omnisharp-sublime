import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpBuildProject(sublime_plugin.TextCommand):
    
    def run(self, edit, buildtype='build'):
        print('building')
        options = {}
        options['build'] = self.build
        options['rebuild'] = self.rebuild
        options['clean'] = self.clean
        sublime.active_window().run_command("save_all")
        options[buildtype]()

    def build(self):
        self.getbuild('build')

    def rebuild(self):
        self.getbuild('rebuild')

    def clean(self):
        self.getbuild('clean')

    def getbuild(self, buildtype):
        params = {}
        params['type'] = buildtype
        omnisharp.get_response(self.view, '/buildtarget', self._handle_build, params)    
    
    def _handle_build(self, data):
        # settings = sublime.load_settings('OmniSharpSublime.sublime-settings')
        # SYNTAX = settings.get('omnisharp_syntax')
        # THEME = settings.get('omnisharp_color_scheme')
        # self.panel = sublime.active_window().get_output_panel("exec")
        # self.panel.settings().set("color_scheme", THEME)
        # self.panel.set_syntax_file(SYNTAX)


        self.buildcommand = data["Command"]
        build = {
            "cmd": self.buildcommand,
            "shell": "true",
            "file_regex": "^(.*)\((\d+)\,(\d+)\):"
        }
        sublime.active_window().run_command('exec',build)
