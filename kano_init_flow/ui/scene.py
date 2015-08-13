# The base class for implementing scenes
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, GdkPixbuf, Gdk, GLib

from kano.gtk3.cursor import attach_cursor_events


class Position(object):
    def __init__(self, x=0, y=0, scale=1.0):
        if x <= 1:
            self._x = int(x * Gdk.Screen.width())
        else:
            self._x = x

        if y <= 1:
            self._y = int(y * Gdk.Screen.height())
        else:
            self._y = y

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

    def __init__(self):
        self._screen_ratio = self._get_screen_ratio()

        self._overlay = Gtk.Overlay()

        self._background = Gtk.Image()
        self._overlay.add(self._background)

        self._fixed = Gtk.Fixed()
        self._overlay.add_overlay(self._fixed)

    def _get_screen_ratio(self):
        w = Gdk.Screen.width()
        h = Gdk.Screen.height()

        ratio = (w * 1.0) / h
        dist_43 = abs(self.RATIO_4_3 - ratio)
        dist_169 = abs(self.RATIO_16_9 - ratio)

        if dist_43 < dist_169:
            return self.RATIO_4_3

        return self.RATIO_16_9

    def set_background(self, ver_43, ver_169):
        """
            Set the background of the scene.

            :param ver_43: Path to the 4:3 version of the background.
            :type ver_43: str

            :param ver_169: Path to the 16:9 version of the background.
            :type ver_169: str
        """

        w = Gdk.Screen.width()
        h = Gdk.Screen.height()

        bg_path = ver_43 if self._screen_ratio == self.RATIO_4_3 else ver_169
        bg_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(bg_path, w, h)
        self._background.set_from_pixbuf(bg_pixbuf)

    def add_widget(self, widget, pos_43, pos_169, clicked_cb=None):
        pos = pos_43 if self._screen_ratio == self.RATIO_4_3 else pos_169

        # If the widget is an image, scale it using GdkPixbuf
        if pos.scale != 1:
            if widget.__class__.__name__ == "Image":
                widget = self._scale_image(widget, pos.scale)
            elif widget.__class__.__name__ == "gtk.gdk.PixbufGifAnim":
                widget = self._scale_gif(widget, pos.scale, 100000)
            else:
                raise RuntimeError('Can\'t scale regular widgets!')

        root_widget = widget
        if clicked_cb:
            # TODO: Add custom styling to this.
            button_wrapper = Gtk.Button()
            button_wrapper.add(root_widget)
            button_wrapper.connect('clicked', self._clicked_cb_wrapper, clicked_cb)
            attach_cursor_events(button_wrapper)
            root_widget = button_wrapper

        self._fixed.put(root_widget, pos.x, pos.y)

    def _clicked_cb_wrapper(self, button, clicked_cb):
        clicked_cb()
        return True

    @property
    def widget(self):
        return self._overlay

    @staticmethod
    def _scale_pixbuf(pixbuf, scale):
        w = pixbuf.get_width()
        h = pixbuf.get_height()

        w_scaled = int(w * scale)
        h_scaled = int(h * scale)
        new_pixbuf = pixbuf.scale_simple(w_scaled, h_scaled,
                                         GdkPixbuf.InterpType.BILINEAR)
        return new_pixbuf, w_scaled, h_scaled

    @staticmethod
    def _scale_image(widget, scale):
        pixbuf = widget.get_pixbuf()
        pixbuf, _, _ = Scene._scale_pixbuf(pixbuf, scale)
        widget.set_from_pixbuf(pixbuf)
        return widget

    @staticmethod
    def _scale_gif(anim, scale, time_between_frames):

        timestamp = GLib.TimeVal()
        pixbuf_iter = anim.get_iter(timestamp)

        max_height = 0
        max_width = 0

        pixbufs = []

        for i in range(4):
            pixbuf = pixbuf_iter.get_pixbuf()
            pixbuf, width, height = Scene._scale_pixbuf(pixbuf, scale)
            pixbufs.append(pixbuf)

            if width > max_width:
                max_width = width

            if height > max_height:
                max_height = height

            timestamp.add(time_between_frames)
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
