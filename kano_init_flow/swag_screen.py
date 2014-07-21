#!/usr/bin/env python

# swag_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# This screen replaces the level up dialogue
#

import sys
from template import Template
import kano_init_flow.constants as constants


class SwagScreen():
    def __init__(self, win):

        self.win = win
        header = "Swag time!"
        subheader = "As you play, you win! You unlocked a new badge, background and levelled up!"
        self.template = Template(constants.media + "/swag.png", header, subheader, "TO THE DESKTOP", "")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.show_all()

    def activate(self, widget, event):

        # Exit
        sys.exit(0)
