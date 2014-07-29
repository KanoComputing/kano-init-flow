#!/usr/bin/env python

# audio_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen for configuring audio
#

from gi.repository import Gtk

from kano.gtk3.buttons import KanoButton
from kano.gtk3.heading import Heading
from template import Template
from kano.utils import play_sound
from kano_settings.config_file import file_replace
import kano_init_flow.constants as constants
from kano_init_flow.data import get_data
from kano_init_flow.paths import media_dir
from kano_init_flow.display_screen import DisplayScreen

number_tries = 0


class AudioTemplate(Gtk.Box):

    def __init__(self, img_filename, title, description):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        if img_filename is not None:
            self.image = Gtk.Image.new_from_file(img_filename)
            self.pack_start(self.image, False, False, 0)
        self.heading = Heading(title, description)

        self.kano_button = KanoButton(text="PLAY SOUND", color="blue", icon_filename=media_dir + "/play-sound.png")
        self.kano_button.pack_and_align()
        self.kano_button.set_margin_top(10)
        self.pack_start(self.heading.container, False, False, 0)
        self.pack_start(self.kano_button.align, False, False, 0)

        button_box = Gtk.ButtonBox(spacing=15)
        button_box.set_layout(Gtk.ButtonBoxStyle.CENTER)

        self.yes_button = KanoButton("YES")
        self.yes_button.set_sensitive(False)
        self.no_button = KanoButton("NO")
        self.no_button.set_sensitive(False)
        button_box.pack_start(self.yes_button, False, False, 0)
        button_box.pack_start(self.no_button, False, False, 0)
        button_box.set_margin_bottom(5)

        self.pack_start(button_box, False, False, 15)


class AudioHintTemplate(Template):

    def __init__(self, img_filename, title, description, kano_button_text, hint_text="", orange_button_text=""):
        Template.__init__(self, img_filename, title, description, kano_button_text, orange_button_text=orange_button_text)
        self.kano_button.set_margin_top(30)

        hint = Gtk.Label(hint_text)
        hint.get_style_context().add_class("hint_label")
        hint.set_margin_top(0)
        self.heading.description.set_margin_bottom(0)

        self.heading.container.pack_start(hint, False, False, 0)


class AudioScreen():
    data = get_data("AUDIO_SCREEN")

    def __init__(self, win):
        global number_tries

        self.win = win

        if number_tries == 0:
            header = self.data["LABEL_1"]
        else:
            header = self.data["LABEL_3"]
            self.win.reset_allocation()
        subheader = self.data["LABEL_2"]
        self.template = AudioTemplate(constants.media + self.data["IMG_FILENAME"], header, subheader)
        self.template.kano_button.connect("button_release_event", self.play_sound)
        self.template.yes_button.connect("button_release_event", self.go_to_next)
        self.template.no_button.connect("button_release_event", self.fix_sound)
        self.win.add(self.template)

        self.win.show_all()

        number_tries += 1

    def play_sound(self, widget, event):

        play_sound('/usr/share/kano-media/sounds/kano_make.wav', background=False)
        self.template.yes_button.set_sensitive(True)
        self.template.no_button.set_sensitive(True)

    def go_to_next(self, widget, event):
        self.win.clear_win()
        DisplayScreen(self.win)

    def fix_sound(self, widget, event):
        self.win.clear_win()
        if number_tries == 1:
            AudioTutorial1(self.win)
        else:
            TvSpeakersScreen(self.win)


class AudioTutorial1():
    data = get_data("AUDIO_TUTORIAL_1")

    def __init__(self, win):

        self.win = win

        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "YES", button2_text="NO")
        self.template.kano_button.connect("button_release_event", self.end_screen)
        self.template.kano_button2.connect("button_release_event", self.next_screen)
        self.win.add(self.template)

        self.win.show_all()

    def end_screen(self, widget, event):
        self.win.clear_win()
        AudioTutorial3(self.win)

    def next_screen(self, widget, event):
        self.win.clear_win()
        AudioTutorial2(self.win)


class AudioTutorial2():
    data = get_data("AUDIO_TUTORIAL_2")

    def __init__(self, win):

        self.win = win

        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        hint = self.data["LABEL_3"]
        self.template = AudioHintTemplate(constants.media + self.data["IMG_FILENAME"], header, subheader, "NEXT", hint_text=hint)
        self.template.kano_button.connect("button_release_event", self.next_screen)
        self.win.add(self.template)

        self.win.show_all()

    def next_screen(self, widget, event):
        self.win.clear_win()
        AudioTutorial3(self.win)


class AudioTutorial3():
    data = get_data("AUDIO_TUTORIAL_3")

    def __init__(self, win):

        self.win = win

        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        hint = self.data["LABEL_3"]
        self.template = AudioHintTemplate(constants.media + self.data["IMG_FILENAME"], header, subheader, "FINISH", hint_text=hint)
        self.template.kano_button.connect("button_release_event", self.next_screen)
        self.win.add(self.template)
        self.win.reset_allocation()

        self.win.show_all()

    def next_screen(self, widget, event):
        self.win.clear_win()

        AudioScreen(self.win)


class TvSpeakersScreen():
    data = get_data("TV_SPEAKERS_SCREEN")

    def __init__(self, win):

        self.win = win

        header = self.data["LABEL_1"]
        subheader = self.data["LABEL_2"]
        self.template = Template(constants.media + self.data["IMG_FILENAME"], header, subheader, "USE TV SPEAKERS", orange_button_text="Setup later")
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

        self.got_to_next()

    def go_to_next(self, widget=None, event=None):

        self.win.clear_win()
        DisplayScreen(self.win)
