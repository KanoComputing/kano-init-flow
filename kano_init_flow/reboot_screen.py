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


class RebootScreen():
    def __init__(self, win):

        self.win = win
        header = "Time to reboot"
        subheader = "To finish setup, we just have to do a quick reboot. Don't worry! Everything is saved"
        self.template = Template(None, header, subheader, "REBOOT", "")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.show_all()

    def activate(self, widget, event):

        # Exit
        exit_code = self.template.exit_codes["launch_profile"]
        sys.exit(exit_code)
