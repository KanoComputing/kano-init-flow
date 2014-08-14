#!/usr/bin/env python

# internet_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen giving user options for the internet
#

import sys
from template import Template
from settings_intro_screen import SettingsIntroScreen
import kano_init_flow.constants as constants
from kano_init_flow.data import get_data


class InternetScreen():
    data = get_data("INTERNET_SCREEN")

    def __init__(self, win):

        self.win = win

        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "CONNECT", orange_button_text="No internet")

        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.kano_button.connect("key_release_event", self.activate)
        self.template.get_orange_button().connect("button_release_event", self.skip)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            exit_code = self.template.exit_codes["launch_wifi"]
            sys.exit(exit_code)

    def skip(self, widget, event):
        self.win.clear_win()
        NoInternetScreen(self.win)


class NoInternetScreen():
    data = get_data("NO_INTERNET_SCREEN")

    def __init__(self, win):

        self.win = win
        self.win.set_resizable(True)
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        image = constants.media + self.data["IMG_FILENAME"]
        self.template = Template(image, header, subheader, "TRY AGAIN", orange_button_text="Connect later")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.launch_wifi_config)
        self.template.kano_button.connect("key_release_event", self.launch_wifi_config)
        self.template.orange_button.connect("button_release_event", self.next_screen)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def launch_wifi_config(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            exit_code = self.template.exit_codes["launch_wifi"]
            sys.exit(exit_code)

    def next_screen(self, widget, event):
        self.win.clear_win()
        OfflineScreen(self.win)


class OfflineScreen():
    data = get_data("OFFLINE_SCREEN")

    def __init__(self, win):

        self.win = win
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        image = constants.media + self.data["IMG_FILENAME"]
        self.template = Template(image, header, subheader, "PLAY OFFLINE")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.skip)
        self.template.kano_button.connect("key_release_event", self.skip)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def skip(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            self.win.clear_win()
            SettingsIntroScreen(self.win, False)
