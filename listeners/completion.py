import sublime
import sublime_plugin
import re

from ..lib import helpers
from ..lib import omnisharp
from ..lib.helpers import active_view


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
        omnisharp.get_response(view, '/autocomplete', self._complete, params)

    def _complete(self, response):
        if response is not None and len(response) > 0:
            completions = []
            for item in response:
                completions.append(self.to_completion(item))

            active_view().run_command('hide_auto_complete')
            self.completions = completions
            self.ready_form_defer = True

            # is the tab key is used to complete just undo the last insertion
            if active_view().command_history(0)[0] == 'insert_best_completion':
                if active_view().substr(sublime.Region(
                        active_view().sel()[0].begin() - 5,
                        active_view().sel()[0].end())) == 'self.':
                    active_view().run_command('undo')

            self._run_auto_complete()

    def _run_auto_complete(self):
        active_view().run_command("auto_complete", {
            'disable_auto_insert': True,
            'api_completions_only': False,
            'next_completion_if_showing': False,
            'auto_complete_commit_on_tab': True,
        })

    def to_completion(self, json):
        display = json['CompletionText']
        display += '\t'
        display += json['DisplayText']

        # Get paramaters out of DisplayText
        pattern = re.compile(r"\(|\)")
        params = pattern.split(json['DisplayText'])
        
        completionText = json['CompletionText']
        paramsSplit = []

        # Split paramaters by comma
        # params starts as 0:(, 1:paramaters, 2:) if this is a method
        # Check if this is a method
        if(len(params) == 3):
        	# Check if method has paramaters
          if params[1] != "":
          	# Separate paramaters by comma
            paramsSplit = params[1].split(',')

        # fix generics completions
        if re.match("^T\W", completionText):
            fixed = re.sub("\(\)?$", "<", completionText)
            completionText = fixed       

        # Output paramaters with field markers if this is a function
        if len(paramsSplit) > 0:
          for i in range(0, len(paramsSplit)):
            completionText += '${' + str(i+1) + ':' + paramsSplit[i].strip() +'}'
            if i < len(paramsSplit)-1:
              completionText += ', '
          completionText += ')'

        return (display, completionText)