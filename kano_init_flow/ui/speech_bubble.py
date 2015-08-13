# speech_bubble.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A widget that resembles a speech bubble
#


from gi.repository import Gtk, Gdk

from kano_init_flow.paths import common_media_path
from kano.gtk3.buttons import OrangeButton


class SpeechBubble(Gtk.Grid):
    # Where's the source of the speech bubble
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, text=None, buttons=None, source=BOTTOM, source_align=0.5):
        self._source = source
        self._source_align = source_align
        self._button_box = None
        if buttons:
            for button in buttons:
                self.add_button(button[0], button[1])

        super(SpeechBubble, self).__init__()
        self.set_row_spacing(0)
        self.set_column_spacing(0)

        # The speech bubble triangle
        img_path = common_media_path("sb-{}.png".format(self._source))
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

        self.attach(self._bubble, 0, 0, 1, 1)

        if self._source == self.TOP:
            self.attach_next_to(img_align, self._bubble,
                                Gtk.PositionType.TOP, 1, 1)
        elif self._source == self.BOTTOM:
            self.attach_next_to(img_align, self._bubble,
                                Gtk.PositionType.BOTTOM, 1, 1)
        elif self._source == self.LEFT:
            self.attach_next_to(img_align, self._bubble,
                                Gtk.PositionType.LEFT, 1, 1)
        elif self._source == self.RIGHT:
            self.attach_next_to(img_align, self._bubble,
                                Gtk.PositionType.RIGHT, 1, 1)

        # Padding in of the bubble
        self._padded_bubble = Gtk.Alignment()
        self._padded_bubble.set_padding(40, 20, 40, 40)
        self._bubble.add(self._padded_bubble)

        self._init_content(text)

        self.show_all()

    def _init_content(self, text_copy):
        self._content = box = Gtk.VBox(hexpand=True, vexpand=True)

        self._text = text = Gtk.Label(text_copy)
        text.set_justify(Gtk.Justification.CENTER)
        box.pack_start(text, False, False, 0)

        self._padded_bubble.add(box)

    def add_button(self, label, callback=None):
        if not self._button_box:
            self._button_box = Gtk.Box()
            self._content.pack_start(self._button_box, False, False, 15)

        button = OrangeButton(label)
        if callback:
            button.connect('button_release_event', callback)
            button.connect('key_release_event', callback)
        self._button_box.pack_start(button, False, False, 10)
        self._button_box.set_halign(Gtk.Align.CENTER)
        self._button_box.set_valign(Gtk.Align.CENTER)

        return button
