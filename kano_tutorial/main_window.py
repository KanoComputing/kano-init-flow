# main_window.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The main window
#

import os
from gi.repository import Gtk

from kano.gtk3.apply_styles import apply_common_to_screen, \
    apply_styling_to_screen

from kano_tutorial.screens import Screen1, Screen2, Screen3, Screen4
from kano_tutorial.drag_and_drop import DragAndDrop
from kano_tutorial.paths import CSS_DIR

REFS = {
    0: Screen1,
    1: Screen2,
    2: Screen3,
    3: Screen4,
    4: DragAndDrop,
}


class MainWindow(Gtk.Window):
    CSS_PATH = os.path.join(CSS_DIR, "kano-tutorial.css")

    def __init__(self, stage=0):

        apply_common_to_screen()
        apply_styling_to_screen(self.CSS_PATH)

        # Create main window
        Gtk.Window.__init__(self, title="Kano")
        self.fullscreen()
        self.connect("delete-event", Gtk.main_quit)
        self.goto(stage)

    def goto(self, stage):
        self.clear_win()
        REFS[stage](self)

    def clear_win(self):
        for i in self.get_children():
            self.remove(i)
