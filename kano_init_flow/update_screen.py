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


class UpdateScreen():
    def __init__(self, win):

        self.win = win

        # check internet
        if is_internet():
            network = self.network_info()[0]
            header = "You are connected to %s- Now let's update!" % network
            subheader = "Updating takes about 10 minutes."
            self.template = Template(constants.media + "/update.png", header, subheader, "UPDATE NOW!", "")
            self.template.kano_button.connect("button_release_event", self.launch_updater)
        else:
            header = "No internet?"
            subheader = "Try again, or connect later. You need internet for most of Kano's cool powers."
            self.template = Template(constants.media + "/update.png", header, subheader, "TRY AGAIN", "Connect Later")
            self.template.kano_button.connect("button_release_event", self.launch_wifi_config)
            self.template.orange_button.connect("button_release_event", self.next_screen)

        self.win.add(self.template)
        self.win.show_all()

    def launch_updater(self, widget, event):
        exit_code = self.template.exit_codes["launch_updater"]
        sys.exit(exit_code)

    def launch_wifi_config(self, widget, event):
        exit_code = self.template.exit_codes["launch_wifi"]
        sys.exit(exit_code)

    def next_screen(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        SettingsIntroScreen(self.win)

    # TODO: This is duplicated code from kano_settings/set_wifi/wifi.py
    def network_info(self):
        network = ''
        command_ip = ''
        command_network = '/sbin/iwconfig wlan0 | grep \'ESSID:\' | awk \'{print $4}\' | sed \'s/ESSID://g\' | sed \'s/\"//g\''
        out, e, _ = run_cmd(command_network)
        if e:
            network = "Ethernet"
            command_ip = '/sbin/ifconfig eth0 | grep inet | awk \'{print $2}\' | cut -d\':\' -f2'
        else:
            network = out
            command_ip = '/sbin/ifconfig wlan0 | grep inet | awk \'{print $2}\' | cut -d\':\' -f2'
        ip, _, _ = run_cmd(command_ip)

        return [network.rstrip(), ip.rstrip()]
