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


class PiAudio(Stage):
    """
        The overscan setting window
    """

    id = 'pi-audio'
    _root = __file__

    def __init__(self, ctl):
        super(PiAudio, self).__init__(ctl)

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
            Gtk.Image.new_from_file(self.media_path('pi-sound.png')),
            Placement(0.67, 0.0),
            Placement(0.5, 0.0)
        )

        scene.add_widget(
            ActiveImage(self.media_path('audio.gif'),
                        hover=self.media_path('audio-hover.gif')),
            Placement(0.542, 0.28),
            Placement(0.4468, 0.32),
            self.next_stage
        )

        scene.add_arrow(
            "down",
            Placement(0.542, 0.05, 0),
            Placement(0.445, 0.13, 0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path('pi-judoka.png')),
            Placement(0.2, 0.6),
            Placement(0.16, 0.6)
        )

        sb = SpeechBubble('Let\'s make sure our sound\nis loud and clear.',
                          scale=scene.scale_factor)
        scene.add_widget(
            sb,
            Placement(0.1, 0.2),
            Placement(0.105, 0.26)
        )

        scene.schedule(40, self._show_hint, sb)

        return scene

    def _show_hint(self, sb):
        sb.set_text('Click on the blue cable\nto continue.')
