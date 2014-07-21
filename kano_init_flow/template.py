
#!/usr/bin/env python

# template.py
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


class KanoButtonBox(Gtk.ButtonBox):

    def __init__(self, kano_button_text, orange_button_text):

        Gtk.ButtonBox.__init__(self, spacing=10)
        self.set_layout(Gtk.ButtonBoxStyle.SPREAD)

        self.kano_button = KanoButton(kano_button_text)

        if orange_button_text:
            self.orange_button = OrangeButton(orange_button_text)
            self.pack_start(self.orange_button, False, False, 0)
            self.pack_start(self.kano_button, False, False, 0)
            # The empty label is to centre the kano_button
            label = Gtk.Label("    ")
            self.pack_start(label, False, False, 0)
        else:
            self.pack_start(self.kano_button, False, False, 0)


# Window class
class Template(Gtk.Box):

    exit_codes = {"launch_wifi": 1, "launch_updater": 2, "launch_profile": 5}

    def __init__(self, img_filename, title, description, kano_button_text, orange_button_text):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        if img_filename is not None:
            self.image = Gtk.Image.new_from_file(img_filename)
            self.pack_start(self.image, False, False, 0)
        self.heading = Heading(title, description)
        self.button_box = KanoButtonBox(kano_button_text, orange_button_text)
        self.kano_button = self.button_box.kano_button
        self.orange_button = self.get_orange_button()

        self.pack_start(self.heading.container, False, False, 0)
        self.pack_start(self.button_box, False, False, 0)

    def get_orange_button(self):
        return getattr(self.button_box, "orange_button", None)
