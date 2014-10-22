import os
import sublime
import sublime_plugin

from ..lib import helpers
from ..lib import omnisharp

class OmniSharpNewClass(sublime_plugin.TextCommand):
    
    PACKAGE_NAME = 'omnisharpsublime'
    TMLP_DIR = 'templates'

    def run(self, edit, type='class'):
        print(sublime.active_window().project_file_name())
        tmpl = self.get_code(type)
        self.tab = self.creat_tab(self.view)

        self.set_syntax()
        self.set_code(tmpl)

    def get_code(self, type):
        code = ''
        file_name = "%s.tmpl" % type
        isIOError = False

        tmpl_dir = 'Packages/' + self.PACKAGE_NAME + '/' + self.TMLP_DIR + '/'
        user_tmpl_dir = 'Packages/User/' + \
            self.PACKAGE_NAME + '/' + self.TMLP_DIR + '/'


        self.user_tmpl_path = os.path.join(user_tmpl_dir, file_name)
        self.tmpl_path = os.path.join(tmpl_dir, file_name)

        try:
            code = sublime.load_resource(self.user_tmpl_path)
        except IOError:
            try:
                code = sublime.load_resource(self.tmpl_path)
            except IOError:
                isIOError = True

        if isIOError:
            sublime.message_dialog('[Warning] No such file: ' + self.tmpl_path
                                   + ' or ' + self.user_tmpl_path)

        return code

    def creat_tab(self, view):
        win = view.window()
        tab = win.new_file()
        tab.set_name('FSFSDFSF')
        return tab

    def set_code(self, code):
        tab = self.tab
        tab.run_command('insert_snippet', {'contents': code})

    def set_syntax(self):
        v = self.tab

        v.set_syntax_file('Packages/C#/C#.tmLanguage')
