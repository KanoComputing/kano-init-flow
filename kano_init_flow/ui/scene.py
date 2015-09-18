# The base class for implementing scenes
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import time

from gi.repository import Gtk, Gdk, GdkPixbuf
from kano.gtk3.cursor import attach_cursor_events

from kano_init_flow.ui.utils import scale_image, scale_pixbuf, add_class, \
                                    scale_gif

from kano_avatar.paths import AVATAR_DEFAULT_LOC, AVATAR_DEFAULT_NAME
from kano_init_flow.ui.profile_icon import ProfileIcon


# TODO: for debuging of different screen ratios
SCREEN_WIDTH = Gdk.Screen.width()
SCREEN_HEIGHT = Gdk.Screen.height()

# SCREEN_WIDTH = 1280
# SCREEN_HEIGHT = 800

# 16 by 9

# SCREEN_WIDTH = 1600
# SCREEN_HEIGHT = 900

# 4 by 3

# SCREEN_WIDTH = 1024
# SCREEN_HEIGHT = 768


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
        self._determine_screen_ratio()
        self._scale_factor = self._get_scale_factor()

        self._widgets = {}

        if main_window:
            self._keys = {}
            main_window.set_key_events_handlers(self._key_press_cb_wrapper,
                                                self._key_release_cb_wrapper)

        self._overlay = Gtk.Overlay()

        self._background = Gtk.Image()
        self._background.set_halign(Gtk.Align.START)
        self._background.set_valign(Gtk.Align.START)
        self._overlay.add(self._background)

        self._last_motion = time.time()

        self._fixed = Gtk.Fixed()
        self._overlay.add_overlay(self._fixed)

        self._eb = Gtk.EventBox()
        self._eb.set_size_request(self._w, self._h)
        self._eb.add(self._overlay)
        add_class(self._eb, 'scene-backdrop')

    def _determine_screen_ratio(self):
        self._w = w = SCREEN_WIDTH
        self._h = h = SCREEN_HEIGHT

        ratio = (w * 1.0) / h
        dist_43 = abs(Scene.RATIO_4_3 - ratio)
        dist_169 = abs(Scene.RATIO_16_9 - ratio)

        if dist_43 < dist_169:
            self._screen_ratio = Scene.RATIO_4_3
        else:
            self._screen_ratio = Scene.RATIO_16_9

        if ratio > 1:
            self._h *= ratio * (1.0 / self._screen_ratio)
        else:
            self._w *= (1.0 / ratio) * self._screen_ratio

    def get_width(self):
        return self._w

    def get_height(self):
        return self._h

    def _get_scale_factor(self):
        if self._screen_ratio == self.RATIO_4_3:
            return self._h / 1200.0
        return self._h / 1080.0

    def set_background(self, ver_43, ver_169):
        """
            Set the background of the scene.

            :param ver_43: Path to the 4:3 version of the background.
            :type ver_43: str

            :param ver_169: Path to the 16:9 version of the background.
            :type ver_169: str
        """

        bg_path = ver_43 if self._screen_ratio == self.RATIO_4_3 else ver_169
        bg_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(bg_path, self._w,
                                                           self._h)
        self._background.set_from_pixbuf(bg_pixbuf)

    def add_profile_icon(self, callback=None, use_default=False):
        # We always want to add the widget to the same position in each screen
        self.add_widget(
            ProfileIcon(use_default),
            Placement(0.03, 0.05, 0),
            Placement(0.03, 0.05, 0),
            callback
        )

    def add_character(self, p43, p169, clicked_cb=None, key=None,
                      name=None, modal=False):
        # Character path in the home directory
        character_path = os.path.join(
            os.path.expanduser("~"),
            ".character-content/character.png"
        )

        self.add_widget(
            Gtk.Image.new_from_file(character_path),
            p43,
            p169,
            clicked_cb,
            key,
            name,
            modal
        )

    def add_widget(self, widget, p43, p169, clicked_cb=None, key=None,
                   name=None, modal=False):
        placement = p43 if self._screen_ratio == self.RATIO_4_3 else p169

        final_scale = placement.scale * self._scale_factor
        if final_scale != 1 and placement.scale != 0:
            if widget.__class__.__name__ == 'Image':
                if widget.get_animation():
                    widget = scale_gif(widget, final_scale)
                else:
                    widget = scale_image(widget, final_scale)
            elif issubclass(widget.__class__, ActiveImage):
                widget.scale(final_scale)
            else:
                if placement.scale != 1.0:
                    raise RuntimeError('Can\'t scale regular widgets!')

        if issubclass(widget.__class__, ActiveImage):
            root_widget = widget.get_widget()
        else:
            root_widget = widget

        if clicked_cb:
            # ActiveImage already comes in a button wrapper
            if not issubclass(widget.__class__, ActiveImage):
                button_wrapper = Gtk.Button()
                button_wrapper.add(root_widget)
                root_widget = button_wrapper

            attach_cursor_events(root_widget)
            if isinstance(clicked_cb, (list, tuple)):
                root_widget.connect('clicked', self._clicked_cb_wrapper,
                                    clicked_cb[0], *clicked_cb[1:])
            else:
                root_widget.connect('clicked', self._clicked_cb_wrapper,
                                    clicked_cb)

            if key is not None:
                if not hasattr(self, '_keys'):
                    msg = 'Scene must be initialised with main_window to ' + \
                          'be able to receive key events.'
                    raise RuntimeError(msg)
                cbs = {'action': clicked_cb}
                if issubclass(widget.__class__, ActiveImage):
                    cbs['down'] = widget.down
                    cbs['up'] = widget.up
                self._keys[key] = cbs

        align = Gtk.Alignment.new(placement.x, placement.y, 0, 0)
        align.add(root_widget)
        align.set_size_request(self._w, self._h)

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

    def _handle_key_event(self, event, cb_seq):
        if hasattr(event, 'keyval'):
            for key, cbs in self._keys.iteritems():
                if event.keyval == key:
                    # call all the callbacks in the sequence
                    for n in cb_seq:
                        if n not in cbs or cbs[n] is None:
                            next
                        cb = cbs[n]
                        if isinstance(cb, (list, tuple)):
                            cb[0](*cb[1:])
                        else:
                            cb()
                    return True
        return False

    def _key_press_cb_wrapper(self, widget, event):
        return self._handle_key_event(event, ['down'])

    def _key_release_cb_wrapper(self, widget, event):
        return self._handle_key_event(event, ['action', 'up'])

    def scale_pixbuf_to_scene(self, pixbuf, scale_4_3, scale_16_9):
        screen_ratio = self._screen_ratio
        if screen_ratio == Scene.RATIO_4_3:
            base_scale = scale_4_3 * self._scale_factor
        elif screen_ratio == Scene.RATIO_16_9:
            base_scale = scale_16_9 * self._scale_factor
        return scale_pixbuf(pixbuf, base_scale)[0]

    def scale_image_to_scene(self, img_widget, scale_4_3, scale_16_9):
        pixbuf = img_widget.get_pixbuf()
        pixbuf = self.scale_pixbuf_to_scene(pixbuf, scale_4_3, scale_16_9)
        return Gtk.Image.new_from_pixbuf(pixbuf)

    @property
    def ratio(self):
        return self._screen_ratio

    @property
    def scale_factor(self):
        return self._scale_factor

    @property
    def widget(self):
        return self._eb

    def show_all(self):
        self._overlay.show_all()

    @staticmethod
    def get_user_character_path():
        return os.path.join(AVATAR_DEFAULT_LOC, AVATAR_DEFAULT_NAME)

    @staticmethod
    def get_user_character_image():
        return Gtk.Image.new_from_file(Scene.get_user_character_path())


