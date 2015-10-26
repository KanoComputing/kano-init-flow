# utils.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
#

import time
from gi.repository import GdkPixbuf, Gtk, GLib

from kano.utils import run_bg


def add_class(widget, class_name):
    widget.get_style_context().add_class(class_name)


def cb_wrapper(widget, cb1=None, cb2=None):
    if cb2 is not None:
        cb2()
    else:
        cb1()

    return True


def scale_pixbuf(pixbuf, scale):
    w = pixbuf.get_width()
    h = pixbuf.get_height()

    w_scaled = int(w * scale)
    h_scaled = int(h * scale)
    new_pixbuf = pixbuf.scale_simple(w_scaled, h_scaled,
                                     GdkPixbuf.InterpType.BILINEAR)
    return new_pixbuf, w_scaled, h_scaled


def scale_image(widget, scale):
    pixbuf = widget.get_pixbuf()
    pixbuf, _, _ = scale_pixbuf(pixbuf, scale)
    widget.set_from_pixbuf(pixbuf)
    return widget


def scale_gif(widget, scale):
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


LEDS_LAST_TRIGGER=0
def trigger_led_speaker():
    global LEDS_LAST_TRIGGER

    now = time.time()
    if now - LEDS_LAST_TRIGGER > 3:
        run_bg('sudo kano-speakerleds initflow 2 4')
        LEDS_LAST_TRIGGER = now


def desaturate_image(image):
    result = image.get_pixbuf().copy()
    image.get_pixbuf().saturate_and_pixelate(result, 0.0, False)
    return Gtk.Image.new_from_pixbuf(result)
