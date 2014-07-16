#!/usr/bin/env python

# tutorial_template.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Tutorial template, with keyboard at bottom and level specific container at top
#

from gi.repository import Gtk
from kano_tutorial.data import get_data


class TutorialTemplate(Gtk.Box):

    def __init__(self, level=0):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.keyboard = Gtk.Image()
        self.box = Gtk.Box()
        self.pack_start(self.box, False, False, 0)
        self.pack_start(self.keyboard, False, False, 0)
        self.set_from_level(level)

    def set_from_level(self, level):
        data = get_data(level)
        filename = data["KEYBOARD_FILENAME"]
        self.keyboard.set_from_file(filename)
