#!/usr/bin/env python

# settings_intro_screen
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Tells user they will configure display and audio
#

from stage import Stage
from display_screen import DisplayScreen


class SettingsIntroScreen():
    def __init__(self, win):

        self.win = win

        # check internet
        self.stage = Stage("../media/images/image_3.png", "Let's put your powers to the test", "Time to test audio and display settings", "NEXT", "")
        self.stage.kano_button.connect("button_release_event", self.activate)
        self.win.add(self.stage)

        self.win.show_all()

    def activate(self, widget, event):

        for child in self.win:
            self.win.remove(child)

        DisplayScreen(self.win)
