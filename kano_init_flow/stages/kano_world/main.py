# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import subprocess
from gi.repository import Gtk, Gdk

from kano.gtk3.buttons import KanoButton
from kano.utils import play_sound

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class, cb_wrapper, scale_image
from kano_init_flow.ui.css import apply_styling_to_screen


class KanoWorld(Stage):
    """
        The overscan setting window
    """

    id = 'kano-world'
    _root = __file__

    def __init__(self, ctl):
        super(KanoWorld, self).__init__(ctl)
        # This doesn't exist yet
        # apply_styling_to_screen(self.css_path('kano-world.css'))

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def _setup_first_scene(self):
        self._is_on = False

        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(
            self.media_path('world-registration-scene-1600x1200.png'),
            self.media_path('world-registration-scene-1920x1080.png')
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('rocket-animation-file-medium.gif')),
            Placement(0.05, 0.5),
            Placement(0.05, 0.5)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('world-widget-animation.gif')),
            Placement(0.95, 0.05),
            Placement(0.95, 0.05)
        )

        # Launch the settings on top
        subprocess.Popen(['/usr/bin/kano-login', '-r'])

        return scene
