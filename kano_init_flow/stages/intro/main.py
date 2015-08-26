# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.paths import common_media_path


class Intro(Stage):
    """
        The first screen where the judoka introduces himself
    """

    id = 'intro'
    _root = __file__

    def __init__(self, ctl):
        super(Intro, self).__init__(ctl)
        apply_styling_to_screen(self.css_path("intro.css"))

    def first_scene(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1.widget)

    def second_scene(self):
        s2 = self._setup_second_scene()
        self._ctl.main_window.push(s2.widget)

    def third_scene(self):
        s3 = self._setup_third_scene()
        self._ctl.main_window.push(s3.widget)

    def fourth_scene(self):
        s4 = self._setup_fourth_scene()
        self._ctl.main_window.push(s4.widget)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        # Grey overlay
        blur = Gtk.EventBox()
        blur.get_style_context().add_class("blur")
        screen = Gdk.Screen.get_default()
        width = screen.get_width()
        height = screen.get_height()
        blur.set_size_request(width, height)

        scene.add_widget(
            blur,
            Placement(0, 0, 0),
            Placement(0, 0, 0),
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("keyboard-intro.gif")),
            Placement(0.5, 0.45, 0),
            Placement(0.5, 0.45, 0),
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path('next-button.gif')),
            Placement(0.5, 0.75, 0),
            Placement(0.5, 0.75, 0),
            self.second_scene
        )

        grab_label = Gtk.Label("GRAB YOUR KEYBOARD")
        grab_label.get_style_context().add_class("big_intro_label")
        click_label = Gtk.Label("CLICK")
        click_label.get_style_context().add_class("intro_label")
        move_label = Gtk.Label("MOVE")
        move_label.get_style_context().add_class("intro_label")

        scene.add_widget(
            grab_label,
            Placement(0.5, 0.25, 0),
            Placement(0.5, 0.25, 0)
        )

        scene.add_widget(
            click_label,
            Placement(0.25, 0.63, 0),
            Placement(0.315, 0.63, 0)
        )

        scene.add_widget(
            move_label,
            Placement(0.72, 0.63, 0),
            Placement(0.665, 0.63, 0)
        )

        return scene

    def _setup_second_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            SpeechBubble(
                text="Well done! You brought your\nKano to life! I'm Judoka and I\nwill be your guide through the\nworld of Kano.",
                source=SpeechBubble.LEFT
            ),
            Placement(0.72, 0.35),
            Placement(0.68, 0.3)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('intro-gif-1.gif')),
            Placement(0.33, 0.4, 0),
            Placement(0.4, 0.4, 0),
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.5, 0.78, 0),
            Placement(0.5, 0.8, 0),
            self.third_scene
        )

        return scene

    def _setup_third_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            SpeechBubble(
                text="Kano is a world where anything\nis possible!\nJudokas can make and play\nusing code powers.",
                source=SpeechBubble.RIGHT
            ),
            Placement(0.36, 0.4, 0),
            Placement(0.4, 0.3, 0),
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('intro-gif-2.gif')),
            Placement(0.71, 0.4, 0),
            Placement(0.63, 0.4, 0),
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.5, 0.78, 0),
            Placement(0.5, 0.8, 0),
            self.fourth_scene
        )

        return scene

    def _setup_fourth_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            SpeechBubble(
                text='Ready to go? Jump on in!',
                source=SpeechBubble.LEFT
            ),
            Placement(0.7, 0.35),
            Placement(0.65, 0.3)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('intro-gif-3.gif')),
            Placement(0.33, 0.3, 0),
            Placement(0.42, 0.27, 0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.5, 0.78, 0),
            Placement(0.5, 0.8, 0),
            self.next_stage
        )

        return scene
