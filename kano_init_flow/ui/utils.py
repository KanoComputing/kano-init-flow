# utils.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
#

def add_class(widget, class_name):
    widget.get_style_context().add_class(class_name)


def cb_wrapper(widget, cb1=None, cb2=None):
    if cb2 is not None:
        cb2()
    else:
        cb1()

    return True
