# speech_bubble_dialog.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A widget that resembles a speech bubble
#


from gi.repository import Gtk, Gdk

from . import constants


class SpeechBubbleDialog(Gtk.Grid):
    # Where's the source of the speech bubble
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, heading, text, source=BOTTOM, source_align=0.5):
        self._source = source
        self._source_align = source_align

        Gtk.Grid.__init__(self)

        # The speech bubble triangle
        img_path = "{}/sb-{}.png".format(constants.media, self._source)
        img = Gtk.Image.new_from_file(img_path)
        img.set_hexpand(False)
        img.set_vexpand(False)

        img_align = Gtk.Alignment()
        img_align.add(img)

        if self._source in [self.TOP, self.BOTTOM]:
            img_align.set(self._source_align, 0, 0, 0)
        else:
            img_align.set(0, self._source_align, 0, 0)

        # The background of the bubble
        self._bubble = Gtk.EventBox()
        self._bubble.get_style_context().add_class('speech-bubble')

        if self._source == self.TOP:
            self.attach(img_align, 0, 0, 1, 1)
            self.attach(self._bubble, 0, 1, 1, 1)
        elif self._source == self.BOTTOM:
            self.attach(self._bubble, 0, 0, 1, 1)
            self.attach(img_align, 0, 1, 1, 1)
        elif self._source == self.LEFT:
            self.attach(img_align, 0, 0, 1, 1)
            self.attach(self._bubble, 1, 0, 1, 1)
        elif self._source == self.RIGHT:
            self.attach(self._bubble, 0, 0, 1, 1)
            self.attach(img_align, 1, 0, 1, 1)

        # Padding in of the bubble
        self._padded_bubble = Gtk.Alignment()
        self._padded_bubble.set_padding(40, 40, 40, 40)
        self._bubble.add(self._padded_bubble)

        self._init_content(heading, text)

        self.show_all()

    def _init_content(self, heading_copy, text_copy):
        self._content = box = Gtk.VBox(hexpand=True, vexpand=True)

        self._heading = heading = Gtk.Label(heading_copy)
        heading.get_style_context().add_class('heading')
        box.pack_start(heading, False, False, 0)

        self._text = text = Gtk.Label(text_copy)
        box.pack_start(text, False, False, 0)

        self._padded_bubble.add(box)
