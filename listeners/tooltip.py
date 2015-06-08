import sublime_plugin, sublime, json, webbrowser
import re
from time import time

class OmniSharpTooltipListener(sublime_plugin.EventListener):

    next_run_time = 0

    def on_activated(self, view):
        self._check_tooltip_after_delay(view)

    def on_modified(self, view):
        self._check_tooltip_after_delay(view)

    def on_selection_modified(self, view):
        self._check_tooltip_after_delay(view)

    def _check_tooltip_after_delay(self, view):
        timeout_ms = 400
        self.next_run_time = time() + 0.0009 * timeout_ms
        sublime.set_timeout(lambda:self._check_tooktip_after_delay_callback(view), timeout_ms)

    def _check_tooktip_after_delay_callback(self, view):
        if self.next_run_time <= time():
            self._check_tooltip(view)

    def _check_tooltip(self, view):

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

            key = "%s,%s" % (word_region.a, word_region.b)
            if key not in oops_map:
                key = "%s,%s" % (region.begin(), region.begin() + 1)
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
        return

