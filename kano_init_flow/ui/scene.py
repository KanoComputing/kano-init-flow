# The base class for implementing scenes
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import time

from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from kano.gtk3.cursor import attach_cursor_events

from kano_init_flow.ui.utils import scale_image, scale_pixbuf, add_class

from kano_avatar.paths import AVATAR_DEFAULT_LOC, AVATAR_DEFAULT_NAME


# TODO: for debuging of different screen ratios
SCREEN_WIDTH = Gdk.Screen.width()
SCREEN_HEIGHT = Gdk.Screen.height()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Placement(object):
    def __init__(self, x=0, y=0, scale=1.0):
        self._x = x
        self._y = y

        # scale = 0.0 means fixed size
        self._scale = scale

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def scale(self):
        return self._scale


class Scene(object):
    """
        The base class for implementing scenes.
    """

    RATIO_4_3 = 4.0 / 3
    RATIO_16_9 = 16.0 / 9

    def __init__(self, main_window=None):
        self._screen_ratio = self._get_screen_ratio()
        self._scale_factor = self._get_scale_factor()

        self._widgets = {}

        if main_window:
            self._keys = {}
            main_window.set_key_events_handler(self._keypress_cb_wrapper)

        self._overlay = Gtk.Overlay()

        self._background = Gtk.Image()
        self._background.set_halign(Gtk.Align.START)
        self._background.set_valign(Gtk.Align.START)
        self._overlay.add(self._background)

        self._last_motion = time.time()

        self._fixed = Gtk.Fixed()
        self._overlay.add_overlay(self._fixed)

    def _get_scale_factor(self):
        if self._screen_ratio == self.RATIO_4_3:
            return SCREEN_HEIGHT / 1200.0
        return SCREEN_HEIGHT / 1080.0

    def set_background(self, ver_43, ver_169):
        """
            Set the background of the scene.

            :param ver_43: Path to the 4:3 version of the background.
            :type ver_43: str

            :param ver_169: Path to the 16:9 version of the background.
            :type ver_169: str
        """

        w = SCREEN_WIDTH
        h = SCREEN_HEIGHT

        bg_path = ver_43 if self._screen_ratio == self.RATIO_4_3 else ver_169
        bg_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(bg_path, w, h)
        self._background.set_from_pixbuf(bg_pixbuf)

    def add_widget(self, widget, p43, p169, clicked_cb=None, key=None, name=None, modal=False):
        placement = p43 if self._screen_ratio == self.RATIO_4_3 else p169

        final_scale = placement.scale * self._scale_factor
        if final_scale != 1 and placement.scale != 0:
            if widget.__class__.__name__ == "Image":
                if widget.get_animation():
                    widget = self._scale_gif(widget, final_scale)
                else:
                    widget = scale_image(widget, final_scale)
            else:
                if placement.scale != 1.0:
                    raise RuntimeError('Can\'t scale regular widgets!')

        root_widget = widget
        if clicked_cb:
            # TODO: Add custom styling to this.
            button_wrapper = Gtk.Button()
            button_wrapper.add(root_widget)
            attach_cursor_events(button_wrapper)
            root_widget = button_wrapper

            if isinstance(clicked_cb, (list, tuple)):
                button_wrapper.connect('clicked', self._clicked_cb_wrapper,
                                       clicked_cb[0], *clicked_cb[1:])
            else:
                button_wrapper.connect('clicked', self._clicked_cb_wrapper,
                                       clicked_cb)

            if key is not None:
                if not hasattr(self, '_keys'):
                    raise RuntimeError('Scene must be initialised with main_window to be able to receive key events.')
                self._keys[key] = clicked_cb

        align = Gtk.Alignment.new(placement.x, placement.y, 0, 0)
        align.add(root_widget)
        align.set_size_request(SCREEN_WIDTH, SCREEN_HEIGHT)

        wrapper = align
        if modal:
            wrapper = Gtk.EventBox()
            add_class(wrapper, 'modal')
            wrapper.add(align)

        wrapper.show_all()
        self._fixed.put(wrapper, 0, 0)

        if name is not None:
            self._widgets[name] = wrapper

    def remove_widget(self, wid):
        """
            :param wid: The id assigned to the widget when it was added to
                        the scene.
            :type wid: str
        """

        if wid in self._widgets:
            w = self._widgets[wid]
            del self._widgets[wid]
            self._fixed.remove(w)

    def _clicked_cb_wrapper(self, widget, clicked_cb, *args):
        clicked_cb(*args)
        return True

    def _keypress_cb_wrapper(self, widget, event):
        if hasattr(event, 'keyval'):
            for key, cb in self._keys.iteritems():
                if event.keyval == key:
                    if isinstance(cb, (list, tuple)):
                        cb[0](*cb[1:])
                    else:
                        cb()
                    return True
        return False

    @staticmethod
    def scale_pixbuf_to_scene(pixbuf, scale_4_3, scale_16_9):
        screen_ratio = Scene._get_screen_ratio()
        if screen_ratio == Scene.RATIO_4_3:
            base_scale = scale_4_3
        elif screen_ratio == Scene.RATIO_16_9:
            base_scale = scale_16_9
        return scale_pixbuf(pixbuf, base_scale)[0]

    @staticmethod
    def scale_image_to_scene(img_widget, scale_4_3, scale_16_9):
        pixbuf = img_widget.get_pixbuf()
        pixbuf = Scene.scale_pixbuf_to_scene(pixbuf, scale_4_3, scale_16_9)
        return Gtk.Image.new_from_pixbuf(pixbuf)

    @property
    def ratio(self):
        return self._screen_ratio

    @property
    def scale_factor(self):
        return self._scale_factor

    @property
    def widget(self):
        return self._overlay

    @staticmethod
    def _get_screen_ratio():
        w = SCREEN_WIDTH
        h = SCREEN_HEIGHT

        ratio = (w * 1.0) / h
        dist_43 = abs(Scene.RATIO_4_3 - ratio)
        dist_169 = abs(Scene.RATIO_16_9 - ratio)

        if dist_43 < dist_169:
            return Scene.RATIO_4_3

        return Scene.RATIO_16_9

    @staticmethod
    def _scale_gif(widget, scale):

        anim = widget.get_animation()
        timestamp = GLib.TimeVal()
        pixbuf_iter = anim.get_iter(timestamp)

        max_height = 0
        max_width = 0

        pixbufs = []

        for i in range(4):
            pixbuf = pixbuf_iter.get_pixbuf()
            pixbuf, width, height = scale_pixbuf(pixbuf, scale)
            pixbufs.append(pixbuf)

            if width > max_width:
                max_width = width

            if height > max_height:
                max_height = height

            # the factor of 1000 is due to conveting from milliseconds to
            # microseconds
            time_to_next_frame = pixbuf_iter.get_delay_time() * 1000
            timestamp.add(time_to_next_frame)
            pixbuf_iter.advance(timestamp)

        # This is the animation we want to fill up
        simpleanim = GdkPixbuf.PixbufSimpleAnim.new(max_width, max_height, 10)
        # Set it so it runs in a loop forever
        simpleanim.set_loop(True)

        for pixbuf in pixbufs:
            simpleanim.add_frame(pixbuf)

        image = Gtk.Image()
        image.set_from_animation(simpleanim)
        return image

    def show_all(self):
        self._overlay.show_all()

    @staticmethod
    def get_user_character_path():
        return os.path.join(AVATAR_DEFAULT_LOC, AVATAR_DEFAULT_NAME)

    @staticmethod
    def get_user_character_image():
        return Gtk.Image.new_from_file(Scene.get_user_character_path())
