#!/usr/bin/env python

# internet_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen giving user options for the internet
#

import os
from gi.repository import Gdk
from template import Template
from settings_intro_screen import SettingsIntroScreen
import kano_init_flow.constants as constants
from kano_init_flow.data import get_data
from kano_init_flow.common import get_init_conf


class InternetScreen():
    data = get_data("INTERNET_SCREEN")

    def __init__(self, win):

        self.win = win

        # Skip Internet setup for workshops
        try:
            flow_type = get_init_conf()["kano_init_flow"]["flow"]
        except KeyError:
            flow_type = "normal"

        if flow_type == "workshops":
            self.go_to_next_screen()
            return

        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "CONNECT", orange_button_text="No internet")

        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.kano_button.connect("key_release_event", self.activate)
        self.template.get_orange_button().connect("button_release_event", self.skip)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            # Launch kano-wifi
            os.system('rxvt -title \'WiFi Setup\' -e sudo /usr/bin/kano-wifi')
            # Go to Settings
            self.go_to_next_screen()

    def skip(self, widget, event):
        self.win.clear_win()
        NoInternetScreen(self.win)

    def go_to_next_screen(self):
        self.win.clear_win()
        SettingsIntroScreen(self.win)


class NoInternetScreen():
    data = get_data("NO_INTERNET_SCREEN")

    def __init__(self, win):

        self.win = win
        self.win.set_resizable(True)
        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        image = constants.media + self.data["IMG_FILENAME"]
        self.template = Template(image, header, subheader, "TRY AGAIN", orange_button_text="Connect later")
        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event", self.launch_wifi_config)

        # WARNING: If the line below is commented out, the launched window
        # does not receive any key events
        # self.template.kano_button.connect("key_release_event", self.launch_wifi_config)
        self.template.orange_button.connect("button_release_event", self.next_screen)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def launch_wifi_config(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            # Launch kano-wifi
            os.system('rxvt -title \'WiFi Setup\' -e sudo /usr/bin/kano-wifi')
            # Go to Settings
            self.go_to_next_screen()

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
        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event", self.skip)
        self.template.kano_button.connect("key_release_event", self.skip)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def skip(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            self.win.clear_win()
            SettingsIntroScreen(self.win)
