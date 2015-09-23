# The pi complete stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path


class PiComplete(Stage):
    """
        The overscan setting window
    """

    id = 'pi-complete'
    _root = __file__

    def __init__(self, ctl):
        super(PiComplete, self).__init__(ctl)

    def first_scene(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1)

    def _setup_first_scene(self):
        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('pi-complete.png')),
            Placement(0.25, 0.2),
            Placement(0.3, 0.2),
            self._ctl.next_stage
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('left-pointing-judoka.png')),
            Placement(0.8, 0.6),
            Placement(0.75, 0.6)
        )

        scene.add_widget(
            SpeechBubble(
                text='You set it up! Now it\'s time to play.\n' +
                     'Let\'s go!',
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.83, 0.3),
            Placement(0.83, 0.2)
        )

        return scene
