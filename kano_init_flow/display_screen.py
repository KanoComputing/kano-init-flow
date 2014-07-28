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
from kano_settings.set_display.functions import get_overscan_status, write_overscan_values, set_overscan_status
import kano.gtk3.kano_dialog as kano_dialog

kdeskrc_home = "/home/%s/.kdeskrc"
wallpaper_path = "/usr/share/kano-desktop/wallpapers/"
overscan_pipe = "/var/tmp/overscan"


def change_wallpaper(path, name):
    # home directory
    USER = os.environ['SUDO_USER']
    deskrc_path = kdeskrc_home % (USER)
    # Wallpaper selected
    image_169 = "%s%s-16-9.png" % (path, name)
    image_43 = "%s%s-4-3.png" % (path, name)
    image_1024 = "%s%s-1024.png" % (path, name)
    # Look for the strings
    found = False
    if os.path.isfile(deskrc_path):
        f = open(deskrc_path, 'r')
        newlines = []
        for line in f:
            if "Background.File-medium:" in line:
                line = "  Background.File-medium: %s\n" % (image_1024)
                found = True
            elif "Background.File-4-3:" in line:
                line = "  Background.File-4-3: %s\n" % (image_43)
            elif "Background.File-16-9:" in line:
                line = "  Background.File-16-9: %s\n" % (image_169)
            newlines.append(line)
        f.close()
    if found:
        # Overwrite config file with new lines
        outfile = open(deskrc_path, 'w')
        outfile.writelines(newlines)
        outfile.close()
    # If not found add it
    else:
        with open(deskrc_path, "a") as outfile:
            outfile.write("  Background.File-medium: %s\n" % (image_1024))
            outfile.write("  Background.File-4-3: %s\n" % (image_43))
            outfile.write("  Background.File-16-9: %s\n" % (image_169))
    # Refresh the wallpaper
    cmd = 'sudo -u %s kdesk -w' % USER
    os.system(cmd)
    return 0


class DisplayScreen():
    data = get_data("DISPLAY_SCREEN")

    def __init__(self, _win):

        self.win = _win

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
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "YES", "NO")
        self.template.kano_button.connect("button_release_event", self.next_screen)
        self.template.orange_button.connect("button_release_event", self.tutorial_screen)
        self.win.add(self.template)

        self.win.show_all()

    def tutorial_screen(self, widget, event):
        self.win.clear_win()
        DisplayTutorial(self.win)

    def next_screen(self, widget, event):
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
        subheader = ""
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "CONTINUE", "Skip")
        self.template.kano_button.connect("button_release_event", self.apply_changes)
        self.template.orange_button.connect("button_release_event", self.skip)
        self.win.add(self.template)

        self.win.show_all()

    def on_key_press(self, widget, event):
        # Right arrow (65363)
        if not hasattr(event, 'keyval') or event.keyval == 65363:
            self.zoom_out()
            return
        # Left arrow (65361)
        if not hasattr(event, 'keyval') or event.keyval == 65361:
            self.zoom_in()
            return

    def apply_changes(self, widget, event):
        if self.original_overscan != self.overscan_values:
            # Bring in message dialog box
            kdialog = kano_dialog.KanoDialog(
                "Are you sure you want to apply changes?",
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

    def skip(self, widget, event):
        # Restore overscan if any
        if self.original_overscan != self.overscan_values:
            set_overscan_status(self.original_overscan)
        # Next screen
        self.go_to_next()

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
        self.overscan_values['top'] -= self.inc
        self.overscan_values['bottom'] -= self.inc
        self.overscan_values['left'] -= self.inc
        self.overscan_values['right'] -= self.inc
        set_overscan_status(self.overscan_values)
