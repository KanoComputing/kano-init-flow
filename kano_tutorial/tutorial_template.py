#!/usr/bin/env python

# tutorial_template.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Tutorial template, with keyboard at bottom and level specific container at top
#

import os
from gi.repository import Gtk, Gdk, GdkPixbuf
from data import get_data
from kano_tutorial.paths import media_dir


class TutorialTemplate(Gtk.Box):

    def __init__(self, level=1):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.eventbox = Gtk.EventBox()
        width = Gdk.Screen.width() / 2
        height = Gdk.Screen.height() / 2
        self.eventbox.set_size_request(width, height)

        self.keyboard = Gtk.Image()
        self.eventbox.add(self.keyboard)
        self.eventbox.get_style_context().add_class("keyboard")

        self.box = Gtk.Box()
        align = Gtk.Alignment(xscale=0, xalign=0.5)
        align.add(self.box)
        self.pack_start(align, False, False, 0)
        self.pack_start(self.eventbox, False, False, 0)
        self.set_from_level(level)

    def set_from_level(self, level):
        data = get_data(level)
        filename = os.path.join(media_dir, data["KEYBOARD_FILENAME"])
        extension = os.path.splitext(filename)[1]
        if extension == '.gif':
            anim = GdkPixbuf.PixbufAnimation.new_from_file(filename)
            self.keyboard.set_from_animation(anim)
        else:
            self.keyboard.set_from_file(filename)
