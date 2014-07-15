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


class FirstScreen():
    def __init__(self, win):

        self.win = win
        self.template = Template("../media/images/image_1.png", "Welcome!",
                                 "You made a computer.  Now let's connect it to the internet", "START", "")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.show_all()

    def activate(self, widget, event):
        self.win.clear_win()
        InternetScreen(self.win)
