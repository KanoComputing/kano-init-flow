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
from kano_init_flow.data import get_data


class SwagScreen():
    data = get_data("SWAG_SCREEN")

    def __init__(self, win):

        self.win = win
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "TO THE DESKTOP")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.show_all()

    def activate(self, widget, event):

        # Exit
        sys.exit(0)
