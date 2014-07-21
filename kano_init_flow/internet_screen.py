#!/usr/bin/env python

# internet_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen giving user options for the internet
#

import sys
from template import Template
from update_screen import UpdateScreen
from kano.network import is_internet
import kano_init_flow.constants as constants


class InternetScreen():
    def __init__(self, win):

        self.win = win

        # Check first for internet
        if is_internet():
            self.skip(None, None)
            return

        header = "Connect to the world"
        subheader = "Let's setup Wifi and bring your Kano to life"
        self.template = Template(constants.media + "/connect.png", header, subheader, "CONNECT", "No Internet")

        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.get_orange_button().connect("button_release_event", self.skip)
        self.win.show_all()

    def activate(self, widget, event):
        exit_code = self.template.exit_codes["launch_wifi"]
        sys.exit(exit_code)

    def skip(self, widget, event):
        UpdateScreen(self.win)
