#!/usr/bin/env python
#
# hal-example: A brief example of a stand-alone GUI application that
#     interfaces with the LinuxCNC HAL.
#
# Copyright (C) 2016 Sebastian Kuzminsky
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GLib

import hal


class HAL_Example:
    """This class is just a container data structure to keep track of
    all the GUI widgets and the HAL handle."""


    def __init__(self):
        """This init function runs when you create an object of the
        HAL_Example type.  It builds a Gtk window with some widgets in
        it, and it connects to HAL and makes some pins."""

        window = Gtk.Window()
        window.set_title('HAL is awesome')
        window.connect('destroy', self.destroy)

        main_box = Gtk.Box()
        main_box.set_spacing(20)
        main_box.set_orientation(Gtk.Orientation.VERTICAL)
        window.add(main_box)

        self.button = Gtk.ToggleButton('Button')
        self.button.set_active(False)
        self.button.connect('toggled', self.button_toggled)
        main_box.add(self.button)

        self.led_label = Gtk.Label()
        main_box.add(self.led_label)

        self.count_label = Gtk.Label()
        main_box.add(self.count_label)

        # register ourselves as a HAL component
        self.hal = hal.component("hal-example")
        self.hal.setprefix("hal-example")

        # create pins
        # a positive edge on the "increment" input increases the value on the "count" output
        self.hal.newpin('increment', hal.HAL_BIT, hal.HAL_IN)
        self.old_increment = self.hal['increment']

        self.hal.newpin('count', hal.HAL_S32, hal.HAL_OUT)

        self.hal.newpin('button', hal.HAL_BIT, hal.HAL_OUT)
        self.hal['button'] = self.button.get_active()

        # we're done creating pins, make this component visible to the rest of HAL
        self.hal.ready()

        # Call the update function to read the HAL input pins, do all
        # our internal thinking, and update the GUI window and the HAL
        # output pins.
        self.update()

        # schedule the timeout handler to run 100 ms from now
        GLib.timeout_add(100, self.timeout_handler)

        # Show the window on the user's screen.
        window.show_all()


    def button_toggled(self, button):
        """This function gets connected to the "toggled" signal of the
        button widget in the GUI.  It runs whenever the user clicks
        the button.  It just reads the new button state from the GUI
        and puts it on the corresponding HAL pin."""

        # copy the gtk button widget state to the matching hal pin
        self.hal['button'] = button.get_active()


    def destroy(self, window):
        """This function gets connected to the "destroyed" signal of
        the GUI window.  It runs when the user kills the window."""

        Gtk.main_quit()


    def timeout_handler(self):
        """This function is a one-shot timeout handler.  It calls update()
        to synchronize the GUI and HAL, and it re-schedules itself to
        run again later."""

        # synchronize GUI and HAL
        self.update()

        # schedule this timeout handler to run again, another 100 ms from now
        GLib.timeout_add(100, self.timeout_handler)


    def update(self):
        """This function reads all the HAL pins, runs our internal logic,
        and updates the GUI widgets and HAL output pins."""

        if self.hal['increment']:
            self.led_label.set_label('TRUE')
        else:
            self.led_label.set_label('FALSE')

        # if there is a positive edge on the 'increment' pin, then increment the count
        if self.hal['increment'] and not self.old_increment:
            self.hal['count'] = self.hal['count'] + 1

        self.old_increment = self.hal['increment']

        self.count_label.set_markup('<b>Count:</b> %4d' % self.hal['count'])


def main():
    app = HAL_Example()
    Gtk.main()


if __name__ == '__main__':
    main()
