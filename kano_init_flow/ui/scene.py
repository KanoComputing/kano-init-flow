# The base class for implementing scenes
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import time

from gi.repository import Gtk, GdkPixbuf, Gdk, GLib

from kano.gtk3.cursor import attach_cursor_events

# TODO: for debuging of different screen ratios
SCREEN_WIDTH = Gdk.Screen.width()
SCREEN_HEIGHT = Gdk.Screen.height()

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

    def __init__(self):
        self._screen_ratio = self._get_screen_ratio()
        self._scale_factor = self._get_screen_scale()

        self._children = []
        self._hand_cursor = []
        self._hand_set_flag = False
        self._hand_cursor_blocked = False

        self._overlay = Gtk.Overlay()

        self._background = Gtk.Image()
        self._background.set_halign(Gtk.Align.START)
        self._background.set_valign(Gtk.Align.START)
        self._overlay.add(self._background)

        self._last_motion = time.time()

        self._fixed = Gtk.Fixed()
        self._overlay.add_overlay(self._fixed)

        self._eb = Gtk.EventBox()
        self._eb.add(self._overlay)
        self._eb.connect('button-release-event', self._propagate_signal)
        self._eb.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self._eb.connect('motion-notify-event', self._motion_cb)

    def _get_screen_ratio(self):
        w = SCREEN_WIDTH
        h = SCREEN_HEIGHT

        ratio = (w * 1.0) / h
        dist_43 = abs(self.RATIO_4_3 - ratio)
        dist_169 = abs(self.RATIO_16_9 - ratio)

        if dist_43 < dist_169:
            return self.RATIO_4_3

        return self.RATIO_16_9

    def _get_screen_scale(self):
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

    def add_widget(self, widget, pos_43, pos_169, clicked_cb=None):
        pos = pos_43 if self._screen_ratio == self.RATIO_4_3 else pos_169

        if pos.scale * self._scale_factor != 1 and pos.scale != 0:
            if widget.__class__.__name__ == "Image":
                if widget.get_animation():
                    widget = self._scale_gif(widget, pos.scale * self._scale_factor)
                else:
                    widget = self._scale_image(widget, pos.scale * self._scale_factor)

            else:
                if pos.scale != 1.0:
                    raise RuntimeError('Can\'t scale regular widgets!')

        root_widget = widget
        if clicked_cb:
            # TODO: Add custom styling to this.
            button_wrapper = Gtk.Button()
            button_wrapper.add(root_widget)
            button_wrapper.connect('button-release-event', self._clicked_cb_wrapper, clicked_cb)
            #attach_cursor_events(button_wrapper)
            root_widget = button_wrapper

            # TODO: This is extremely hacky
            self._hand_cursor.append(root_widget)

        #root_widget.connect('size-allocate', self._sprite_allocated)
        align = Gtk.Alignment.new(pos.x, pos.y, 0, 0)
        align.add(root_widget)
        self._children.append(root_widget)
        self._overlay.add_overlay(align)

    def _propagate_signal(self, widget=None, event=None, data=None):
        for child in self._children:
            alloc = child.get_allocation()
            if event.x >= alloc.x and event.x <= (alloc.x + alloc.width) and \
               event.y >= alloc.y and event.y <= (alloc.y + alloc.height):
                ev = Gdk.Event.new(Gdk.EventType.BUTTON_RELEASE)
                ev.send_event = True
                ev.window = widget.get_window()
                child.emit('button-release-event', ev)
                #break
        return True

    def _motion_cb(self, widget, event):
        dt = time.time() - self._last_motion
        if not self._hand_cursor_blocked and dt > 0.2:
            root_win = widget.get_root_window()
            cursor = root_win.get_cursor()

            new_cursor = Gdk.CursorType.ARROW
            for child in self._children:
                alloc = child.get_allocation()
                if event.x >= alloc.x and event.x <= (alloc.x + alloc.width) and \
                   event.y >= alloc.y and event.y <= (alloc.y + alloc.height) and \
                   child in self._hand_cursor: # FIXME
                    new_cursor = Gdk.CursorType.HAND1
                    break

            if cursor != new_cursor:
                if new_cursor == Gdk.CursorType.HAND1:
                    self._hand_set_flag = True
                else:
                    # The hand wasn't set by the event box, don't remove it
                    if not self._hand_set_flag:
                        return True
                    self._hand_set_flag = False


                root_win.set_cursor(Gdk.Cursor.new(new_cursor))

        return True

    def _clicked_cb_wrapper(self, widget, event, clicked_cb):
        self._hand_cursor_blocked = True
        root_win = widget.get_root_window()
        root_win.set_cursor(Gdk.Cursor.new(Gdk.CursorType.ARROW))

        clicked_cb()
        return True

    @property
    def ratio(self):
        return self._screen_ratio

    @property
    def widget(self):
        return self._eb #self._overlay

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
    def _scale_gif(widget, scale):

        anim = widget.get_animation()
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
