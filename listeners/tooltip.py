import sublime_plugin, sublime, json, webbrowser
import re, os
from time import time

settings = {}

class OmniSharpTooltipListener(sublime_plugin.EventListener):

    cache = {}
    region_row = []
    lang = None


    def on_activated(self, view):
        self.time = time()
        sublime.set_timeout(lambda:self.run(view, 'activated'), 0)

    def on_modified(self, view):
        self.time = time()

    def on_selection_modified(self, view):
        now = time()
        sublime.set_timeout(lambda:self.run(view, 'selection_modified'), 0)
        self.time = now

    def run(self, view, where):
        global region_row, lang

        view_settings = view.settings()
        if view_settings.get('is_widget'):
            return

        oops_map = view.settings().get("oops")
        if None == oops_map:
            return

        for region in view.sel():

            row_col = view.rowcol(region.begin())
            word_region = view.word(region.begin())
            word = view.substr(word_region)

            key = str(row_col[0]) + "@" + word
            if key not in oops_map:
                continue

            issue = oops_map[key]

            css = "html {background-color: #232628; color: #CCCCCC; } body {font-size: 12px; } a {color: #6699cc; } b {color: #cc99cc; } h1 {color: #99cc99; font-size: 14px; }"
            html = ['<style>%s</style>' % css]
            html.append(issue)

            view.show_popup(''.join(html), location=-1, max_width=600, on_navigate=self.on_navigate)

            return

        view.hide_popup()

    def on_navigate(self, link):
        global lang

