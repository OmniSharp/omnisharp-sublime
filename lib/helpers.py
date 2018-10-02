import sublime
import os
import fnmatch
import json



def is_csharp(view):
    if len(view.sel()) == 0:
        return False

    location = view.sel()[0].begin()
    return view.match_selector(location, 'source.cs')


def get_settings(view, name, default=None):
    settings = sublime.load_settings('OmniSharpSublime.sublime-settings')
    from_plugin = settings.get(name, default)
    return view.settings().get(name, from_plugin)


def active_view():
    return sublime.active_window().active_view()


def project_file_name(view):
    return view.window().project_file_name()


def project_data(view):
    return view.window().project_data()


def current_solution_filepath_or_project_rootpath(view):
    project_file = project_file_name(view)
    if project_file is not None:
        print('project file %s found' % project_file)

        data = project_data(view)
        if 'solution_file' not in data:
            raise ValueError('Please specify a path to the solution file in your sublime-project file or delete it')

        project_dir = os.path.dirname(project_file)
        solution_file_name = data['solution_file']
        solution_file_path = os.path.join(project_dir, solution_file_name)
        return os.path.abspath(solution_file_path)
    else:
        active_window = sublime.active_window()

        if len(active_window.folders()) > 0:
            return active_window.folders()[
                0]  # assume parent folder is opened that contains all project folders eg/Web,ClassLib,Tests

        try:
            return os.path.dirname(active_window.active_view().file_name())
        except Exception:
            print("New file not saved. Can't find path.")
            return None


def get_omni_active(view):
    """
        Returns the active omnisharp server
    :param view:
    :return:
    """
    servers = get_settings(view, "omnisharp_servers")
    active_server = get_settings(view, "omnisharp_server_active")

    for server in servers:
        if(server.get("name") == active_server):
            return server

    raise Exception("No OmniSharpSever selected")


def get_omni_path(view):
    """
        Returns the path to the active omnisharp server's executable.
        If the path in the config file contains a .* then it will
        attempt to match it to .cmd on windows, or no extension on a nix.
    :param view:
    :return: string
    """
    relative_omni_path = get_omni_active(view).get("path")

    if relative_omni_path is None:
        return None

    absolute_omni_path = os.path.abspath(get_plugin_path() + os.sep + relative_omni_path).replace('\\', '/')

    if absolute_omni_path.endswith(".*"):
        absolute_omni_path = absolute_omni_path[0:-2] + ("" if os.name == 'posix' else ".cmd")
    return absolute_omni_path


def get_config_path(view):
    """
        Returns the path to the active omnisharp server's config file.
    :param view:
    :return: string
    """
    relative_config_path = get_omni_active(view).get("config")

    if relative_config_path is None:
        return None
    return os.path.abspath(get_plugin_path() + os.sep + relative_config_path).replace('\\', '/')


def get_plugin_path():
    """
        Returns the path to the plugin folder
    :return: string
    """
    if os.name == 'posix':
        source_file_path = os.path.realpath(__file__)
    else:
        source_file_path = os.path.realpath(__file__).replace('\\', '/')

    source_dir_path = os.path.dirname(source_file_path)
    plugin_dir_path = os.path.dirname(source_dir_path)
    return plugin_dir_path


def save_all_files(window):
    """
        Saves all the files open in the window
    :param window:
    """
    for view in window.views():
        if view.file_name() and view.is_dirty():
            view.run_command("save")


def quote_path(path):
    """
        Surrounds the path in quotes.
    :param path:
    :return: string
    """
    return '"' + path.strip('"') + '"'
