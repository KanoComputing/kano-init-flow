#!/usr/bin/env python

# display_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen for configuring display
#

import os
from template import Template
from kano.utils import is_monitor, run_cmd
from kano_init_flow.reboot_screen import RebootScreen
from kano_init_flow.data import get_data
import kano_init_flow.constants as constants
from kano_settings.system.display import get_overscan_status, write_overscan_values, set_overscan_status
from kano_settings.set_wallpaper import change_wallpaper
import kano.gtk3.kano_dialog as kano_dialog

from gi.repository import Gdk

kdeskrc_home = "/home/%s/.kdeskrc"
wallpaper_path = "/usr/share/kano-desktop/wallpapers/"
overscan_pipe = "/dev/mailbox"


class DisplayScreen():
    data = get_data("DISPLAY_SCREEN")

    def __init__(self, _win):

        self.win = _win
        self.win.set_resizable(True)

        # check for monitor
        if is_monitor():
            # Go to next screen
            self.win.clear_win()
            RebootScreen(self.win)
            return

        # Change background
        change_wallpaper(constants.media, "/Display-Test")
        # Create UI
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "YES", button2_text="NO")
        self.template.kano_button2.set_color("red")
        self.template.kano_button.connect("button_release_event", self.next_screen)
        self.template.kano_button.connect("key_release_event", self.next_screen)
        self.template.kano_button2.connect("button_release_event", self.tutorial_screen)
        self.template.kano_button2.connect("key_release_event", self.tutorial_screen)
        self.win.set_main_widget(self.template)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def tutorial_screen(self, widget, event):
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            self.win.clear_win()
            DisplayTutorial(self.win)

    def next_screen(self, widget, event):
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:

            # Restore background
            change_wallpaper(wallpaper_path, "kanux-background")

            # Go to next screen
            self.win.clear_win()
            RebootScreen(self.win)


class DisplayTutorial():
    data = get_data("DISPLAY_TUTORIAL")
    overscan_values = None
    original_overscan = None
    inc = 1

    def __init__(self, _win):

        self.win = _win

        # Launch pipeline
        if not os.path.exists(overscan_pipe):
            run_cmd('mknod {} c 100 0'.format(overscan_pipe))
        # Get current overscan
        self.original_overscan = get_overscan_status()
        self.overscan_values = get_overscan_status()
        # Listen for key events
        self.win.connect("key-press-event", self.on_key_press)
        # Create UI
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "CONTINUE", orange_button_text="Reset")
        self.template.kano_button.connect("button_release_event", self.apply_changes)
        self.template.kano_button.connect("key_release_event", self.apply_changes)
        self.template.orange_button.connect("button_release_event", self.reset)
        self.win.set_main_widget(self.template)

        self.template.kano_button.grab_focus()

        self.win.show_all()

    def on_key_press(self, widget, event):
        # Up arrow (65362)
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Up:
            self.zoom_out()
            return
        # Down arrow (65364)
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Down:
            self.zoom_in()
            return

    def apply_changes(self, widget, event):
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

    def reset(self, widget, event):
        # Restore overscan if any
        if self.original_overscan != self.overscan_values:
            self.overscan_values = self.original_overscan
            set_overscan_status(self.original_overscan)

    def go_to_next(self):
        # Restore background
        change_wallpaper(wallpaper_path, "kanux-background")
        # Go to next screen
        self.win.clear_win()
        RebootScreen(self.win)

    def zoom_out(self):
        self.overscan_values['top'] += self.inc
        self.overscan_values['bottom'] += self.inc
        self.overscan_values['left'] += self.inc
        self.overscan_values['right'] += self.inc
        set_overscan_status(self.overscan_values)

    def zoom_in(self):
        # Do not go into negative values
        if self.overscan_values['top'] > 0:
            self.overscan_values['top'] -= self.inc
            self.overscan_values['bottom'] -= self.inc
            self.overscan_values['left'] -= self.inc
            self.overscan_values['right'] -= self.inc
            set_overscan_status(self.overscan_values)
