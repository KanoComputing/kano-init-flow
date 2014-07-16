#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# screens.py


from gi.repository import Gtk
import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if dir_path != '/usr':
        sys.path.append(dir_path)

from kano_tutorial.data import get_data
from kano_tutorial.drag_and_drop import DragAndDrop
from kano_tutorial.tutorial_template import TutorialTemplate


class ButtonTemplate(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)

        # Container for the elements in the box
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.image = Gtk.Image()
        self.heading = Gtk.Label()
        self.description = Gtk.Label()

        self.box.pack_start(self.image, False, False, 0)
        self.box.pack_start(self.heading, False, False, 0)
        self.box.pack_start(self.description, False, False, 0)

        self.add(self.box)

    def set_level(self, level):
        data = get_data(level)
        text1 = data["LABEL_1"]
        text2 = data["LABEL_2"]
        filename = data["JUDOKA_FILENAME"]

        self.heading.set_text(text1)
        self.description.set_text(text2)

        self.image.set_from_file(filename)


class Screen1(TutorialTemplate):
    def __init__(self, win):
        TutorialTemplate.__init__(self, 1)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_level(1)
        top.connect("button-release-event", self.next)

        self.box.add(top)
        self.win.show_all()

    def next(self, widget, event):
        self.win.clear_win()
        Screen2(self.win)


class Screen2(TutorialTemplate):
    def __init__(self, win):
        TutorialTemplate.__init__(self, 2)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_level(2)
        top.connect("key-release-event", self.next)

        self.box.add(top)
        top.grab_focus()
        self.win.show_all()

    def next(self, widget, event):
        # if ENTER key is pressed
        if event.keyval == 65293:
            self.win.clear_win()
            DragAndDrop(self.win)
