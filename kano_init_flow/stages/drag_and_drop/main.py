# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, GdkPixbuf, Gdk

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, SCREEN_WIDTH, \
    SCREEN_HEIGHT
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano.gtk3.cursor import attach_cursor_events
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.drag_classes import DragSource, DropArea
from kano_init_flow.ui.components import NextButton


class DragAndDrop(Stage):
    """
        The tutorial for drag and drop
    """

    id = 'drag-and-drop'
    _root = __file__

    def __init__(self, ctl):
        super(DragAndDrop, self).__init__(ctl)

    def first_scene(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1.widget)

    def second_scene(self):
        s2 = self._setup_second_scene()
        self._ctl.main_window.push(s2.widget)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('cliff-file-1600x1200.png'),
                             self.media_path('cliff-file-1920x1080.png'))

        char_pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            self.media_path('judoka-clicked.png')
        )
        char_pixbuf = scene.scale_pixbuf_to_scene(char_pixbuf, 0.6, 0.8)
        judoka = Gtk.Image.new_from_file(self.media_path('cliff-judoka.png'))
        judoka = scene.scale_image_to_scene(judoka, 0.6, 0.8)
        speechbubble = SpeechBubble(
            text='I need to cross this!\n\nClick and drag me to\n' +
                 'the other side.',
            source=SpeechBubble.LEFT,
            source_align=0.0,
            scale=scene.scale_factor
        )
        keyboard = Gtk.Image.new_from_file(self.media_path('keyboard.gif'))

        drag_source = DragSource(judoka, char_pixbuf, speechbubble, keyboard)

        # Send the second cb to the scene
        drop_area = DropArea(self.second_scene)
        drop_area.set_size_request(
            0.35 * SCREEN_WIDTH, 0.5 * SCREEN_HEIGHT
        )

        scene.add_widget(
            keyboard,
            Placement(0.5, 0.9, 0),
            Placement(0.5, 0.9, 0)
        )

        scene.add_widget(
            speechbubble,
            Placement(0.46, 0.25),
            Placement(0.44, 0.25)
        )

        scene.add_widget(
            drag_source,
            Placement(0.25, 0.25),
            Placement(0.25, 0.25)
        )

        scene.add_widget(
            drop_area,
            Placement(1, 0),
            Placement(1, 0)
        )

        return scene

    def _setup_second_scene(self):
        scene = Scene(self._ctl.main_window)
        scene.set_background(self.media_path('cliff-file-1600x1200.png'),
                             self.media_path('cliff-file-1920x1080.png'))

        scene.add_widget(
            SpeechBubble(text='Thanks!', source=SpeechBubble.BOTTOM,
                         scale=scene.scale_factor),
            Placement(0.86, 0.06),
            Placement(0.91, 0.1)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('cliff-judoka.png')),
            Placement(0.85, 0.3, 0.92),
            Placement(0.9, 0.35, 0.96)
        )

        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.7, 0),
            Placement(0.5, 0.7, 0),
            self.next_stage,
            key=Gdk.KEY_space
        )

        return scene
