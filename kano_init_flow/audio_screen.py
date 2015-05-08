#!/usr/bin/env python

# audio_screen.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Screen for configuring audio
#

import time
import os
from gi.repository import Gtk

from kano.gtk3.buttons import KanoButton
from kano.gtk3.heading import Heading
from kano.utils import play_sound
from kano_settings.system.audio import is_HDMI, set_to_HDMI, hdmi_supported

from kano_init_flow.display_screen import DisplayScreen
from kano_init_flow.paths import MEDIA_DIR
from kano_init_flow.template import Template, TopImageTemplate, HintHeading

number_tries = 0


class AudioTemplate(Gtk.Box):

    def __init__(self, img_path, title, description):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        if img_path:
            self.image = Gtk.Image.new_from_file(img_path)
            self.pack_start(self.image, False, False, 0)
        self.heading = Heading(title, description)

        icon_path = os.path.join(MEDIA_DIR, "play-sound.png")
        self.kano_button = KanoButton(text="PLAY SOUND", color="blue",
                                      icon_filename=icon_path)
        self.kano_button.pack_and_align()
        self.kano_button.set_margin_top(10)
        self.pack_start(self.heading.container, False, False, 0)
        self.pack_start(self.kano_button.align, False, False, 0)

        button_box = Gtk.ButtonBox(spacing=15)
        button_box.set_layout(Gtk.ButtonBoxStyle.CENTER)

        self.yes_button = KanoButton("YES")
        self.yes_button.set_sensitive(False)
        self.no_button = KanoButton("NO", color="red")
        self.no_button.set_sensitive(False)
        button_box.pack_start(self.yes_button, False, False, 0)
        button_box.pack_start(self.no_button, False, False, 0)
        button_box.set_margin_bottom(5)

        self.pack_start(button_box, False, False, 15)


class AudioHintTemplate(TopImageTemplate):

    def __init__(self, img_path, title, description, kano_button_text,
                 hint_text="", orange_button_text=""):
        TopImageTemplate.__init__(self, img_path)

        self.heading = HintHeading(title, description, hint_text)
        self.pack_start(self.heading.container, False, False, 0)

        self.heading.description.set_margin_bottom(0)
        self.heading.container.set_margin_bottom(0)
        self.heading.container.set_size_request(590, -1)
        self.heading.container.set_spacing(0)

        self.kano_button = KanoButton(kano_button_text)
        self.kano_button.set_margin_top(30)
        self.kano_button.set_margin_bottom(30)
        self.kano_button.pack_and_align()

        self.pack_start(self.kano_button.align, False, False, 0)