class ActiveImage(object):
    def __init__(self, img, hover=None, down=None):
        self._img = Gtk.Image.new_from_file(img)

        if hover:
            self._hover = Gtk.Image.new_from_file(hover)
        else:
            self._hover = self._copy_img()

        if down:
            self._down = Gtk.Image.new_from_file(down)
        else:
            self._down = self._copy_img()

    def _copy_img(self):
        if self._img.get_animation():
            return Gtk.Image.new_from_animation(self._img.get_animation())
        else:
            return Gtk.Image.new_from_pixbuf(self._img.get_pixbuf())

    def scale(self, factor):
        scaled = []
        for w in [self._img, self._hover, self._down]:
            if w.get_animation():
                w = scale_gif(w, factor)
            else:
                w = scale_image(w, factor)
            scaled.append(w)

        self._img, self._hover, self._down = scaled

    def get_widget(self):
        self._w = Gtk.Image()
        self.set(self._img)
        self._button = Gtk.Button()
        self._button.add(self._w)

        if self._hover:
            self._button.connect('enter-notify-event', self._enter_cb)
            self._button.connect('leave-notify-event', self._leave_cb)

        if self._down:
            self._button.connect('button-press-event', self._down_cb)
            self._button.connect('button-release-event', self._up_cb)

        return self._button

    def set(self, img):
        if img.get_animation():
            self._w.set_from_animation(img.get_animation())
        else:
            self._w.set_from_pixbuf(img.get_pixbuf())

    def down(self):
        self.set(self._down)

    def up(self):
        self.set(self._img)

    def _down_cb(self, widget, event, user=None):
        self.down()

    def _up_cb(self, widget, event, user=None):
        self.up()

    def _enter_cb(self, widget, event, user=None):
        self.set(self._hover)

    def _leave_cb(self, widget, event, user=None):
        self.set(self._img)
