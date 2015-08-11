# The Status class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Keeps user's progression through the init flow
#

import Gtk

from .controller import Controller


class MainWindow(Gtk.Window):
    """
        Manages the full-screen top level window of the application.
    """

    def __init__(self):
        self._controller = Controller()
