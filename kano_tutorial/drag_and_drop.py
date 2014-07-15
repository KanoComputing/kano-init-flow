#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#


from gi.repository import Gtk, Gdk, GdkPixbuf
import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if dir_path != '/usr':
        sys.path.append(dir_path)


class Judoka(Gtk.EventBox):

    def __init__(self, img_filename, action=Gdk.DragAction.ASK):
        Gtk.EventBox.__init__(self)

        self.width = 500
        self.height = 500
        self.set_size_request(self.width, self.height)

        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], action)

        self.action = action

        self.image = Gtk.Image.new_from_file(img_filename)
        self.add(self.image)

        # To send image data
        self.drag_source_add_image_targets()

        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_filename)

        self.connect("drag-begin", self.on_drag_begin)
        self.connect("drag-data-get", self.on_drag_data_get)
        self.connect("drag-failed", self.on_drag_fail)
        self.connect("drag-end", self.on_drag_end)
        self.connect("drag-data-delete", self.on_drag_delete)

    def on_drag_begin(self, widget, drag_context):
        print "entered on drag begin"
        Gtk.drag_set_icon_pixbuf(drag_context, self.pixbuf, 120, 90)
        if self.action == Gdk.DragAction.ASK:
            widget.hide()

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        print "entered on_drag_data_get"
        data.set_pixbuf(self.pixbuf)

    def on_drag_fail(self, drag_context, drag_result, data):
        print "drag failed"
        print data

    def on_drag_end(self, widget, event):
        print "drag ended"
        self.image.hide()

    def on_drag_delete(self, widget, event):
        print "drag deleted"
        widget.destroy()


class DropArea(Gtk.EventBox):

    def __init__(self):
        Gtk.EventBox.__init__(self)

        self.width = 500
        self.height = 500
        self.set_size_request(self.width, self.height)

        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY | Gdk.DragAction.ASK)
        targets = Gtk.TargetList.new([])
        targets.add_image_targets(2, True)
        self.drag_dest_set_target_list(targets)

        self.connect("drag-data-received", self.on_drag_data_received)

        self.image = Gtk.Image()
        self.image.set_from_file("judoka_1.png")

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        print "on_drag_data_received"

        if info == 2:
            self.add(self.image)
            self.image.show()
            drag_context.finish(False, False, time)


# Window class
class MainWindow(Gtk.Window):

    def __init__(self, stage=0):

        WINDOW_WIDTH = 900
        WINDOW_HEIGHT = 500

        # Create main window
        Gtk.Window.__init__(self, title="Kano")
        self.set_decorated(False)
        self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.connect("delete-event", Gtk.main_quit)

        self.drop_area = DropArea()
        self.judoka = Judoka("judoka_2.png")

        self.box = Gtk.Box()
        self.box.pack_start(self.judoka, False, False, 0)
        self.box.pack_start(self.drop_area, False, False, 100)

        self.add(self.box)


def main():
    win = MainWindow()
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
