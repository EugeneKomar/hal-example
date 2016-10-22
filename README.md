hal-example: A brief example of a stand-alone GUI application that
    interfaces with the LinuxCNC HAL.

This program runs on any computer with linuxcnc, python, and python-gi
installed.

Run this:

    > halrun -I hal-example.hal

That will start HAL, run the hal-example.py program, and put you in a
halcmd shell.  When you are done, kill the GUI window and exit halcmd.
