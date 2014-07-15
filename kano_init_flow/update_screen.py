#!/usr/bin/env python

# update_screen,py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen giving user options for updating
#

import sys
from template import Template
from kano.network import is_internet
from settings_intro_screen import SettingsIntroScreen


class UpdateScreen():
    def __init__(self, win):

        self.win = win

        # check internet
        if is_internet():
            self.template = Template("../media/images/image_3.png", "Great, you have internet!", "Now let's update your system", "UPDATE NOW!", "USING PROXY?")
            self.template.kano_button.connect("button_release_event", self.launch_updater)
            self.template.orange_button.connect("button_release_event", self.using_proxy)
        else:
            self.template = Template("../media/images/image_3.png", "No internet?", "No worried, we can still play", "NEXT", "CONNECT")
            self.template.kano_button.connect("button_release_event", self.next_screen)
            self.template.orange_button.connect("button_release_event", self.launch_wifi_config)

        self.win.add(self.template)
        self.win.show_all()

    def launch_updater(self, widget, event):
        sys.exit(3)

    def launch_wifi_config(self, widget, event):
        sys.exit(2)

    def using_proxy(self, widget, event):
        sys.exit(4)

    def next_screen(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        SettingsIntroScreen(self.win)
