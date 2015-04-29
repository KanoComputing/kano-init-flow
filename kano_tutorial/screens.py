#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# screens.py


from gi.repository import Gtk, Gdk
import os

from kano_tutorial.data import get_data
from kano_tutorial.drag_and_drop import DragAndDrop
from kano_tutorial.tutorial_template import TutorialTemplate
from kano_tutorial.paths import media_dir
from kano.gtk3.cursor import attach_cursor_events


class ButtonTemplate(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)

        self.get_style_context().add_class("drag_source")

        self.width = Gdk.Screen.width()
        self.height = Gdk.Screen.height() / 2
        self.set_size_request(self.width, self.height)

        # Container for the elements in the box

        self.image = Gtk.Image()

        self.label1 = Gtk.Label()
        self.label1.get_style_context().add_class("drag_source_label")
        self.label2 = Gtk.Label()
        self.label2.get_style_context().add_class("drag_source_label_bold")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.box.pack_start(self.image, False, False, 0)
        self.box.pack_start(self.label1, False, False, 0)
        self.box.pack_start(self.label2, False, False, 0)

        align = Gtk.Alignment(xscale=0, yscale=0, xalign=0.5, yalign=0.5)
        align.add(self.box)
        align.set_size_request(self.width, self.height)

        self.add(align)

    def set_level(self, level):
        data = get_data(level)
        filename = os.path.join(media_dir, data["JUDOKA_FILENAME"])
        label1_text = data["LABEL_1"]
        label2_text = data["LABEL_2"]
        self.image.set_from_file(filename)
        self.label1.set_text(label1_text)
        self.label2.set_text(label2_text)


class Screen1(TutorialTemplate):

    def __init__(self, win):
        TutorialTemplate.__init__(self, 1)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_level(1)
        top.connect("key-release-event", self.next)
        self.win.connect("map-event", self.set_cursor_invisible)

        self.box.pack_start(top, False, False, 0)
        top.grab_focus()
        self.win.show_all()

    def set_cursor_invisible(self, widget=None, event=None):
        blank_cursor = Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR)
        self.win.get_window().set_cursor(blank_cursor)

    def next(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Tab":
            self.win.clear_win()
            Screen2(self.win)


class Screen2(TutorialTemplate):
    def __init__(self, win):
        TutorialTemplate.__init__(self, 2)

        self.win = win
        self.win.add(self)

        self.window_event_handler = self.win.connect(
            "button-release-event", self.next
        )

        top = ButtonTemplate()
        top.set_level(2)

        self.set_cursor_visible()

        self.box.add(top)
        top.grab_focus()
        self.win.show_all()

    def set_cursor_visible(self):
        self.win.get_window().set_cursor(None)

    def next(self, widget, event):

        # left click the widget
        if event.button == 1:
            self.win.clear_win()

            # Disconnect the event listener
            self.win.disconnect(self.window_event_handler)
            Screen3(self.win)


class Screen3(TutorialTemplate):
    def __init__(self, win):
        TutorialTemplate.__init__(self, 3)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_level(3)
        top.connect("button-release-event", self.next)
        attach_cursor_events(top)

        self.box.pack_start(top, False, False, 0)
        self.win.show_all()

    def next(self, widget, event):

        # left click the widget
        if event.button == 1:

            self.win.clear_win()
            Screen4(self.win)


class Screen4(TutorialTemplate):
    def __init__(self, win):
        TutorialTemplate.__init__(self, 4)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_level(4)

        self.window_event_handler = self.win.connect(
            "button-release-event", self.next
        )

        self.box.add(top)
        top.grab_focus()
        self.win.show_all()

    def next(self, widget, event):

        # left click the widget
        if event.button == 1:

            self.win.clear_win()

            # Disconnect the event listener
            self.win.disconnect(self.window_event_handler)
            DragAndDrop(self.win)
