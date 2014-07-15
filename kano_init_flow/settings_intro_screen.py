#!/usr/bin/env python

# settings_intro_screen
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Tells user they will configure display and audio
#

from template import Template
from display_screen import DisplayScreen


class SettingsIntroScreen():
    def __init__(self, win):

        self.win = win

        # check internet
        self.template = Template("../media/images/image_3.png", "Let's put your powers to the test", "Time to test audio and display settings", "NEXT", "")
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.add(self.template)

        self.win.show_all()

    def activate(self, widget, event):

        for child in self.win:
            self.win.remove(child)

        DisplayScreen(self.win)
