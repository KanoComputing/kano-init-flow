#!/usr/bin/env python

# audio_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen for configuring audio
#

import sys
from gi.repository import Gtk

from kano.gtk3.buttons import KanoButton
from template import Template


class AudioTemplate(Template):

    def __init__(self, img_filename, title, description, kano_button_text, orange_button_text):
        Template.__init__(self, img_filename, title, description, kano_button_text, orange_button_text)

        button_box = Gtk.ButtonBox(spacing=10)
        button_box.set_layout(Gtk.ButtonBoxStyle.CENTER)

        self.yes_button = KanoButton("YES")
        self.yes_button.set_sensitive(False)
        self.no_button = KanoButton("NO")
        self.no_button.set_sensitive(False)
        button_box.pack_start(self.yes_button, False, False, 0)
        button_box.pack_start(self.no_button, False, False, 0)

        self.pack_start(button_box, False, False, 10)


class AudioScreen():
    def __init__(self, win):

        self.win = win

        self.template = AudioTemplate("../media/images/image_5.png", "Can you hear me?", "", "PLAY SOUND", "")
        self.template.kano_button.connect("button_release_event", self.play_sound)
        self.template.yes_button.connect("button_release_event", self.go_to_next)
        self.template.no_button.connect("button_release_event", self.fix_sound)
        self.win.add(self.template)

        self.win.show_all()

    def play_sound(self, widget, event):
        print "Playing sound"
        self.template.yes_button.set_sensitive(True)
        self.template.no_button.set_sensitive(True)

    def go_to_next(self, widget, event):
        exit_code = self.template.exit_codes["launch_profile"]
        sys.exit(exit_code)

    def fix_sound(self, widget, event):
        self.win.clear_win()
        TvSpeakersScreen(self.win)


class TvSpeakersScreen():
    def __init__(self, win):

        self.win = win

        self.template = Template("../media/images/image_5.png", "Let's switch to the TV speakers",
                                 "If you are using a TV with speakers, click the button below", "USE TV SPEAKERS", "STEtUP LATER")
        self.template.kano_button.connect("button_release_event", self.setup_hdmi)
        self.template.orange_button.connect("button_release_event", self.go_to_next)
        self.win.add(self.template)

        self.win.show_all()

    def setup_hdmi(self, widget, event):
        print "setup hdmi"
        self.win.clear_win()
        Reboot(self.win)

    def go_to_next(self, widget, event):
        exit_code = self.template.exit_codes["launch_profile"]
        sys.exit(exit_code)


class Reboot():
    def __init__(self, win):

        self.win = win

        self.template = Template("../media/images/image_5.png", "Reboot",
                                 "To apply changes and get sound from the TV, we'll need to do a quick reboot", "REBOOT", "")
        self.template.kano_button.connect("button_release_event", self.reboot)
        self.win.add(self.template)

        self.win.show_all()

    def reboot(self, widget, event):
        sys.exit(5)
