# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk

from kano.gtk3.buttons import KanoButton
from kano.utils import is_monitor
from kano_settings.system.display import get_overscan_status, \
    write_overscan_values, set_overscan_status, launch_pipe


from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.ui.utils import cb_wrapper


class Bugs(Stage):
    """
        The overscan setting window
    """

    id = 'bugs'
    _root = __file__

    def __init__(self, ctl):
        super(Bugs, self).__init__(ctl)

        apply_styling_to_screen(self.css_path('bugs.css'))

        self._zapped = 0
        self._total_bugs = 3

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('forest-4-3.png'),
                             self.media_path('forest-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('left-bug.png')),
            Placement(0.03, 0.1),
            Placement(0.05, 0.2),
            [self._bug_zapped, scene, 'left-bug'],
            name='left-bug'
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('middle-bug.gif')),
            Placement(0.47, 0.45),
            Placement(0.47, 0.49),
            [self._bug_zapped, scene, 'middle-bug'],
            name='middle-bug'
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('right-bug.png')),
            Placement(0.9, 0.05),
            Placement(0.955, 0.04),
            [self._bug_zapped, scene, 'right-bug'],
            name='right-bug'
        )

        self._place_judoka_into_scene(scene)

        return scene

    def _place_judoka_into_scene(self, scene, happy=False):
        image = 'judoka-scared.png'
        copy = 'Arrgh!\nLook at the size of those pesky bugs.\n\n' + \
               'I can\'t reach them from here,\n' + \
               'help me get rid of them, quick!'
        if happy:
            image = 'judoka.png'
            copy = 'Great work!\n\nThere\'s nothing worse than\n' + \
                   'a computer full of bugs.'

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path(image)),
            Placement(0.9, 0.9),
            Placement(0.9, 0.9),
            name='judoka'
        )

        scene.add_widget(
            SpeechBubble(
                text=copy,
                source=SpeechBubble.RIGHT,
                source_align=0.0
            ),
            Placement(0.65, 0.76),
            Placement(0.74, 0.74),
            name='speech-bubble'
        )

    def _bug_zapped(self, scene, wid):
        self._zapped += 1
        scene.remove_widget(wid)

        if self._zapped >= self._total_bugs:
            scene.remove_widget('judoka')
            scene.remove_widget('speech-bubble')
            self._place_judoka_into_scene(scene, True)

            scene.add_widget(
                Gtk.Image.new_from_file(common_media_path('next-button.gif')),
                Placement(0.5, 0.9, 0),
                Placement(0.5, 0.9, 0),
                self._ctl.next_stage
            )
