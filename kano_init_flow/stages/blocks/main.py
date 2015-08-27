# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk, GdkPixbuf

from kano.gtk3.cursor import attach_cursor_events
from kano.logging import logger
from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
# from kano_init_flow.ui.css import apply_styling_to_screen


class Blocks(Stage):
    """
        The overscan setting window
    """

    id = 'blocks'
    _root = __file__

    def __init__(self, ctl):
        super(Blocks, self).__init__(ctl)

        # apply_styling_to_screen(self.css_path('blocks.css'))

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
        scene.set_background(self.media_path('scene-1600x1200.png'),
                             self.media_path('scene-1920x1080.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("boulder.png")),
            Placement(0.4, 0.2),
            Placement(0.63, 0.44)
        )

        scene.add_widget(
            scene.get_user_character_image(),
            Placement(0.2, 0.2),
            Placement(0.22, 0.6, 0.52)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("mage-doka.png")),
            Placement(0.46, 0.25),
            Placement(0.8, 0.6)
        )

        return scene

    def _setup_first_scene(self):
        scene = self._setup_base_temple_scene()

        scene.add_widget(
            SpeechBubble(
                text="Oh no, there's a boulder" +
                     "\nblocking our exit!",
                source=SpeechBubble.BOTTOM,
                source_align=0.5
            ),
            Placement(0.4, 0.2, 0),
            Placement(0.85, 0.25, 0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.5, 0.7, 0),
            Placement(0.5, 0.87, 0),
            self.second_scene
        )

        # Add static image of altar

        return scene

    def _setup_second_scene(self):
        scene = self._setup_base_temple_scene()

        scene.add_widget(
            SpeechBubble(
                text="But don\'t worry,"
                     "\nJudokas can use code blocks" +
                     "\nto change the world around them." +
                     "\n\nLooks like there is one over there.",
                source=SpeechBubble.BOTTOM,
                source_align=0.5
            ),
            Placement(0.46, 0.25, 0),
            Placement(0.88, 0.15, 0)
        )

        # Add moving image of altar. For now use next button.
        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.5, 0.7, 0),
            Placement(0.5, 0.87, 0),
            self.third_scene
        )

        return scene

    def _setup_third_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('altar-screen-incomplete-1600x1200.png'),
                             self.media_path('altar-screen-incomplete.png'))

        block_image = scene.scale_image_to_scene(
            Gtk.Image.new_from_file(self.media_path("kano-block.png")),
            0.7,
            0.9
        )

        block_pixbuf = scene.scale_pixbuf_to_scene(
            GdkPixbuf.Pixbuf.new_from_file(self.media_path("kano-block.png")),
            0.7,
            0.9
        )

        # TODO: Add drop area
        block_drag_source = DragSource(block_image, block_pixbuf)

        # Make into drag source
        scene.add_widget(
            block_drag_source,
            Placement(0.46, 0.25),
            Placement(0.44, 0.15)
        )

        drop_area = DropArea(self.fourth_scene)

        # Make this a percentage of the screen size
        screen = Gdk.Screen.get_default()
        drop_area_width = screen.get_width() * 0.2
        drop_area_height = screen.get_height() * 0.07
        drop_area.set_size_request(drop_area_width, drop_area_height)

        scene.add_widget(
            drop_area,
            Placement(0.46, 0.25, 0),
            Placement(0.54, 0.48, 0)
        )

        return scene

    def _setup_fourth_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('altar-screen-complete-1600x1200.png'),
                             self.media_path('altar-screen-complete.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.5, 0.75, 0),
            Placement(0.55, 0.9, 0),
            self.fifth_scene
        )

        return scene

    def _setup_fifth_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('scene-1600x1200.png'),
                             self.media_path('scene-1920x1080.png'))

        # Move boulder
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("boulder.png")),
            Placement(0.46, 0.25),
            Placement(0.8, 0.44)
        )

        scene.add_widget(
            scene.get_user_character_image(),
            Placement(0.2, 0.2),
            Placement(0.22, 0.6, 0.52)
        )

        scene.add_widget(
            SpeechBubble(
                text="Well done, now you can escape!",
                source=SpeechBubble.BOTTOM,
                source_align=0.5
            ),
            Placement(0.46, 0.25, 0),
            Placement(0.85, 0.25, 0)
        )

        # Change mage face?
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("mage-doka.png")),
            Placement(0.46, 0.25),
            Placement(0.8, 0.6)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.5, 0.7, 0),
            Placement(0.5, 0.87, 0),
            self.next_stage
        )

        return scene


# TODO: these need to be moved to a common place, this is duplicate of code
# in the drag and drop screen.
class DragSource(Gtk.EventBox):
    """
    The object which is dragged from the source to the destination.
    """

    # Pass the scaled images into the class
    def __init__(self, image, pixbuf):
        Gtk.EventBox.__init__(self)
        attach_cursor_events(self)

        self.image = image
        self.add(image)

        # This follows the cursor when the item is being dragged
        self.pixbuf = pixbuf
        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                             Gdk.DragAction.ASK)

        # To send image data
        self.drag_source_add_image_targets()
        self.connect("drag-begin", self.on_drag_begin)
        self.connect("drag-data-get", self.on_drag_data_get)
        self.connect("drag-failed", self.on_drag_fail)
        self.connect("drag-end", self.on_drag_end)
        self.connect("drag-data-delete", self.on_drag_delete)

    def on_drag_begin(self, _, drag_context):
        """ Triggered when dragging starts """

        logger.info("Drag has begun")

        # (120, 90) refers to where the cursor relative to the drag icon
        Gtk.drag_set_icon_pixbuf(drag_context, self.pixbuf, 50, 50)
        self.remove(self.image)
        self.show_all()

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        """ Passes the drag data to the drop area """

        logger.info("Data is sent from source")
        data.set_pixbuf(self.pixbuf)

    @staticmethod
    def on_drag_fail(drag_context, drag_result, data):
        """ Handles when the Judoka isn't dragged to the drop area """

        logger.info("Drag failed")
        logger.info(data)

    def on_drag_end(self, *_):
        """ Triggered when the drag action is terminated """

        logger.info("Drag ended")
        self.add(self.image)
        self.show_all()

    def on_drag_delete(self, *_):
        """ Triggered when the drag action is completed successfully """

        logger.info("Drag deleted")
        self.destroy()


class DropArea(Gtk.Button):
    """
    Area which the user has to drag the block into
    """

    def __init__(self, next_cb):
        super(DropArea, self).__init__()

        self.next_cb = next_cb
        self.get_style_context().add_class("drag_dest")

        self.drag_dest_set(
            Gtk.DestDefaults.MOTION | Gtk.DestDefaults.DROP,
            [],
            Gdk.DragAction.ASK
        )

        targets = Gtk.TargetList.new([])
        targets.add_image_targets(2, True)
        self.drag_dest_set_target_list(targets)

        self.connect("drag-data-received", self.on_drag_data_received)

    def on_drag_data_received(self, widget, drag_context, x, y,
                              data, info, time):
        """
        Triggered whenever new drag data is received. If the Judoka
        has been successfully dragged then move on to the next stage
        """

        logger.info("Drop area has received data")
        if info == 2:
            drag_context.finish(True, True, time)
            self.next_cb()
