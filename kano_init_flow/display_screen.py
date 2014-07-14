#!/usr/bin/env python

# display_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen for configuring display
#

from stage import Stage
from audio_screen import AudioScreen


class DisplayScreen():
    def __init__(self, win):

        self.win = win

        # check internet
        self.stage = Stage("../media/images/image_4.png", "Display screen placeholder", "", "NEXT", "")
        self.stage.kano_button.connect("button_release_event", self.activate)
        self.win.add(self.stage)

        self.win.show_all()

    def activate(self, widget, event):

        for child in self.win:
            self.win.remove(child)

        AudioScreen(self.win)
