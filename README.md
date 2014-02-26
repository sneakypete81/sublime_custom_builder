sublimeText Custom Builder
======================

Sublime Text plugin to launch customisable build commands. Easily select the command you need each time you build.

Installation
------------

Coming soon to Package Control. In the meantime, install by copying this script into your ```Packages``` folder.

Usage
-----

Create a [build system file](http://docs.sublimetext.info/en/latest/file_processing/build_systems.html). 
To run the custom builder for all Python files, use:
```
   {
       "target": "custom_builder_prompt",
       "selector": "source.python",
   }
```

Now open a file, bring up the Command Palette and type "Build". This should display the Custom Builder selector.

![Empty Custom Builder selector](https://github.com/sneakypete81/images/raw/master/sublime_custom_builder_screenshot_empty.png)

Press Enter to create a new command, and type the command to run. 
To create a command to list the curent directory, type ```dir```.

Now give it a name and press Enter.

That's it, you should see the command output appear in the output pane.

Now when you bring up the Custom Builder selector you will see the new command at the top of the list.

![Custom Builder selector](https://github.com/sneakypete81/images/raw/master/sublime_custom_builder_screenshot_single.png)

Editing Commands
----------------

You can edit your existing commands by opening the ```Custom Builder.sublime-settings``` file in your ```Packages/User``` folder

Build System Variables
----------------------

You can use any of the [Build System Features](http://docs.sublimetext.info/en/latest/reference/build_systems.html) in your build system files.

Unfortunately Build System Variables (```$file_path```, ```$project```, etc.) are not expanded properly by default. To use these in your commands, pass them through in the "cmd" argument:

```
   {
       "target": "custom_builder_prompt",
       "selector": "source.python",
       "cmd": {"file": "$file"},
       "shell": true,
   }
```

You can then use the variable in your Custom Builder command:
```
   dir $file
```
