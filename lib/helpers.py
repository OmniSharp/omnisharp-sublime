import sublime


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
