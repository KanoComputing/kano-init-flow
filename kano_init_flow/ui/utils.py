# utils.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
#

from gi.repository import GdkPixbuf

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
