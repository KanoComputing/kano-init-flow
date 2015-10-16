# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, ActiveImage
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.speech_bubble import SpeechBubble


class PiKeyboard(Stage):
    """
        The overscan setting window
    """

    id = 'pi-keyboard'
    _root = __file__

    def __init__(self, ctl):
        super(PiKeyboard, self).__init__(ctl)

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):

        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(
            common_media_path('blueprint-bg-4-3.png'),
            common_media_path('blueprint-bg-16-9.png')
        )

        scene.add_widget(
            ActiveImage(self.media_path('keyboard.gif'),
                        hover=self.media_path('keyboard-hover.gif')),
            Placement(0.43, 0.70),
            Placement(0.4, 0.79),
            self.next_stage
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('pi-keyboard.png')),
            Placement(0.67, 0),
            Placement(0.55, 0)
        )

        scene.add_arrow(
            "right",
            Placement(0.25, 0.69, 0),
            Placement(0.28, 0.775, 0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(
                common_media_path('down-right-pointing-judoka.png')
            ),
            Placement(0.15, 0.45),
            Placement(0.2, 0.5)
        )

        scene.add_widget(
            SpeechBubble('CLICK on the keyboard dongle',
                         scale=scene.scale_factor),
            Placement(0.08, 0.2),
            Placement(0.15, 0.18)
        )

        return scene
