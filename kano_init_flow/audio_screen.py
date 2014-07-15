#!/usr/bin/env python

# audio_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen for configuring audio
#

import sys
from kano_init_flow.template import Template


class AudioScreen():
    def __init__(self, win):

        self.win = win

        # check internet
        self.template = Template("../media/images/image_5.png", "Audio screen placeholder", "", "FINISH", "")
        self.template.kano_button.connect("button_release_event", self.activate)
        self.win.add(self.template)

        self.win.show_all()

    def activate(self, widget, event):

        # Exit with 4 so that it doesn't launch the updater
        sys.exit(4)
