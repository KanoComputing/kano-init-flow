#!/usr/bin/env python

# first_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Intro screen of the first boot
#

from template import Template
from internet_screen import InternetScreen
import kano_init_flow.constants as constants


class FirstScreen():
    def __init__(self, win):

        self.win = win
        header = "We made it!"
        subheader = "You made a computer - now let's give it new powers!"
        self.template = Template(constants.media + "/made_it.png", header, subheader, "START SETUP", "")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.show_all()

    def activate(self, widget, event):
        self.win.clear_win()
        InternetScreen(self.win)
