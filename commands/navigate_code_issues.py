import sublime
import sublime_plugin

from ..lib import omnisharp
from ..lib import helpers


class OmniSharpNextCodeIssue(sublime_plugin.TextCommand):
    def run(self, text):
        oops_map = self.get_oops_map()
        if None == oops_map:
            return

        sel = self.view.sel()
        cursor = min(sel[0].a, sel[0].b)

        next_region = None
        all_regions = self.view.get_regions("oops")
        for region in all_regions:
            if (not region.contains(cursor)) and region.begin() > cursor and (next_region == None or region.begin() < next_region.begin()):
                next_region = region

        if next_region == None and len(all_regions) > 0:
            next_region = all_regions[0]

        if next_region != None:
            self.view.show_at_center(next_region)
            sel.clear()
            sel.add(sublime.Region(next_region.begin(), next_region.begin()))

    def is_enabled(self):
        oops_map = self.get_oops_map()
        return None != oops_map

    def get_oops_map(self):
        return self.view.settings().get("oops")


class OmniSharpLastCodeIssue(sublime_plugin.TextCommand):
    def run(self, text):
        oops_map = self.get_oops_map()
        if None == oops_map:
            return

        sel = self.view.sel()
        cursor = min(sel[0].a, sel[0].b)

        next_region = None
        all_regions = self.view.get_regions("oops")
        for region in all_regions:
            if (not region.contains(cursor)) and region.end() < cursor and (next_region == None or region.end() > next_region.end()):
                next_region = region

        if next_region == None and len(all_regions) > 0:
            next_region = all_regions[-1]

        if next_region != None:
            self.view.show_at_center(next_region)
            sel.clear()
            sel.add(sublime.Region(next_region.begin(), next_region.begin()))

    def is_enabled(self):
        oops_map = self.get_oops_map()
        return None != oops_map

    def get_oops_map(self):
        return self.view.settings().get("oops")
