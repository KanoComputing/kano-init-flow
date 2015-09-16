# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.speech_bubble import SpeechBubble


class PiHdmi(Stage):
    """
        The overscan setting window
    """

    id = 'pi-hdmi'
    _root = __file__

    def __init__(self, ctl):
        super(PiHdmi, self).__init__(ctl)

    def first_scene(self):
        # Check if the pi is connected to a monitor
        #if is_monitor():
        #    self._ctl.next_stage()

        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):

        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(
            common_media_path('blueprint-bg-4-3.png'),
            common_media_path('blueprint-bg-16-9.png')
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('HDMI-cable-cut.gif')),
            Placement(0.68, 0),
            Placement(0.6, 0),
            self.next_stage
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('HDMI-pi-image.png')),
            Placement(0.65, 0.15),
            Placement(0.52, 0.2)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path('pi-judoka.png')),
            Placement(0.18, 0.6),
            Placement(0.18, 0.6)
        )

        scene.add_widget(
            SpeechBubble('Let\'s configure the HDMI!'),
            Placement(0.08, 0.3),
            Placement(0.14, 0.3)
        )

        return scene
