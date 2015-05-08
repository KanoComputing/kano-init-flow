#!/usr/bin/env python

# display_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen for configuring display
#

import os
from gi.repository import Gdk

import kano.gtk3.kano_dialog as kano_dialog
from kano_settings.system.wallpaper import change_wallpaper
from kano.utils import is_monitor, run_cmd
from kano_settings.system.display import get_overscan_status, \
    write_overscan_values, set_overscan_status

from kano_init_flow.template import Template
from kano_init_flow.paths import MEDIA_DIR


WALLPAPER_PATH = "/usr/share/kano-desktop/wallpapers/"
OVERSCAN_PIPE = "/dev/mailbox"


class DisplayScreen(object):

    def __init__(self, _win):

        self.win = _win
        # check for monitor
        if is_monitor():
            self.win.exit_flow()
            return

        self.win.set_resizable(True)

        # Change background
        change_wallpaper(MEDIA_DIR, "/Display-Test")
        # Create UI
        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "display_test.png"),
            title="Can you see four white lines?",
            description="They should be touching each side of your screen.",
            button1_text="YES",
            button2_text="NO"
        )
        self.template.kano_button2.set_color("red")
        self.template.kano_button.connect("button_release_event",
                                          self.next_screen)
        self.template.kano_button.connect("key_release_event",
                                          self.next_screen)
        self.template.kano_button2.connect("button_release_event",
                                           self.tutorial_screen)
        self.template.kano_button2.connect("key_release_event",
                                           self.tutorial_screen)
        self.win.set_main_widget(self.template)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def tutorial_screen(self, _, event):
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            self.win.clear_win()
            DisplayTutorial(self.win)

    def next_screen(self, _, event):
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            # Restore background
            change_wallpaper(WALLPAPER_PATH, "kanux-default")
            self.win.exit_flow()


class DisplayTutorial(object):
    overscan_values = None
    original_overscan = None
    inc = 1

    def __init__(self, _win):

        self.win = _win

        # Launch pipeline
        if not os.path.exists(OVERSCAN_PIPE):
            run_cmd('mknod {} c 100 0'.format(OVERSCAN_PIPE))
        # Get current overscan
        self.original_overscan = get_overscan_status()
        self.overscan_values = get_overscan_status()
        # Listen for key events
        self.win.connect("key-press-event", self.on_key_press)
        # Create UI
        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "display_test2.png"),
            title="Use UP and DOWN keys",
            description="Stretch or shrink your screen, until the white " \
                        "lines are lined up with the edges",
            button1_text="CONTINUE",
            orange_button_text="Reset"
        )
        self.template.kano_button.connect("button_release_event",
                                          self.apply_changes)
        self.template.kano_button.connect("key_release_event",
                                          self.apply_changes)
        self.template.orange_button.connect("button_release_event",
                                            self.reset)
        self.win.set_main_widget(self.template)

        self.template.kano_button.grab_focus()

        self.win.show_all()

    def on_key_press(self, _, event):
        # Up arrow (65362)
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Up:
            self.zoom_out()
            return
        # Down arrow (65364)
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Down:
            self.zoom_in()
            return

    def apply_changes(self, _, event):
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            if self.original_overscan != self.overscan_values:
                # Bring in message dialog box
                kdialog = kano_dialog.KanoDialog(
                    "Are you sure you want to set this screen size?",
                    "",
                    {
                        "OK": {
                            "return_value": -1
                        },
                        "CANCEL": {
                            "return_value": 0
                        }
                    },
                    parent_window=self.win
                )
                response = kdialog.run()
                if response == 0:
                    return
                # Apply changes
                write_overscan_values(self.overscan_values)
            # Next screen
            self.go_to_next()

    def reset(self, *_):
        # Restore overscan if any
        if self.original_overscan != self.overscan_values:
            self.overscan_values = self.original_overscan
            set_overscan_status(self.original_overscan)

    def go_to_next(self):
        # Restore background
        change_wallpaper(WALLPAPER_PATH, "kanux-default")
        self.win.exit_flow()

    def _change_overscan(self, change):
        for side, value in self.overscan_values.iteritems():
            # Do allow negative values
            self.overscan_values[side] = max(value + change, 0)

        set_overscan_status(self.overscan_values)

    def zoom_out(self):
        self._change_overscan(self.inc)

    def zoom_in(self):
        self._change_overscan(-self.inc)
