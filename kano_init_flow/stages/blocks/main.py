# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk, GdkPixbuf
from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.drag_classes import DragSource, DropArea
from kano_init_flow.ui.components import NextButton


class Blocks(Stage):
    """
        The overscan setting window
    """

    id = 'blocks'
    _root = __file__

    def __init__(self, ctl):
        super(Blocks, self).__init__(ctl)

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def second_scene(self):
        s = self._setup_second_scene()
        self._ctl.main_window.push(s.widget)

    def third_scene(self):
        s = self._setup_third_scene()
        self._ctl.main_window.push(s.widget)

    def fourth_scene(self):
        s = self._setup_fourth_scene()
        self._ctl.main_window.push(s.widget)

    def fifth_scene(self):
        s = self._setup_fifth_scene()
        self._ctl.main_window.push(s.widget)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_base_temple_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('blocks-scene-incomplete-1600x1200.png'),
                             self.media_path('blocks-scene-incomplete-1920x1080.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("boulder.png")),
            Placement(0.65, 0.47),
            Placement(0.63, 0.44)
        )

        scene.add_widget(
            scene.get_user_character_image(),
            Placement(0.22, 0.55, 0.52),
            Placement(0.22, 0.6, 0.52)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("mage-doka.png")),
            Placement(0.8, 0.55),
            Placement(0.8, 0.6)
        )

        return scene

    def _setup_first_scene(self):
        scene = self._setup_base_temple_scene()

        copy = [
            'Oh no, there\'s a boulder',
            'in the way!'
        ]
        scene.add_widget(
            SpeechBubble(
                text='\n'.join(copy),
                source=SpeechBubble.BOTTOM,
                source_align=0.5,
                scale=scene.scale_factor
            ),
            Placement(0.85, 0.23),
            Placement(0.85, 0.23)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("altar-still.png")),
            Placement(0.41, 0.55, 1),
            Placement(0.41, 0.65, 1)
        )

        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.87, 0),
            Placement(0.5, 0.87, 0),
            self.second_scene
        )

        return scene

    def _setup_second_scene(self):
        scene = self._setup_base_temple_scene()

        copy = [
            'But don\'t worry, you can',
            'use Kano blocks to create code',
            'to change what\'s around you.\n',
            'Looks like there\'s one over there!'
        ]
        scene.add_widget(
            SpeechBubble(
                text='\n'.join(copy),
                source=SpeechBubble.BOTTOM,
                source_align=0.5,
                scale=scene.scale_factor
            ),
            Placement(0.88, 0.15, 0),
            Placement(0.88, 0.15, 0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("altar.gif")),
            Placement(0.41, 0.55, 1),
            Placement(0.41, 0.65, 1),
            self.third_scene
        )

        return scene

    def _setup_third_scene(self):
        scene = Scene()

        scene.set_background(common_media_path("blueprint-bg-4-3.png"),
                             common_media_path("blueprint-bg-16-9.png"))

        # Altar
        scene.add_widget(Gtk.Image.new_from_file(self.media_path('altar-incomplete.png')),
                         Placement(0.5, 0.5, 1),
                         Placement(0.5, 0.5, 1))

        # Block image for drag source
        block_image = scene.scale_image_to_scene(
            Gtk.Image.new_from_file(self.media_path("kano-block.png")),
            1,
            1
        )

        block_pixbuf = scene.scale_pixbuf_to_scene(
            GdkPixbuf.Pixbuf.new_from_file(self.media_path("kano-block.png")),
            1,
            1
        )

        block_drag_source = DragSource(block_image, block_pixbuf)

        scene.add_widget(
            block_drag_source,
            Placement(0.5, 0.68, 0),
            Placement(0.5, 0.68, 0)
        )

        # Block drop area
        drop_area = DropArea(self.fourth_scene)
        drop_area_width = scene.get_width() * 0.24
        drop_area_height = scene.get_height() * 0.08
        drop_area.set_size_request(drop_area_width, drop_area_height)

        scene.add_widget(
            drop_area,
            Placement(0.505, 0.47, 0),
            Placement(0.505, 0.47, 0)
        )

        return scene

    def _setup_fourth_scene(self):
        scene = Scene()
        scene.set_background(common_media_path("blueprint-bg-4-3.png"),
                             common_media_path("blueprint-bg-16-9.png"))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("altar-complete.png")),
            Placement(0.5, 0.5, 1),
            Placement(0.5, 0.5, 1),
        )

        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.9, 0),
            Placement(0.5, 0.9, 0),
            self.fifth_scene
        )

        return scene

    def _setup_fifth_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('blocks-scene-complete-1600x1200.png'),
                             self.media_path('blocks-scene-complete-1920x1080.png'))

        # Move boulder
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("boulder.png")),
            Placement(0.8, 0.44),
            Placement(0.8, 0.44)
        )

        scene.add_widget(
            scene.get_user_character_image(),
            Placement(0.22, 0.55, 0.52),
            Placement(0.22, 0.6, 0.52)
        )

        scene.add_widget(
            SpeechBubble(
                text="Awesome, now we can escape!",
                source=SpeechBubble.BOTTOM,
                source_align=0.5,
                scale=scene.scale_factor
            ),
            Placement(0.85, 0.25, 0),
            Placement(0.85, 0.25, 0)
        )

        # Change mage face?
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("mage-doka.png")),
            Placement(0.8, 0.55),
            Placement(0.8, 0.6)
        )

        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.8, 0),
            Placement(0.5, 0.87, 0),
            self.next_stage
        )

        return scene
