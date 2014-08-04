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
from update_screen import UpdateScreen
from keyboard_screen import KeyboardScreen
from kano.network import is_internet
import kano_init_flow.constants as constants
from kano_init_flow.data import get_data
from kano.utils import detect_kano_keyboard


class FirstScreen():
    data = get_data("FIRST_SCREEN")

    def __init__(self, win):

        self.win = win
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "START SETUP")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.show_all()

    def activate(self, widget, event):
        self.win.clear_win()

        if not detect_kano_keyboard():
            KeyboardScreen(self.win)
        elif not is_internet():
            InternetScreen(self.win)
        else:
            UpdateScreen(self.win)
