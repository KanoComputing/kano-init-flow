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


class InternetScreen():
    def __init__(self, win):

        self.win = win
        self.template = Template("../media/images/image_2.png", "Connect to the world",
                                 "Let's setup Wifi and bring your Kano to life", "CONNECT", "LATER")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.orange_button.connect("button_release_event", self.skip)
        self.win.show_all()

    def activate(self, widget, event):
        exit_code = self.template.exit_codes["launch_wifi"]
        sys.exit(exit_code)

    def skip(self, widget, event):
        self.win.clear_win()
        UpdateScreen(self.win)
