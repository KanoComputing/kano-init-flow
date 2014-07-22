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
from kano_init_flow.data import get_data


class SettingsIntroScreen():
    data = get_data("SETTINGS_INTRO_SCREEN")

    def __init__(self, win, internet=True):

        self.win = win

        header = self.data["LABEL_1"]
        if internet:
            subheader = self.data["LABEL_2"]
        else:
            subheader = self.data["LABEL_3"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "TEST SOUND", "")
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.add(self.template)

        self.win.show_all()

    def activate(self, widget, event):
        self.win.clear_win()
        # TODO: DisplayScreen(self.win)
        AudioScreen(self.win)
