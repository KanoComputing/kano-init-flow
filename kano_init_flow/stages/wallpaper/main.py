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

from kano.utils import run_cmd


class Wallpaper(Stage):
    """
        Set the desktop wallpaper
    """

    id = 'wallpaper'
    _root = __file__

    def __init__(self, ctl):
        super(Wallpaper, self).__init__(ctl)

    def first_scene(self):
        self._ctl.main_window.hide()
        while Gtk.events_pending():
            Gtk.main_iteration()
        run_cmd('kdesk -w')
        run_cmd('sudo kano-settings first-boot-set-wallpaper')
        self._ctl.main_window.show()
        self.next_stage()

    def next_stage(self):
        self._ctl.next_stage()
