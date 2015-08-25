# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk

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

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            SpeechBubble(
                text="Hi, I'm the Judoka and\nI'll show you a world\nblah blah blah",
                source=SpeechBubble.LEFT
            ),
            Placement(0.68, 0.35),
            Placement(0.65, 0.35)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('intro-gif-1.gif')),
            Placement(0.35, 0.5, 0),
            Placement(0.4, 0.5, 0),
            self.second_scene
        )

        return scene

    def _setup_second_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            SpeechBubble(
                text='Whoooooop boom boom!',
                source=SpeechBubble.LEFT
            ),
            Placement(0.68, 0.35),
            Placement(0.65, 0.35)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('intro-gif-2.gif')),
            Placement(0.39, 0.5, 0),
            Placement(0.425, 0.5, 0),
            self.third_scene
        )

        return scene

    def _setup_third_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            SpeechBubble(
                text='Scene 3',
                source=SpeechBubble.LEFT
            ),
            Placement(0.65, 0.35),
            Placement(0.65, 0.35)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('intro-gif-3.gif')),
            Placement(0.37, 0.42, 0),
            Placement(0.42, 0.42, 0),
            self.next_stage
        )

        return scene
