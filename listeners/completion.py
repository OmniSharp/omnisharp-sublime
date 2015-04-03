import sublime
import sublime_plugin
import re

from ..lib import helpers
from ..lib import omnisharp
from ..lib.helpers import active_view

AC_OPTS = sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS

class OmniSharpCompletionEventListener(sublime_plugin.EventListener):

    completions = []
    ready_form_defer = False

    def on_query_completions(self, view, prefix, locations):

        if not helpers.is_csharp(view):
            return

        if self.ready_form_defer is True:
            cpl = self.completions
            self.completions = []
            self.ready_form_defer = False
            return cpl

        if re.match("^\W*$", prefix):
            word_to_complete = ''
        else:
            word_to_complete = prefix

        params = {}
        params['wordToComplete'] = word_to_complete
        params['WantSnippet'] = True
        params['WantMethodHeader'] = True
        params['WantReturnType'] = True 
        omnisharp.get_response(view, '/autocomplete', self._complete, params)
        return ([], AC_OPTS)

    def _complete(self, data):
        if data is None:
            return
        
        completions = []
        for item in data:
            completions.append(self.to_completion(item))

        active_view().run_command('hide_auto_complete')
        self.completions = completions 
        self.ready_form_defer = True

        self._run_auto_complete()

    def _run_auto_complete(self):
        active_view().run_command("auto_complete", {
            'disable_auto_insert': True,
            'api_completions_only': True,
            'next_completion_if_showing': False,
            'auto_complete_commit_on_tab': True,
        })

    def to_completion(self, json):
        display = json['MethodHeader'] if json['MethodHeader'] is not None and len(json['MethodHeader']) > 0 else json['CompletionText']
        display += '\t'
        display += json['ReturnType'] if json['ReturnType'] is not None and len(json['ReturnType']) > 0 else json['DisplayText']

        completionText = json['Snippet'] if json['Snippet'] is not None and len(json['Snippet']) > 0 else json['DisplayText']

        return (display, completionText)
