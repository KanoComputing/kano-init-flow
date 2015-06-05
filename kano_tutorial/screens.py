# screens.py
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screens for the tutorial
#


from gi.repository import Gtk, Gdk
import os

from kano_tutorial.drag_and_drop import DragAndDrop
from kano_tutorial.tutorial_template import TutorialTemplate
from kano_tutorial.paths import MEDIA_DIR
from kano.gtk3.cursor import attach_cursor_events


class ButtonTemplate(Gtk.Button):
    """
    Base class for instruction widgets
    """

    def __init__(self):
        Gtk.Button.__init__(self)

        self.get_style_context().add_class("drag_source")

        self.width = Gdk.Screen.width()
        self.height = Gdk.Screen.height() / 2
        self.set_size_request(self.width, self.height)

        # Container for the elements in the box

        self.image = Gtk.Image()

        self.label = Gtk.Label()
        self.label.get_style_context().add_class("drag_source_label")
        self.instruction = Gtk.Label()
        self.instruction.get_style_context().add_class("drag_source_label_bold")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.box.pack_start(self.image, False, False, 0)
        self.box.pack_start(self.label, False, False, 0)
        self.box.pack_start(self.instruction, False, False, 0)

        align = Gtk.Alignment(xscale=0, yscale=0, xalign=0.5, yalign=0.5)
        align.add(self.box)
        align.set_size_request(self.width, self.height)

        self.add(align)

    def set_content(self, img_path, label, instruction):
        """ Fill the widget with the desired content """

        self.image.set_from_file(img_path)
        self.label.set_text(label)
        self.instruction.set_text(instruction)


class Screen1(TutorialTemplate):
    """
    Screen to activate the mouse
    """

    def __init__(self, win):
        img_path = os.path.join(MEDIA_DIR, "keyboard-tab.gif")
        TutorialTemplate.__init__(self, img_path=img_path)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()

        top.set_content(
            img_path=os.path.join(MEDIA_DIR, "mouse-dotted.png"),
            label=_("We escaped!  Now let's turn on new powers!  "
                    "First - the mouse."),
            instruction=_("Press [tab] to activate the mouse.")
        )

        top.connect("key-release-event", self.next)
        self.win.connect("map-event", self.set_cursor_invisible)

        self.box.pack_start(top, False, False, 0)
        top.grab_focus()
        self.win.show_all()

    def set_cursor_invisible(self, *_):
        blank_cursor = Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR)
        self.win.get_window().set_cursor(blank_cursor)

    def next(self, _, event):
        """ Go to the next screen """
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Tab":
            self.win.clear_win()
            Screen2(self.win)


class Screen2(TutorialTemplate):
    """
    Screen to teach left click
    """

    def __init__(self, win):
        img_path = os.path.join(MEDIA_DIR, "keyboard-left-click.gif")
        TutorialTemplate.__init__(self, img_path=img_path)

        self.win = win
        self.win.add(self)

        self.window_event_handler = self.win.connect(
            "button-release-event", self.next
        )

        top = ButtonTemplate()
        top.set_content(
            img_path=os.path.join(MEDIA_DIR, "mouse-filled.png"),
            label=_("Nice! You can move the mouse with the touchpad."),
            instruction=_("Left click to continue.")
        )
        top.connect('button-release-event', self.next)

        self.set_cursor_visible()

        self.box.add(top)
        top.grab_focus()
        self.win.show_all()

    def set_cursor_visible(self):
        self.win.get_window().set_cursor(None)

    def next(self, _, event):
        """ Go to the next screen """

        # left click the widget
        if event.button == 1:
            self.win.clear_win()

            # Disconnect the event listener
            self.win.disconnect(self.window_event_handler)
            Screen3(self.win)


class Screen3(TutorialTemplate):
    """
    Reinforce left click by righting the Judoka
    """

    def __init__(self, win):
        img_path = os.path.join(MEDIA_DIR, "keyboard-click.gif")
        TutorialTemplate.__init__(self, img_path=img_path)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_content(
            img_path=os.path.join(MEDIA_DIR, "judoka-hanging.png"),
            label=_("But wait, I'm upside down!  Click me to flip me over!"),
            instruction=_("Left click the Judoka.")
        )
        top.connect("button-release-event", self.next)
        attach_cursor_events(top)

        self.box.pack_start(top, False, False, 0)
        self.win.show_all()

    def next(self, _, event):
        """ Go to the next screen """

        # left click the widget
        if event.button == 1:

            self.win.clear_win()
            Screen4(self.win)


class Screen4(TutorialTemplate):
    """
    Reinforce left click again by requiring clicking
    """

    def __init__(self, win):
        img_path = os.path.join(MEDIA_DIR, "keyboard-left-click.gif")
        TutorialTemplate.__init__(self, img_path=img_path)

        self.win = win
        self.win.add(self)

        top = ButtonTemplate()
        top.set_content(
            img_path=os.path.join(MEDIA_DIR, "judoka-fixed.png"),
            label=_("Wow thanks - you flipped me! Good mouse-work."),
            instruction=_("Left click to continue.")
        )
        top.connect('button-release-event', self.next)

        self.window_event_handler = self.win.connect(
            "button-release-event", self.next
        )

        self.box.add(top)
        top.grab_focus()
        self.win.show_all()

    def next(self, _, event):
        """ Go to the next screen """

        # left click the widget
        if event.button == 1:

            self.win.clear_win()

            # Disconnect the event listener
            self.win.disconnect(self.window_event_handler)
            DragAndDrop(self.win)
