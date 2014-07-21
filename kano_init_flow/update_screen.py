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
from kano.utils import run_cmd
import kano_init_flow.constants as constants
from kano_init_flow.data import get_data


class UpdateScreen():
    data = get_data("UPDATE_SCREEN")

    def __init__(self, win):
        self.win = win

        # check internet
        if not is_internet():
            self.next_screen()
            return

        network = self.network_info()
        header = "You are connected to %s- Now let's update!" % network
        subheader = self.data["LABEL_2"]
        image = constants.media + self.data["IMG_FILENAME"]
        self.template = Template(image, header, subheader, "UPDATE NOW!", "")
        self.template.kano_button.connect("button_release_event", self.launch_updater)

        self.win.add(self.template)
        self.win.show_all()

    def launch_updater(self, widget, event):
        exit_code = self.template.exit_codes["launch_updater"]
        sys.exit(exit_code)

    def next_screen(self):
        self.win.clear_win()
        SettingsIntroScreen(self.win)

    # TODO: This is duplicated code from kano_settings/set_wifi/wifi.py
    def network_info(self):
        network = ''
        command_network = '/sbin/iwconfig wlan0 | grep \'ESSID:\' | awk \'{print $4}\' | sed \'s/ESSID://g\' | sed \'s/\"//g\''
        out, e, _ = run_cmd(command_network)
        if e:
            network = "Ethernet"
        else:
            network = out

        return network.rstrip()
