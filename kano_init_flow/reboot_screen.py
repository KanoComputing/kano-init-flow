#!/usr/bin/env python

# reboot_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Shows message before reboot
#

import sys
import os
from kano_init_flow.template import Template


class RebootScreen(object):

    def __init__(self, win):
        self.win = win
        self.win.shrink()

        self.template = Template(
            img_path=None,
            title="Time to reboot",
            description="To finish setup, we have to do a quick reboot. " \
                        "Don't worry! Everything is saved.",
            button1_text="REBOOT"
        )
        self.win.set_main_widget(self.template)
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.kano_button.connect("key_release_event", self.activate)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, _, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            os.system('reboot')
            sys.exit(0)
