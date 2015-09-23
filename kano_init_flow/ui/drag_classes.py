#!/usr/bin/env python

# drag_classes.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk
from kano.gtk3.cursor import attach_cursor_events
from kano.logging import logger


# TODO: these need to be moved to a common place, this is duplicate of code
# in the drag and drop screen.
class DragSource(Gtk.EventBox):
    """
    The object which is dragged from the source to the destination.
    """

    # Pass the scaled images into the class
    def __init__(self, image, pixbuf, *hidden_elements):
        Gtk.EventBox.__init__(self)
        attach_cursor_events(self)

        self.image = image
        self.add(image)

        self.hidden_elements = hidden_elements

        # This follows the cursor when the item is being dragged
        self.pixbuf = pixbuf
        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                             Gdk.DragAction.ASK)

        # To send image data
        self.drag_source_add_image_targets()
        self.connect("drag-begin", self.on_drag_begin)
        self.connect("drag-data-get", self.on_drag_data_get)
        self.connect("drag-failed", self.on_drag_fail)
        self.connect("drag-end", self.on_drag_end)
        self.connect("drag-data-delete", self.on_drag_delete)

    def on_drag_begin(self, _, drag_context):
        """ Triggered when dragging starts """

        logger.info("Drag has begun")

        # (120, 90) refers to where the cursor relative to the drag icon
        Gtk.drag_set_icon_pixbuf(drag_context, self.pixbuf, 50, 50)
        self.remove(self.image)

        for element in self.hidden_elements:
            element.hide()

        self.show_all()

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        """ Passes the drag data to the drop area """

        logger.info("Data is sent from source")
        data.set_pixbuf(self.pixbuf)

    @staticmethod
    def on_drag_fail(drag_context, drag_result, data):
        """ Handles when the Judoka isn't dragged to the drop area """

        logger.info("Drag failed")
        logger.info(data)

    def on_drag_end(self, *_):
        """ Triggered when the drag action is terminated """

        logger.info("Drag ended")
        self.add(self.image)

        for element in self.hidden_elements:
            element.show()

        self.show_all()

    def on_drag_delete(self, *_):
        """ Triggered when the drag action is completed successfully """

        logger.info("Drag deleted")
        self.destroy()


class DropArea(Gtk.Button):
    """
    Area which the user has to drag the block into
    """

    def __init__(self, next_cb):
        super(DropArea, self).__init__()

        self.next_cb = next_cb
        self.get_style_context().add_class("drag_dest")

        self.drag_dest_set(
            Gtk.DestDefaults.MOTION | Gtk.DestDefaults.DROP,
            [],
            Gdk.DragAction.ASK
        )

        targets = Gtk.TargetList.new([])
        targets.add_image_targets(2, True)
        self.drag_dest_set_target_list(targets)

        self.connect("drag-data-received", self.on_drag_data_received)

    def on_drag_data_received(self, widget, drag_context, x, y,
                              data, info, time):
        """
        Triggered whenever new drag data is received. If the Judoka
        has been successfully dragged then move on to the next stage
        """

        logger.info("Drop area has received data")
        if info == 2:
            drag_context.finish(True, True, time)
            self.next_cb()
