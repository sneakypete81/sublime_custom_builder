import sublime, sublime_plugin

_SETTINGS_FILENAME = "Custom Builder.sublime-settings"

class CustomBuilderPromptCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwds):
        self._commands = None
        self._kwds = {}
        self._command_input_text = None

        sublime_plugin.WindowCommand.__init__(self, *args, **kwds)

    def run(self, **kwds):
        self._kwds = kwds
        self._commands = HistoryList("commands")
        self._select_command()

    def _select_command(self):
        """Show the list of defined commands"""
        self.window.show_quick_panel([[cmd["title"], cmd["command"]] for cmd in self._commands] + [["<New>", "Create a new command"]],
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
        """Prompt for a new command"""
        latest = self._commands.get_latest({"command": ""})

        self.window.show_input_panel("Command to Run:", latest["command"],
                                     self._on_input_command_done,
                                     None, None)

    def _on_input_command_done(self, text):
        self._command_input_text = text
        self._input_title()

    def _input_title(self):
        """Prompt for a command title"""
        self.window.show_input_panel("Command Title:", "",
                                     self._on_input_title_done,
                                     None, None)

    def _on_input_title_done(self, text):
        """Save and run the command"""
        self._commands.add({"title": text, "command": self._command_input_text})
        self._command_input_text = None
        self._build()

    def _build(self):
        args = dict(self._kwds)
        command = self._commands.get_latest()["command"]

        # Substitute all variables specified in args["cmd"]
        for var in args.get("cmd", {}):
            command = command.replace("$%s" % var, args["cmd"][var])

        args["cmd"] = command
        self.window.run_command("exec", args)


class HistoryList(list):
    """Maintain a list of objects ordered by 'last used' and saved in the settings file"""
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

    def get_latest(self, default=None):
        """Return the first element of the list"""
        if len(self):
            return self[0]
        else:
            return default
