#!/usr/bin/env python

# first_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Intro screen of the first boot
#

import os

from kano.network import is_internet
from kano.utils import detect_kano_keyboard

from kano_init_flow.paths import MEDIA_DIR
from kano_init_flow.data import get_data
from kano_init_flow.template import Template
from kano_init_flow.internet_screen import InternetScreen
from kano_init_flow.settings_intro_screen import SettingsIntroScreen
from kano_init_flow.keyboard_screen import KeyboardScreen


class FirstScreen(object):
    data = get_data("FIRST_SCREEN")

    def __init__(self, win):

        self.win = win
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(
            os.path.join(MEDIA_DIR, self.data["IMG_FILENAME"]),
            header,
            subheader,
            "START SETUP"
        )
        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event",
                                          self.activate)
        self.template.kano_button.connect("key_release_event",
                                          self.activate)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, widget, event):
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            self.win.clear_win()

            if not detect_kano_keyboard():
                KeyboardScreen(self.win)
            elif not is_internet():
                InternetScreen(self.win)
            else:
                SettingsIntroScreen(self.win)
