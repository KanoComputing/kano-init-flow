#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# drag_and_drop.py


from gi.repository import Gtk, Gdk, GdkPixbuf
import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if dir_path != '/usr':
        sys.path.append(dir_path)

from kano_tutorial.data import get_data
from kano_tutorial.tutorial_template import TutorialTemplate

data_3 = get_data(3)
data_4 = get_data(4)


class Judoka(Gtk.Fixed):

    def __init__(self):
        Gtk.Fixed.__init__(self)

        label1_text = data_3["LABEL_1"]
        label2_text = data_3["LABEL_2"]
        img_filename = data_3["WORD_JUDOKA_FILENAME"]
        drag_icon_filename = data_3["DRAGGING_JUDOKA_FILENAME"]

        self.width = 500
        self.height = 500
        self.set_size_request(self.width, self.height)

        self.image = Gtk.Image.new_from_file(img_filename)
        self.eventbox = Gtk.EventBox()
        self.eventbox.add(self.image)

        self.label1 = Gtk.Label(label1_text)
        self.label2 = Gtk.Label(label2_text)

        self.put(self.eventbox, 50, 50)
        self.put(self.label1, 50, 300)
        self.put(self.label2, 50, 350)

        self.eventbox.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.ASK)
        # To send image data
        self.eventbox.drag_source_add_image_targets()

        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(drag_icon_filename)

        self.eventbox.connect("drag-begin", self.on_drag_begin)
        self.eventbox.connect("drag-data-get", self.on_drag_data_get)
        self.eventbox.connect("drag-failed", self.on_drag_fail)
        self.eventbox.connect("drag-end", self.on_drag_end)
        self.eventbox.connect("drag-data-delete", self.on_drag_delete)

    def on_drag_begin(self, widget, drag_context):
        print "entered on drag begin"
        # (120, 90) refers to where the cursor relative to the drag icon
        Gtk.drag_set_icon_pixbuf(drag_context, self.pixbuf, 120, 90)
        widget.hide()

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        print "entered on_drag_data_get"
        data.set_pixbuf(self.pixbuf)

    def on_drag_fail(self, drag_context, drag_result, data):
        print "drag failed"
        print data

    def on_drag_end(self, widget, event):
        print "drag ended"
        widget.show()

    def on_drag_delete(self, widget, event):
        print "drag deleted"
        self.image.hide()
        self.label1.hide()
        self.label2.hide()


class DropArea(Gtk.Button):

    def __init__(self):
        Gtk.Button.__init__(self)

        self.width = 500
        self.height = 500
        self.set_size_request(self.width, self.height)

        label1_text = data_4["LABEL_1"]
        label2_text = data_4["LABEL_2"]
        colour_judoka_filename = data_4["COLOUR_JUDOKA_FILENAME"]

        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.ASK)
        targets = Gtk.TargetList.new([])
        targets.add_image_targets(2, True)
        self.drag_dest_set_target_list(targets)

        self.connect("drag-data-received", self.on_drag_data_received)

        self.image = Gtk.Image()
        self.image.set_from_file(colour_judoka_filename)

        self.label1 = Gtk.Label(label1_text)
        self.label2 = Gtk.Label(label2_text)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.pack_start(self.image, False, False, 0)
        self.box.pack_start(self.label1, False, False, 0)
        self.box.pack_start(self.label2, False, False, 0)

        self.add(self.box)

    def hide_image_labels(self):
        self.image.hide()
        self.label1.hide()
        self.label2.hide()

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        print "on_drag_data_received"

        if info == 2:
            self.image.show()
            self.label1.show()
            self.label2.show()
            drag_context.finish(True, True, time)

            # Hacky: get top level window to change keyboard image
            win = self.get_toplevel()
            template = win.get_children()[0]
            template.set_from_level(4)

            self.connect("key-release-event", self.close_application)
            self.grab_focus()

    def close_application(self, widget, event):

        # If ENTER key is pressed
        if event.keyval == 65293:

            # Currently, exit code has no effect, kano-init-flow is launched regardless
            sys.exit(0)


class DragAndDrop(TutorialTemplate):

    def __init__(self, win):
        TutorialTemplate.__init__(self, 3)

        self.win = win
        self.drop_area = DropArea()
        self.judoka = Judoka()

        self.box.pack_start(self.judoka, False, False, 0)
        self.box.pack_start(self.drop_area, False, False, 100)

        self.win.add(self)
        self.win.show_all()
        self.drop_area.hide_image_labels()
