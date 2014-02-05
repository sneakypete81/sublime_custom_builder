import sublime, sublime_plugin

_SETTINGS_FILENAME = "Custom Builder.sublime-settings"

class CustomBuilderPromptCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwds):
        self._commands = HistoryList("commands")
        self._kwds = {}

        sublime_plugin.WindowCommand.__init__(self, *args, **kwds)

    def run(self, **kwds):
        self._kwds = kwds
        self._select_command()

    def _select_command(self):
        self.window.show_quick_panel([["Title Goes Here", cmd] for cmd in self._commands] + [["<Other>", "Create a new command"]],
                                     self._on_select_command_done)

    def _on_select_command_done(self, index):
        if index == len(self._commands):
            # Ask for a new build command
            self._input_command()
        elif index >= 0:
            # Select the build command and start the build
            self._commands.select(index)
            self._build()

    def _input_command(self):
        self.window.show_input_panel("Build Command:", self._commands.get_latest(),
                                     self._on_input_command_done,
                                     None, None)

    def _on_input_command_done(self, text):
        """Save the build command and start the build"""
        self._commands.add(text)
        self._build()

    def _build(self):
        print("Command: %s : %s" % (self._commands.get_latest(), self._kwds))
        args = dict(self._kwds)
        args["cmd"] = self._commands.get_latest()
        self.window.run_command("exec", args)

class HistoryList(list):
    def __init__(self, name):
        self._name = name
        self._settings = sublime.load_settings(_SETTINGS_FILENAME)
        list.__init__(self, self._settings.get(self._name, []))

    def _save(self):
        self._settings.set(self._name, self)
        sublime.save_settings(_SETTINGS_FILENAME)

    def add(self, item):
        """Add the item to the top of the list, removing any existing copies"""
        while item in self:
            self.pop(self.index(item))
        self.insert(0, item)
        self._save()

    def select(self, index):
        """Move the specified index to the top of the list"""
        self.add(self[index])

    def get_latest(self, default=""):
        """Return the first element of the list"""
        if len(self):
            return self[0]
        else:
            return default

class OldCustomBuilderPromptCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwds):
        self._working_dirs = HistoryList("working_dirs")
        self._commands = HistoryList("commands")
        self._kwds = {}

        sublime_plugin.WindowCommand.__init__(self, *args, **kwds)

    def run(self, **kwds):
        self._kwds = kwds
        self._select_working_dir()

    def _select_working_dir(self):
        self.window.show_quick_panel(["Working Dir: %s" % dir for dir in self._working_dirs + ["<Other>"]],
                                     self._on_select_working_dir_done)

    def _on_select_working_dir_done(self, index):
        if index == len(self._working_dirs):
            # Ask for a new working directory
            self._input_working_dir()
        elif index >= 0:
            # Select the working dir and ask for a build command
            self._working_dirs.select(index)
            # Can't chain Quick Panels directly - use a short timeout
            sublime.set_timeout(lambda: self._select_command(), 1)

    def _input_working_dir(self):
        self.window.show_input_panel("Working Directory:", self._working_dirs.get_latest(),
                                     self._on_input_working_dir_done,
                                     None, None)

    def _on_input_working_dir_done(self, text):
        # Add the working dir to the top of the list and ask for a build command
        self._working_dirs.add(text)
        self._select_command()

    def _select_command(self):
        self.window.show_quick_panel(["Command: %s" % dir for dir in self._commands + ["<Other>"]],
                                     self._on_select_command_done)

    def _on_select_command_done(self, index):
        if index == len(self._commands):
            # Ask for a new build command
            self._input_command()
        elif index >= 0:
            # Select the build command and start the build
            self._commands.select(index)
            self._build()

    def _input_command(self):
        self.window.show_input_panel("Build Command:", self._commands.get_latest(),
                                     self._on_input_command_done,
                                     None, None)

    def _on_input_command_done(self, text):
        """Save the build command and start the build"""
        self._commands.add(text)
        self._build()

    def _build(self):
        print("Command: %s : %s : %s" % (self._working_dirs.get_latest(), self._commands.get_latest(), self._kwds))
