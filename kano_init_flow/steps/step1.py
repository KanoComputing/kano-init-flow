#!/usr/bin/env python

# step1.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The first speech bubble of the init flow
#

from kano.network import is_internet
from kano.utils import detect_kano_keyboard

from kano_init_flow.data import get_data
from kano_init_flow.speech_bubble_dialog import SpeechBubbleDialog

# Screens that may follow
from kano_init_flow.internet_screen import InternetScreen
from kano_init_flow.settings_intro_screen import SettingsIntroScreen
from kano_init_flow.keyboard_screen import KeyboardScreen


class Step1:
    data = get_data("STEP1")

    def __init__(self, win):
        self.win = win
        header = self.data["HEADER"]
        subheader = self.data["TEXT"]

        sbd = SpeechBubbleDialog(header, subheader,
                                 source=SpeechBubbleDialog.BOTTOM,
                                 source_align=0.5, has_judoka=True)
        button = sbd.add_button('START', self.activate)
        button.grab_focus()

        # Make one of the kano button grab the focus
        self.win.set_main_widget(sbd)

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
