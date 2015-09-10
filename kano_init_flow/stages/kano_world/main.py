# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import threading
import subprocess
from gi.repository import Gtk, GLib

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano.logging import logger

from kano.network import is_internet


class KanoWorld(Stage):
    """
        The overscan setting window
    """

    id = 'kano-world'
    _root = __file__

    def __init__(self, ctl):
        super(KanoWorld, self).__init__(ctl)
        self._ctl = ctl

    def first_scene(self):
        if not is_internet():
            self.next_stage()
            return

        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def next_stage(self):
        self._ctl.next_stage()

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
        thread = threading.Thread(target=self.launch_registration)
        thread.daemon = True
        thread.start()

        return scene

    def launch_registration(self):
        try:
            p = subprocess.Popen(['/usr/bin/kano-login', '-r'])
            p.wait()
        except Exception:
            logger.debug("kano-login failed to launch")

        GLib.idle_add(self.next_stage)
