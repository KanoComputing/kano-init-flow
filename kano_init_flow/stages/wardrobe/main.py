# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
from gi.repository import Gtk, Gdk

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.paths import common_media_path
from kano_avatar_gui.CharacterCreator import CharacterCreator
from kano.gtk3.kano_dialog import KanoDialog
from kano_init_flow.ui.components import NextButton


class Wardrobe(Stage):
    """
        The first screen where the judoka introduces himself
    """

    id = 'wardrobe'
    _root = __file__

    def __init__(self, ctl):
        super(Wardrobe, self).__init__(ctl)
        apply_styling_to_screen(self.css_path("wardrobe.css"))

    def first_scene(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1.widget)

    def second_scene(self):
        s3 = self._setup_second_scene()
        self._ctl.main_window.push(s3.widget)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()

        scene.set_background(self.media_path('scene-1600x1200.png'),
                             self.media_path('scene-1920x1080.png'))

        self._first_scene = scene

        scene.add_widget(
            SpeechBubble(
                text="Let's dress up your\ncharacter!",
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.9, 0.4),
            Placement(0.85, 0.45)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("tailor-judoka.png")),
            Placement(0.85, 0.8, 0.85),
            Placement(0.8, 0.9, 0.85)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("outline.gif")),
            Placement(0.5, 0.7, 0.95),
            Placement(0.45, 0.72, 0.95),
            self._char_creator_dialog
        )

        return scene

    def _create_blur(self):
        blur = Gtk.EventBox()

        screen = Gdk.Screen.get_default()
        width = screen.get_width()
        height = screen.get_height()

        blur.set_size_request(width, height)
        return blur

    def _char_creator_dialog(self):
        self._blur = self._create_blur()

        # Add watch cursor
        watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
        self._ctl.main_window.get_window().set_cursor(watch_cursor)

        self._first_scene.add_widget(
            self._blur,
            Placement(0, 0),
            Placement(0, 0)
        )
        self._blur.get_style_context().add_class("blur")
        self._first_scene.show_all()

        while Gtk.events_pending():
            Gtk.main_iteration()

        char_edit = CharacterCreator(randomise=True)
        kdialog = KanoDialog(widget=char_edit)
        kdialog.run()
        char_edit.save()
        self.second_scene()

    def _setup_second_scene(self):
        self._ctl.main_window.get_window().set_cursor(None)
        scene = Scene(self._ctl.main_window)
        scene.set_background(self.media_path('scene-1600x1200.png'),
                             self.media_path('scene-1920x1080.png'))

        # Need to get the character at this point.
        char_path = os.path.join(
            os.path.expanduser("~"), ".character-content/character.png"
        )

        scene.add_widget(
            Gtk.Image.new_from_file(char_path),
            Placement(0.5, 0.65, 0.69),
            Placement(0.45, 0.65, 0.69)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("tailor-judoka.png")),
            Placement(0.85, 0.8, 0.85),
            Placement(0.85, 0.8, 0.85)
        )

        scene.add_widget(
            SpeechBubble(
                text="You look amazing!",
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.9, 0.4),
            Placement(0.9, 0.4)
        )

        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.95, 0),
            Placement(0.45, 0.95, 0),
            self.next_stage,
            key=Gdk.KEY_space
        )

        return scene

    def _next_stage_wrapper(self, widget, event):
        self.next_stage()
