#!/usr/bin/env python

# settings_intro_screen
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Tells user they will configure display and audio
#

from template import Template
#from display_screen import DisplayScreen
from audio_screen import AudioScreen
import kano_init_flow.constants as constants


class SettingsIntroScreen():
    def __init__(self, win):

        self.win = win

        header = "You have the power!"
        subheader = "Update successful! Now let's test out your powers."
        self.template = Template(constants.media + "/update_successful.png", header, subheader, "TEST SOUND", "")
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.add(self.template)

        self.win.show_all()

    def activate(self, widget, event):
        self.win.clear_win()
        # DisplayScreen(self.win)
        AudioScreen(self.win)
