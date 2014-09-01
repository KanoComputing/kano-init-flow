#!/usr/bin/env python

# reboot_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Shows message before reboot
#

import sys
from template import Template
from kano_init_flow.data import get_data


class RebootScreen():
    data = get_data("REBOOT_SCREEN")

    def __init__(self, win):

        self.win = win
        self.win.shrink()
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(None, header, subheader, "REBOOT")
        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.kano_button.connect("key_release_event", self.activate)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            # Exit
            exit_code = self.template.exit_codes["launch_profile"]
            sys.exit(exit_code)
