# drag_and_drop.py
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen to teach dragging and dropping by moving an image of the Judoka
# into a specified region
#


from gi.repository import Gtk, Gdk, GdkPixbuf
import os
import sys

from kano_tutorial.tutorial_template import TutorialTemplate
from kano_tutorial.paths import MEDIA_DIR
from kano.logging import logger
from kano.gtk3.cursor import attach_cursor_events


class Judoka(Gtk.EventBox):
    """
    The object which is dragged from the source to the destination.
    """

    def __init__(self):
        Gtk.EventBox.__init__(self)

        self.get_style_context().add_class("drag_source")

        self.width = Gdk.Screen.width() / 2
        self.height = Gdk.Screen.height() / 2
        self.set_size_request(self.width, self.height)

        img_filename = os.path.join(MEDIA_DIR, "judoka-pointing.png")
        self.image = Gtk.Image.new_from_file(img_filename)

        self.eventbox = Gtk.EventBox()
        self.eventbox.add(self.image)
        attach_cursor_events(self.eventbox)

        self.bg_image = Gtk.Image()
        drag_bg_filename = os.path.join(MEDIA_DIR, "judoka-dragged-BG.png")
        self.bg_image.set_from_file(drag_bg_filename)

        self.label1 = Gtk.Label(_("I can show colors too "
                                  "- 16.7 million of them!")
        self.label1.get_style_context().add_class("drag_source_label")
        self.instruction = Gtk.Label(_("Click, hold, and drag "
                                       "me to the color.")
        self.instruction.get_style_context().add_class("drag_source_label_bold")

        # Mimic dimensions of the image so when the image is hidden,
        # event box does not change size
        self.eventbox.set_size_request(291, 350)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.pack_start(self.eventbox, False, False, 0)
        box.pack_start(self.label1, False, False, 0)
        box.pack_start(self.instruction, False, False, 0)

        self.align = Gtk.Alignment(xscale=0, yscale=0, xalign=0.5, yalign=0.5)
        self.align.add(box)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.pack_start(self.align, True, True, 0)
        self.add(self.box)

        self.eventbox.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                                      Gdk.DragAction.ASK)

        # To send image data
        self.eventbox.drag_source_add_image_targets()

        # The pixbuf is to set the dragging icon that follows the mouse
        drag_icon_filename = os.path.join(MEDIA_DIR, "judoka-dragged.png")
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(drag_icon_filename)

        self.eventbox.connect("drag-begin", self.on_drag_begin)
        self.eventbox.connect("drag-data-get", self.on_drag_data_get)
        self.eventbox.connect("drag-failed", self.on_drag_fail)
        self.eventbox.connect("drag-end", self.on_drag_end)
        self.eventbox.connect("drag-data-delete", self.on_drag_delete)

    def on_drag_begin(self, _, drag_context):
        """ Triggered when dragging starts """

        logger.info("Drag has begun")

        # (120, 90) refers to where the cursor relative to the drag icon
        Gtk.drag_set_icon_pixbuf(drag_context, self.pixbuf, 100, 20)
        self.eventbox.remove(self.image)
        self.eventbox.add(self.bg_image)
        self.eventbox.show_all()

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
        self.eventbox.remove(self.bg_image)
        self.eventbox.add(self.image)
        self.eventbox.show_all()

    def on_drag_delete(self, *_):
        """ Triggered when the drag action is completed successfully """

        logger.info("Drag deleted")
        self.eventbox.destroy()
        self.label1.destroy()
        self.instruction.destroy()


class DropArea(Gtk.Button):
    """
    Area which the user has to drag the Judoka into
    """

    def __init__(self):
        Gtk.Button.__init__(self)

        self.get_style_context().add_class("drag_dest")

        self.width = Gdk.Screen.width() / 2
        self.height = Gdk.Screen.height() / 2
        self.set_size_request(self.width, self.height)

        self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.ASK)
        targets = Gtk.TargetList.new([])
        targets.add_image_targets(2, True)
        self.drag_dest_set_target_list(targets)

        self.connect("drag-data-received", self.on_drag_data_received)

        self.colour_judoka_image = Gtk.Image()
        colour_judoka_filename = os.path.join(MEDIA_DIR, "judoka-coloured.png")
        self.colour_judoka_image.set_from_file(colour_judoka_filename)

        self.bullseye = Gtk.Image()
        target_filename = os.path.join(MEDIA_DIR, "bullseye.png")
        self.bullseye.set_from_file(target_filename)

        self.fixed = Gtk.Fixed()
        self.fixed.put(self.bullseye, 0, 0)
        self.fixed.put(self.colour_judoka_image, 0, 0)

        self.label1 = Gtk.Label(_("Nice work, keyboard ninja!"))
        self.label1.get_style_context().add_class("drag_dest_label")
        self.instruction = Gtk.Label(_("Left click to continue."))
        self.instruction.get_style_context().add_class("drag_dest_label_bold")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.fixed, False, False, 0)
        box.pack_start(self.label1, False, False, 0)
        box.pack_start(self.instruction, False, False, 0)

        align = Gtk.Alignment(xscale=0, yscale=0, xalign=0.5, yalign=0.5)
        align.add(box)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.pack_start(align, True, True, 0)

        self.add(self.box)

    def hide_image_labels(self):
        """
        Hide the Judoka image and text. This is until the Judoka
        has been successfully dragged into this window.
        """

        self.colour_judoka_image.hide()
        self.label1.hide()
        self.instruction.hide()

    def on_drag_data_received(self, widget, drag_context, x, y,
                              data, info, time):
        """
        Triggered whenever new drag data is received. If the Judoka
        has been successfully dragged then move on to the next stage
        """

        logger.info("Drop area has recieved data")

        if info == 2:
            self.colour_judoka_image.show()
            self.label1.show()
            self.instruction.show()
            drag_context.finish(True, True, time)

            # Hacky: get top level window to change keyboard image
            win = self.get_toplevel()
            template = win.get_children()[0]
            keyboard_image = os.path.join(MEDIA_DIR, "keyboard-left-click.gif")
            template.set_image(img_path=keyboard_image)

            win.connect("button-release-event", self.close_application)
            self.connect("button-release-event", self.close_application)
            self.grab_focus()

    @staticmethod
    def close_application(_, event):
        """ Exit """

        # left click
        if event.button == 1:
            # Currently, exit code has no effect,
            # kano-init-flow is launched regardless
            sys.exit(0)


class DragAndDrop(TutorialTemplate):
    """
    Screen to teach dragging and dropping.
    Requires the user to click and drag the Judoka into the drop area
    """

    def __init__(self, win):
        img_path = os.path.join(MEDIA_DIR, "keyboard-clickandhold.gif")
        TutorialTemplate.__init__(self, img_path=img_path)

        self.win = win
        self.drop_area = DropArea()
        self.judoka = Judoka()

        self.box.pack_start(self.judoka, False, False, 0)
        self.box.pack_start(self.drop_area, False, False, 0)

        self.win.add(self)
        self.win.show_all()
        self.drop_area.hide_image_labels()
