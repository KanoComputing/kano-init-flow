# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk, GdkPixbuf

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.ui.css import apply_styling_to_screen
from kano.gtk3.cursor import attach_cursor_events

from kano.logging import logger


class DragAndDrop(Stage):
    """
        The internet connection stage
    """

    id = 'drag-and-drop'
    _root = __file__

    def __init__(self, ctl):
        super(DragAndDrop, self).__init__(ctl)
        apply_styling_to_screen(self.css_path("drag-and-drop.css"))

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
        char_pixbuf = Scene.scale_pixbuf_to_scene(char_pixbuf, 0.6, 0.8)
        judoka = Gtk.Image.new_from_file(self.media_path('cliff-judoka.png'))
        judoka = Scene.scale_image_to_scene(judoka, 0.6, 0.8)
        speechbubble = SpeechBubble(
            text='Jump Willy!',
            source=SpeechBubble.BOTTOM
        )
        drag_source = DragSource(judoka, char_pixbuf, speechbubble)

        # Send the second cb to the scene
        drop_area = DropArea(self.second_scene)
        drop_area.set_size_request(
            0.4 * Gdk.Screen.width(), 0.5 * Gdk.Screen.height()
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('keyboard.gif')),
            Placement(0.5, 0.9, 0),
            Placement(0.5, 0.9, 0)
        )

        scene.add_widget(
            speechbubble,
            Placement(0.22, 0.05),
            Placement(0.24, 0.03)
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
        scene = Scene()
        scene.set_background(self.media_path('cliff-file-1600x1200.png'),
                             self.media_path('cliff-file-1920x1080.png'))

        scene.add_widget(
            SpeechBubble(text='Well done!', source=SpeechBubble.BOTTOM),
            Placement(0.86, 0.06),
            Placement(0.91, 0.1)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('cliff-judoka.png')),
            Placement(0.85, 0.3, 0.92),
            Placement(0.9, 0.35, 0.96)
        )

        next_button = Gtk.Button()
        next_button.set_image(Gtk.Image.new_from_file(
            self.media_path("next-button.png"))
        )
        next_button.connect("button-release-event", self._next_stage_wrapper)
        attach_cursor_events(next_button)
        scene.add_widget(
            next_button,
            Placement(0.85, 0.8),
            Placement(0.9, 0.85)
        )

        return scene

    def _next_stage_wrapper(self, widget, event):
        self.next_stage()


class DragSource(Gtk.EventBox):
    """
    The object which is dragged from the source to the destination.
    """

    # Pass the scaled images into the class
    def __init__(self, image, pixbuf, speechbubble):
        Gtk.EventBox.__init__(self)
        attach_cursor_events(self)

        self.speechbubble = speechbubble
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
        self.speechbubble.hide()
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
        self.speechbubble.show()
        self.show_all()

    def on_drag_delete(self, *_):
        """ Triggered when the drag action is completed successfully """

        logger.info("Drag deleted")
        self.destroy()


class DropArea(Gtk.EventBox):
    """
    Area which the user has to drag the Judoka into
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
