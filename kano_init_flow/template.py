
#!/usr/bin/env python

# stage.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Main template for the stages of the init flow
#

import os
import sys
from gi.repository import Gtk

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.append(dir_path)

from kano.gtk3.buttons import KanoButton, OrangeButton
from kano.gtk3.heading import Heading


# Window class
class Template(Gtk.Box):

    def __init__(self, img_filename, title, description, kano_button_text, orange_button_text):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.image = Gtk.Image.new_from_file(img_filename)
        self.heading = Heading(title, description)
        self.kano_button = KanoButton(kano_button_text)
        self.kano_button.pack_and_align()

        self.pack_start(self.image, False, False, 0)
        self.pack_start(self.heading.container, False, False, 0)
        self.pack_start(self.kano_button.align, False, False, 0)

        if not orange_button_text == "":
            self.orange_button = OrangeButton(orange_button_text)
            align = Gtk.Alignment()
            align.set_padding(5, 5, 0, 0)
            align.add(self.orange_button)
            self.pack_start(align, False, False, 10)
