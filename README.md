sublimeText Custom Builder
======================

Sublime Text plugin to launch customisable build commands. Easily select the command you need each time you build.

Installation
============

Coming soon to Package Control. In the meantime, install by copying this script into your Packages folder.

Usage
=====

1. 
Create a build system file (see http://docs.sublimetext.info/en/latest/file_processing/build_systems.html).
To run the custom builder for all Python files, use:

   {
       "target": "custom_builder_prompt",
       "selector": "source.python",
   }

2.
Now open a file, bring up the Command Palette and type "Build". This should display the Custom Builder selector.

3.
Press <Enter> to create a new command, and type the command to run.
To create a command to list the curent directory:
   
   dir

4.   
Now give it a name and press <Enter>.

5.
That's it, you should see the command output appear in the output pane.

6.
Now when you bring up the Custom Builder selector (step 2) you will see the new command at the top of the list.
