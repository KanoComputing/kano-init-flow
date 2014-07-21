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


class InternetScreen():

    def __init__(self, win):

        self.win = win

        header = "Connect to the world"
        subheader = "Let's setup Wifi and bring your Kano to life"
        self.template = Template(constants.media + "/connect.png", header, subheader, "CONNECT", "No Internet")

        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.get_orange_button().connect("button_release_event", self.skip)
        self.win.show_all()

    def activate(self, widget, event):
        exit_code = self.template.exit_codes["launch_wifi"]
        sys.exit(exit_code)

    def skip(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        NoInternetScreen(self.win)


class NoInternetScreen():

    def __init__(self, win):

        self.win = win
        header = "No internet?"
        subheader = "Try again, or connect later. You need internet for most of Kano's cool powers."
        image = constants.media + "/no_internet.png"
        self.template = Template(image, header, subheader, "TRY AGAIN", "Connect Later")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.launch_wifi_config)
        self.template.orange_button.connect("button_release_event", self.next_screen)
        self.win.show_all()

    def launch_wifi_config(self, widget, event):
        exit_code = self.template.exit_codes["launch_wifi"]
        sys.exit(exit_code)

    def next_screen(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        OfflineScreen(self.win)


class OfflineScreen():

    def __init__(self, win):

        self.win = win
        header = "Internet trouble? We can help!"
        subheader = "Kano is coolest when it's online. Go to http://help.kano.me and we''l help you."
        image = constants.media + "/internet_trouble.png"
        self.template = Template(image, header, subheader, "PLAY OFFLINE", "")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.skip)
        self.win.show_all()

    def skip(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        SettingsIntroScreen(self.win)
