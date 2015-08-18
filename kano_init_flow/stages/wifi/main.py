# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk


from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path


class Wifi(Stage):
    """
        The internet connection stage
    """

    id = 'wifi'
    _root = __file__

    def __init__(self, ctl):
        super(Wifi, self).__init__(ctl)

    def first_step(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1.widget)

    def second_step(self):
        s2 = self._setup_second_scene()
        self._ctl.main_window.push(s2.widget)

    def third_step(self):
        s3 = self._setup_third_scene()
        self._ctl.main_window.push(s3.widget)

    def next_step(self):
        self._stage.ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('space-1-bg-4-3.png'),
                             self.media_path('space-1-bg-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('character.png')),
            Placement(0.08, 0.9, 0.45),
            Placement(0.12, 0.9, 0.5)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.png')),
            Placement(0.9, 0.9, 0.65),
            Placement(0.9, 0.9, 0.75)
        )

        scene.add_widget(
            SpeechBubble(text='Wicked', source=SpeechBubble.RIGHT),
            Placement(0.78, 0.72),
            Placement(0.79, 0.68)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('console.gif')),
            Placement(0.35, 0.925, 0.8),
            Placement(0.367, 0.888),
            self.second_step
        )

        return scene

    def _setup_second_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('console-large.png')),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0),
            self.third_step
        )

        """
        x, y = img.get_size()
        # the widget will be fixed
        wifi_flow = WifiFlow(x, y)
        scene.add_widget(
            wifi_flow,
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0),
            self.third_step
        )
        """

        return scene

    def _setup_third_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('space-2-bg-4-3.png'),
                             self.media_path('space-2-bg-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('character.png')),
            Placement(0.08, 0.9, 0.45),
            Placement(0.12, 0.9, 0.5)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.png')),
            Placement(0.9, 0.9, 0.65),
            Placement(0.9, 0.9, 0.75)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('rocket.gif')),
            Placement(0.697, 0.597, 0.8),
            Placement(0.695, 0.275),
            self.first_step
        )

        scene.add_widget(
            SpeechBubble(text='Wicked', source=SpeechBubble.RIGHT),
            Placement(0.78, 0.72),
            Placement(0.79, 0.68)
        )

        return scene
