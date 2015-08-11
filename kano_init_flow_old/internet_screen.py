#!/usr/bin/env python

# internet_screen.py
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen giving user options for the internet
#

import os
from gi.repository import Gdk

from .paths import MEDIA_DIR
from .common import get_init_conf
from .template import Template
from .settings_intro_screen import SettingsIntroScreen


class InternetScreen(object):
    """ Screen to launch the connection GUI """

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

        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "connect.png"),
            title=_("Connect to the world"),
            description=_("Let's set up WiFi and bring your Kano to life"),
            button1_text=_("Connect").upper(),
            orange_button_text=_("No internet")
        )

        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event",
                                          self.activate)
        # WARNING: If the line below is commented out, the launched window
        # does not receive any key events
        # self.template.kano_button.connect("key_release_event", self.activate)

        self.template.get_orange_button().connect("button_release_event",
                                                  self.skip)

        # No need to grab the focus if we can't use the Enter key to "click" it
        # self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, _, event):
        """ Launch the WiFi setup screen """

        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            # Launch kano-wifi
            # os.system('rxvt -title \'WiFi Setup\' -e sudo /usr/bin/kano-wifi')
            os.system('sudo /usr/bin/kano-wifi-gui')

            # Go to Settings
            self.go_to_next_screen()

    def skip(self, *_):
        """ Skip the up Internet connection phase """

        self.win.clear_win()
        NoInternetScreen(self.win)

    def go_to_next_screen(self):
        """ Move on """

        self.win.clear_win()
        SettingsIntroScreen(self.win)


class NoInternetScreen(object):
    """
    Screen for when the Internet has purposefully
    not been configured by the user
    """

    def __init__(self, win):
        self.win = win
        self.win.set_resizable(True)

        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "no_internet.png"),
            title=_("No internet?"),
            description=_("Try again, or connect later. You need internet "
                          "for most of Kano's coolest powers."),
            button1_text=_("TRY AGAIN"),
            orange_button_text=_("Connect later")
        )
        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event",
                                          self.launch_wifi_config)

        # WARNING: If the line below is commented out, the launched window
        # does not receive any key events
        # self.template.kano_button.connect("key_release_event",
        #                                   self.launch_wifi_config)
        self.template.orange_button.connect("button_release_event",
                                            self.go_to_next_screen)

        # No need to grab the focus if we can't use the Enter key to "click" it
        # self.template.kano_button.grab_focus()

        self.win.show_all()

    def launch_wifi_config(self, _, event):
        """ Launch the WiFi config """

        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == Gdk.KEY_Return:
            # Launch kano-wifi
            # os.system('rxvt -title \'WiFi Setup\' -e sudo /usr/bin/kano-wifi')
            os.system('sudo /usr/bin/kano-wifi-gui')

            # Go to Settings
            self.go_to_next_screen()

    def go_to_next_screen(self, *_):
        """ Carry on to the next phase """

        self.win.clear_win()
        OfflineScreen(self.win)


class OfflineScreen(object):
    """
    Screen for when the Internet has purposefully
    not been configured by the user
    """

    def __init__(self, win):
        self.win = win

        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "internet_trouble.png"),
            title=_("Internet trouble? We can help!"),
            description=_("Visit http://help.kano.me on another device, "
                          "or email wifi@kano.me. You can play offline in "
                          "the meantime."),
            button1_text=_("PLAY OFFLINE").upper()
        )

        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event", self.skip)
        self.template.kano_button.connect("key_release_event", self.skip)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def skip(self, _, event):
        """ Move on to next phase """

        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            self.win.clear_win()
            SettingsIntroScreen(self.win)
