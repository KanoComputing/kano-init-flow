# The Status class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Keeps user's progression through the init flow
#

from gi.repository import Gtk

from .controller import Controller


class MainWindow(Gtk.Window):
    """
        Manages the full-screen top level window of the application.
    """

    def __init__(self, start_from=None):
        """
            :param start_from: Overrides the status and makes the init flow
                               start from this stage.
            :type start_from: str
        """

        Gtk.Window.__init__(self)
        self._ctl = Controller(self, start_from)
        self.connect("delete-event", Gtk.main_quit)

    def show(self):
        self._ctl.first_stage()
        super(MainWindow, self).show()

    def push(self, child):
        # TODO: This should be wrapped in add_idle
        # destroy current child
        # put a new one in
        pass
