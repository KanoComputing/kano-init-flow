# first_screen.py
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Intro screen of the first boot
#

import os

from kano.network import is_internet
from kano.utils import detect_kano_keyboard

from kano_init_flow.paths import MEDIA_DIR
from kano_init_flow.template import Template
from kano_init_flow.internet_screen import InternetScreen
from kano_init_flow.settings_intro_screen import SettingsIntroScreen
from kano_init_flow.keyboard_screen import KeyboardScreen


class FirstScreen(object):
    """
    Initial screen. Introduces the init flow.
    """

    def __init__(self, win):

        self.win = win
        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "made_it.png"),
            title="We made it!",
            description="You made a computer - now let's give it new powers!",
            button1_text="START SETUP"
        )
        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event",
                                          self.activate)
        self.template.kano_button.connect("key_release_event",
                                          self.activate)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, _, event):
        """ Move to the first setup screen """

        if not hasattr(event, 'keyval') or event.keyval == 65293:
            self.win.clear_win()

            if not detect_kano_keyboard():
                KeyboardScreen(self.win)
            elif not is_internet():
                InternetScreen(self.win)
            else:
                SettingsIntroScreen(self.win)
