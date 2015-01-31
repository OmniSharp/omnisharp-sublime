import sublime
import os
import fnmatch

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

def current_project_folder(view):
    project_file = project_file_name(view)
    print('project file is : ' + project_file)
    if project_file is None:
        return None
    project_dir = os.path.dirname(project_file)
    return project_dir

def current_solution_or_folder(view):
    project_file = project_file_name(view)
    print('project file is : ' + project_file)
    if project_file is None:
        return current_project_folder(view)

    project_dir = os.path.dirname(project_file)

    data = project_data(view)
    if 'solution_file' not in data:
        return current_project_folder(view)

    solution_file_name = data['solution_file']
    solution_file_path = os.path.join(project_dir, solution_file_name)
    solution_file_path = os.path.abspath(solution_file_path)

    return solution_file_path

def current_solution_or_project_json_folder(view):
    project_file = project_file_name(view)
    if project_file is not None:
        print('project file found')
        project_dir = os.path.dirname(project_file)

        data = project_data(view)
        if 'solution_file' not in data:
            raise ValueError('Please specify a path to the solution file in your sublime-project file or delete it')
        else:
            solution_file_name = data['solution_file']
            solution_file_path = os.path.join(project_dir, solution_file_name)
            solution_file_path = os.path.abspath(solution_file_path)
            return solution_file_path
    else:
        parentpath = sublime.active_window().folders()[0] #assume parent folder is opened that contains all project folders eg/Web,ClassLib,Tests

        for root, dirnames, filenames in os.walk(parentpath):
          if 'bin' not in root or 'obj' not in root:
            for filename in filenames:
                if filename.endswith(('.sln', 'project.json')):
                    if filename.endswith('.sln'):
                        print ("discovery solution is : " + os.path.join(root, filename))
                        return os.path.join(root, filename)
                    else:
                        print("vnext root is : " + root)
                        return root

def current_solution_or_vnext_folder(view):
    project_file = project_file_name(view)
    
    if project_file is not None:
        project_dir = os.path.dirname(project_file)
        return project_dir
    else:
        parentpath = sublime.active_window().folders()[0] #assume parent folder is opened that contains all project folders eg/Web,ClassLib,Tests
<<<<<<< HEAD

        for root, dirnames, filenames in os.walk(parentpath):
          if 'bin' not in root or 'obj' not in root:
            for filename in filenames:
                if filename.endswith(('.sln', 'project.json')):
                    print("root is : " + root)
                    return root
=======
        print(parentpath)
        return parentpath
        # for root, dirnames, filenames in os.walk(parentpath):
        #   if 'bin' not in root or 'obj' not in root:
        #     for filename in filenames:
        #         if filename.endswith(('.sln', 'project.json')):
        #             #if filename.endswith('.sln'):
        #             #print("dir is : " + dirnames)
        #             print("root is : " + root)
        #             return root
>>>>>>> b11115d... latest server and minor fix to retrieve root folder in helpers.py

