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
from kano.utils import play_sound
from kano_settings.config_file import file_replace
import kano_init_flow.constants as constants

number_tries = 0


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
        global number_tries

        self.win = win
        number_tries += 1

        header = "Can you hear me?"
        subheader = ""
        self.template = AudioTemplate(constants.media + "/sound_test.png", header, subheader, "PLAY SOUND", "")
        self.template.kano_button.connect("button_release_event", self.play_sound)
        self.template.yes_button.connect("button_release_event", self.go_to_next)
        self.template.no_button.connect("button_release_event", self.fix_sound)
        self.win.add(self.template)

        self.win.show_all()

    def play_sound(self, widget, event):

        play_sound('/usr/share/kano-media/sounds/kano_make.wav', background=False)
        self.template.yes_button.set_sensitive(True)
        self.template.no_button.set_sensitive(True)

    def go_to_next(self, widget, event):
        exit_code = self.template.exit_codes["launch_profile"]
        sys.exit(exit_code)

    def fix_sound(self, widget, event):
        self.win.clear_win()
        if number_tries == 1:
            AudioTutorial1(self.win)
        else:
            TvSpeakersScreen(self.win)


class AudioTutorial1():
    def __init__(self, win):

        self.win = win

        header = "Can you see the light?"
        subheader = "If the power plug is connected properly you should see a blue light."
        self.template = Template(constants.media + "/Audio_See_the_light.png", header, subheader, "YES", "NO")
        self.template.kano_button.connect("button_release_event", self.end_screen)
        self.template.orange_button.connect("button_release_event", self.next_screen)
        self.template.set_size_request(590, 540)
        self.win.add(self.template)

        self.win.show_all()

    def end_screen(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        AudioTutorial3(self.win)

    def next_screen(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        AudioTutorial2(self.win)


class AudioTutorial2():
    def __init__(self, win):

        self.win = win

        header = "No light? Check the GPIO"
        subheader = "Make sure that you've connected the power lead to the right pins."
        self.template = Template(constants.media + "/Audio_GPIO.png", header, subheader, "NEXT", "")
        self.template.kano_button.connect("button_release_event", self.next_screen)
        self.template.set_size_request(590, 540)
        self.win.add(self.template)

        self.win.show_all()

    def next_screen(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        AudioTutorial3(self.win)


class AudioTutorial3():
    def __init__(self, win):

        self.win = win

        header = "Plug in the blue cable"
        subheader = "If you see the light, it's powered!"
        self.template = Template(constants.media + "/Audio_blue-cable.png", header, subheader, "FINISH", "")
        self.template.kano_button.connect("button_release_event", self.next_screen)
        self.template.set_size_request(590, 540)
        self.win.add(self.template)

        self.win.show_all()

    def next_screen(self, widget, event):
        for child in self.win:
            self.win.remove(child)

        AudioScreen(self.win)


class TvSpeakersScreen():
    def __init__(self, win):

        self.win = win

        header = "Let's switch to the TV speakers"
        subheader = "If you are using a TV with speakers, click the button below"
        self.template = Template(constants.media + "/tv-speakers.png", header, subheader, "USE TV SPEAKERS", "Setup Later")
        self.template.kano_button.connect("button_release_event", self.setup_hdmi)
        self.template.orange_button.connect("button_release_event", self.go_to_next)
        self.win.add(self.template)

        self.win.show_all()

    def setup_hdmi(self, widget, event):
        # Apply HDMI settings
        rc_local_path = "/etc/rc.audio"
        config_txt_path = "/boot/config.txt"
        # Uncomment/comment out the line in /boot/config.txt
        amixer_from = "amixer -c 0 cset numid=3 [0-9]"
        edid_from = "#?hdmi_ignore_edid_audio=1"
        drive_from = "#?hdmi_drive=2"
        # HDMI config
        amixer_to = "amixer -c 0 cset numid=3 2"
        edid_to = "#hdmi_ignore_edid_audio=1"
        drive_to = "hdmi_drive=2"

        file_replace(rc_local_path, amixer_from, amixer_to)
        file_replace(config_txt_path, edid_from, edid_to)
        file_replace(config_txt_path, drive_from, drive_to)

        # TODO: indicate kano-settings that we are now in HDMI

        self.win.clear_win()
        Reboot(self.win)

    def go_to_next(self, widget, event):
        exit_code = self.template.exit_codes["launch_profile"]
        sys.exit(exit_code)


class Reboot():
    def __init__(self, win):

        self.win = win

        header = "Reboot"
        subheader = "To apply changes and get sound from the TV, we'll need to do a quick reboot"
        self.template = Template("../media/images/image_5.png", header, subheader, "REBOOT", "")
        self.template.kano_button.connect("button_release_event", self.reboot)
        self.win.add(self.template)

        self.win.show_all()

    def reboot(self, widget, event):
        # For now
        exit_code = self.template.exit_codes["reboot"]
        sys.exit(exit_code)