class AudioScreen(object):

    def __init__(self, win):
        global number_tries

        self.win = win
        self.time_click = None

        if number_tries == 0:
            header = "Can you hear me?"
        else:
            header = "Let's try again - can you hear me now?"
            self.win.shrink()
        subheader = ""
        self.template = AudioTemplate(
            os.path.join(MEDIA_DIR, 'sound_test.png'),
            header,
            subheader
        )
        self.template.kano_button.connect("button_release_event",
                                          self.play_sound)
        self.template.kano_button.connect("key_release_event",
                                          self.play_sound)
        self.template.yes_button.connect("button_release_event",
                                         self.go_to_next)
        self.template.yes_button.connect("key_release_event",
                                         self.go_to_next)
        self.template.no_button.connect("button_release_event",
                                        self.fix_sound)
        self.template.no_button.connect("key_release_event",
                                        self.fix_sound)
        self.win.set_main_widget(self.template)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

        number_tries += 1

    def play_sound(self, widget, event):
        # Check if first click or 3 seconds have passed
        ready = (self.time_click is None) or (time.time() - self.time_click > 3)
        # If ready and enter key is pressed or mouse button is clicked
        if ready and \
            (not hasattr(event, 'keyval') or event.keyval == 65293):

            self.time_click = time.time()
            play_sound('/usr/share/kano-media/sounds/kano_test_sound.wav',
                       background=True)
            time.sleep(1)

            self.template.yes_button.set_sensitive(True)
            self.template.no_button.set_sensitive(True)

            self.template.yes_button.grab_focus()

    def go_to_next(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            self.win.clear_win()
            DisplayScreen(self.win)

    def fix_sound(self, widget, event):
        """
        Launches the appropriate screen for resolving the problem
        of not hearing any sound.
        """

        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            self.win.clear_win()

            if number_tries == 1:
                # check if current settings is configured for HDMI or analogue
                if not is_HDMI():
                    SeeTheLightScreen(self.win)
                else:
                    AnalogueScreen(self.win)
            else:
                if hdmi_supported:
                    TvSpeakersScreen(self.win)
                else:
                    DisplayScreen(self.win)


class SeeTheLightScreen(object):
    """
    Troubleshooting screen: is the power light on the speaker on?
    """

    def __init__(self, win):

        self.win = win

        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "Audio_See_the_light.png"),
            title="Can you see the light?",
            description="If the power plugs are connected correctly, " \
                        "you should see a blue light.",
            button1_text="YES",
            button2_text="NO"
        )
        self.template.kano_button2.set_color("red")
        self.template.kano_button.connect("button_release_event",
                                          self.end_screen)
        self.template.kano_button.connect("key_release_event",
                                          self.end_screen)
        self.template.kano_button2.connect("button_release_event",
                                           self.next_screen)
        self.template.kano_button2.connect("key_release_event",
                                           self.next_screen)
        self.win.set_main_widget(self.template)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def end_screen(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            self.win.clear_win()
            BlueCableScreen(self.win)

    def next_screen(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            self.win.clear_win()
            CheckTheGPIOScreen(self.win)


class CheckTheGPIOScreen(object):

    def __init__(self, win):

        self.win = win

        self.template = AudioHintTemplate(
            img_path=os.path.join(MEDIA_DIR, "Audio_GPIO.png"),
            title="No light? Check the GPIO",
            description="The red and black cables have to be connected to " \
                        "these two pins - exactly.",
            kano_button_text="NEXT",
            hint_text="Make sure the red cable is on top."
        )
        self.template.kano_button.connect("button_release_event",
                                          self.next_screen)
        self.template.kano_button.connect("key_release_event",
                                          self.next_screen)
        self.win.set_main_widget(self.template)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def next_screen(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            self.win.clear_win()
            BlueCableScreen(self.win)


class BlueCableScreen(object):

    def __init__(self, win):

        self.win = win

        self.template = AudioHintTemplate(
            img_path=os.path.join(MEDIA_DIR, "Audio_blue-cable.png"),
            title="Plug in the blue cable",
            description="If you see the light, it's powered!",
            kano_button_text="FINISH",
            hint_text="Now plug the audio."
        )
        self.template.kano_button.connect("button_release_event",
                                          self.next_screen)
        self.template.kano_button.connect("key_release_event",
                                          self.next_screen)
        self.win.set_main_widget(self.template)
        self.win.shrink()

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def next_screen(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            self.win.clear_win()
            AudioScreen(self.win)


class TvSpeakersScreen(object):

    def __init__(self, win):

        self.win = win

        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "/tv-speakers.png"),
            title="Let's switch to the TV speakers",
            description="If you're using a TV with speakers, " \
                        "click the button below",
            button1_text="USE TV SPEAKERS",
            orange_button_text="Setup later"
        )
        self.template.kano_button.connect("button_release_event",
                                          self.setup_hdmi)
        self.template.orange_button.connect("button_release_event",
                                            self.go_to_next)
        self.template.kano_button.connect("key_release_event",
                                          self.setup_hdmi)
        self.win.set_main_widget(self.template)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def setup_hdmi(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            set_to_HDMI(True)
            self.go_to_next()

    def go_to_next(self, widget=None, event=None):

        self.win.clear_win()
        DisplayScreen(self.win)


class AnalogueScreen(object):

    def __init__(self, win):

        self.win = win

        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "Audio_Use_Speakers.png"),
            title="Let's switch your speaker",
            description="If you want to change from TV sound to analogue " \
                        "speaker, click the button below",
            button1_text="USE SPEAKERS",
            orange_button_text="Setup later"
        )
        self.template.kano_button.connect("button_release_event",
                                          self.setup_analogue)
        self.template.kano_button.connect("key_release_event",
                                          self.setup_analogue)
        self.template.orange_button.connect("button_release_event",
                                            self.go_to_next)
        self.win.set_main_widget(self.template)

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def setup_analogue(self, widget, event):
        # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:
            set_to_HDMI(False)
            self.go_to_next()

    def go_to_next(self, widget=None, event=None):

        self.win.clear_win()
        DisplayScreen(self.win)
