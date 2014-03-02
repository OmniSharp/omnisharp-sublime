import sublime
import os


def is_csharp(view):
    try:
        location = view.sel()[0].begin()
    except:
        return False

    return view.match_selector(location, 'source.cs')


def get_settings(view, name, default=None):
    settings = sublime.load_settings('OmniSharpSublime.sublime-settings')
    from_plugin = settings.get(name, default)
    return view.settings().get(name, from_plugin)


def active_view():
    return sublime.active_window().active_view()


def project_file_name(view):
    filename = view.window().project_file_name()
    return filename


def project_data(view):
    return view.window().project_data()


def current_solution(view):
    project_file = project_file_name(view)
    if project_file is None:
        return None

    project_dir = os.path.dirname(project_file)

    data = project_data(view)
    if 'solution_file' not in data:
        return None

    solution_file_name = data['solution_file']
    solution_file_path = os.path.join(project_dir, solution_file_name)
    solution_file_path = os.path.abspath(solution_file_path)

    return solution_file_path
