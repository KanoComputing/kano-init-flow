# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, GdkPixbuf


from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Position


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

    def next_step(self):
        self._stage.ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('space-1-bg-4-3.png'),
                             self.media_path('space-1-bg-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('character.png')),
            Position(0.07, 0.6, 0.35),
            Position(0.15, 0.6, 0.5)
        )

        scene.add_widget(
            GdkPixbuf.PixbufAnimation.new_from_file(
                self.media_path('console.gif')
            ),
            Position(0.315, 0.58, 0.55),
            Position(0.82, 0.55, 0.8),
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.svg')),
            Position(0.7, 0.55, 1.0),
            Position(0.82, 0.55, 1.5)
        )

        return scene
