#!/usr/bin/env python

# settings_intro_screen
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Tells user they will configure display and audio
#

import os

from kano.network import is_internet

from kano_init_flow.template import Template
from kano_init_flow.audio_screen import AudioScreen
from kano_init_flow.paths import MEDIA_DIR
from kano_init_flow.data import get_data


class SettingsIntroScreen(object):
    data = get_data("SETTINGS_INTRO_SCREEN")

    def __init__(self, win):

        self.win = win
        self.win.set_resizable(True)
        header = self.data["LABEL_1"]
        if is_internet():
            subheader = self.data["LABEL_2"]
        else:
            subheader = self.data["LABEL_3"]
        self.template = Template(
            os.path.join(MEDIA_DIR, self.data["IMG_FILENAME"]),
            header,
            subheader,
            "TEST SOUND"
        )
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.kano_button.connect("key_release_event", self.activate)
        self.win.set_main_widget(self.template)
        self.win.shrink()

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, widget, event):
         # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            self.win.clear_win()
            AudioScreen(self.win)
