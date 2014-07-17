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
from kano_tutorial.paths import media_dir


class ButtonTemplate(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)

        self.get_style_context().add_class("drag_source")
        self.set_size_request(1024, 450)

        # Container for the elements in the box
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.image = Gtk.Image()
        align_image = Gtk.Alignment()
        align_image.set_padding(40, 10, 0, 0)
        align_image.add(self.image)
        self.label1 = Gtk.Label()
        self.label1.get_style_context().add_class("drag_source_label")
        self.label2 = Gtk.Label()
        self.label2.get_style_context().add_class("drag_source_label")
        self.label3 = Gtk.Label()
        self.label3.get_style_context().add_class("drag_source_label_bold")

        self.box.pack_start(align_image, False, False, 0)
        self.box.pack_start(self.label1, False, False, 0)
        self.box.pack_start(self.label2, False, False, 0)
        self.box.pack_start(self.label3, False, False, 0)

        self.add(self.box)

    def set_level(self, level):
        data = get_data(level)
        filename = os.path.join(media_dir, data["JUDOKA_FILENAME"])
        label1_text = data["LABEL_1"]
        label2_text = data["LABEL_2"]
        label3_text = data["LABEL_3"]
        self.image.set_from_file(filename)
        self.label1.set_text(label1_text)
        self.label2.set_text(label2_text)
        self.label3.set_text(label3_text)


class Screen1(TutorialTemplate):
    def __init__(self, win):
        TutorialTemplate.__init__(self, 1)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_level(1)
        top.connect("button-release-event", self.next)

        self.box.pack_start(top, False, False, 0)
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
