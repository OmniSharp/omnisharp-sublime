from sublime import Region, Window

from ._view import ViewSettings, unset_read_only, append, clear, get_text
from .. import ST3

if ST3:
    basestring = str


class OutputPanel(object):
    """This class represents an output panel (useful for e.g. build systems).
    Please note that the panel's contents will be cleared on __init__.

    Can be used as a context handler in `with` statement which will
    automatically invoke the `finish()` method.

    Example usage:

        with OutputPanel(sublime.active_window(), "test") as output:
            output.write_line("some testing here")


    OutputPanel(window, panel_name, file_regex=None, line_regex=None, path=None,
                read_only=True, auto_show=True)
        * window
            The window. This is usually `self.window` or
            `self.view.window()`, depending on the type of your command.

        * panel_name
            The panel's name, passed to `window.get_output_panel()`.

        * file_regex
            Important for Build Systems. The user can browse the errors you
            writewith F4 and Shift+F4 keys. The error's location is
            determined with 3 capturing groups:
            the file name, the line number and the column.
            The last two are optional.

            Example:
                r"Error in file "(.*?)", line (\d+), column (\d+)"

        * line_regex
            Same style as `file_regex` except that it misses the first
            group for the file name.

            If `file_regex` doesn't match on the current line, but
            `line_regex` exists, and it does match on the current line,
            then walk backwards through the buffer until a line matching
            file regex is found, and use these two matches
            to determine the file and line to go to; column is optional.

        * path
            This is only needed if you specify the file_regex param and
            will be used as the root dir for relative filenames when
            determining error locations.

        * read_only
            A boolean whether the output panel should be read only.
            You usually want this to be true.
            Can be modified with `self.view.set_read_only()` when needed.

        * auto_show
            Option if the panel should be shown when `finish()` is called and
            text has been added.

    Useful attributes:

        view
            The view handle of the output panel. Can be passed to
            `Edit(output.view)` to group modifications for example.

    Defines the following methods:

        set_path(path=None, file_regex=None, line_regex=None)
            Used to update `path`, `file_regex` and `line_regex` if
            they are not `None`, see the constructor for information
            about these parameters.

            The file_regex is updated automatically because it might happen
            that the same panel_name is used multiple times.
            If `file_regex` is omitted or `None` it will be reset to
            the latest regex specified (when creating the instance or from
            the last call of  set_regex/path).
            The same applies to `line_regex`.

        set_regex(file_regex=None, line_regex=None)
            Subset of set_path. Read there for further information.

        write(text)
            Will just write appending `text` to the output panel.

        write_line(text='')
            Same as write() but inserts a newline at the end.

        clear()
            Erases all text in the output panel.

        show()
        hide()
            Show or hide the output panel.

        finish()
            Call this when you are done with updating the panel.
            Required if you want the next_result command (F4) to work.
            If `auto_show` is true, will also show the panel if text was added.
    """
    def __init__(self, window, panel_name, file_regex=None,
                 line_regex=None, path=None, read_only=True,
                 auto_show=True):
        if not isinstance(window, Window):
            raise ValueError("window parameter is invalid")
        if not isinstance(panel_name, basestring):
            raise ValueError("panel_name must be a string")

        self.window = window
        self.panel_name = panel_name
        self.view = window.get_output_panel(panel_name)
        self.view.set_read_only(read_only)
        self.settings = ViewSettings(self.view)

        self.set_path(path, file_regex, line_regex)

        self.auto_show = auto_show

    def set_path(self, path=None, file_regex=None, line_regex=None):
        """Update the view's result_base_dir pattern.
        Only overrides the previous settings if parameters are not None.
        """
        if path is not None:
            self.settings.result_base_dir = path
        # Also always update the file_regex
        self.set_regex(file_regex, line_regex)

    def set_regex(self, file_regex=None, line_regex=None):
        """Update the view's result_(file|line)_regex patterns.
        Only overrides the previous settings if parameters are not None.
        """
        if file_regex is not None:
            self.file_regex = file_regex
        if hasattr(self, 'file_regex'):
            self.settings.result_file_regex = self.file_regex

        if line_regex is not None:
            self.line_regex = line_regex
        if hasattr(self, 'line_regex'):
            self.settings.result_line_regex = self.line_regex

        # Call get_output_panel again after assigning the above settings, so
        # that "next_result" and "prev_result" work. However, it will also clear
        # the view so read it before and re-write its contents afterwards. Cache
        # selection as well.
        contents = get_text(self.view)
        sel = self.view.sel()
        selections = list(sel)
        self.view = self.window.get_output_panel(self.panel_name)
        sel.clear()
        for reg in selections:  # sel.add_all requires a `RegionSet` in ST2
            sel.add(reg)
        self.write(contents)

    def write(self, text):
        """Appends `text` to the output panel.
        Alias for `sublime_lib.view.append(self.view, text)`
        + `with unset_read_only:`.
        """
        with unset_read_only(self.view):
            append(self.view, text)

    def write_line(self, text=''):
        """Appends `text` to the output panel and starts a new line.
        """
        self.write(text + "\n")

    def clear(self):
        """Clears the output panel.
        Alias for `sublime_lib.view.clear(self.view)`.
        """
        with unset_read_only(self.view):
            clear(self.view)

    def show(self):
        """Makes the output panel visible.
        """
        self.window.run_command("show_panel",
                                {"panel": "output.%s" % self.panel_name})

    def hide(self):
        """Makes the output panel invisible.
        """
        self.window.run_command("hide_panel",
                                {"panel": "output.%s" % self.panel_name})

    def finish(self):
        """Things that are required to use the output panel properly.

        Set the selection to the start, so that next_result will work as
        expected. Also shows the panel if text has been added.
        """
        self.set_path()
        self.view.sel().clear()
        self.view.sel().add(Region(0))
        if self.auto_show:
            if self.view.size():
                self.show()
            else:
                self.hide()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.finish()
