# The Status class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Keeps user's progression through the init flow
#

from gi.repository import Gtk, GLib

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

        super(MainWindow, self).__init__()
        self._ctl = Controller(self, start_from)
        self.connect("delete-event", Gtk.main_quit)
        self._child = None

        self.set_decorated(False)
        self.fullscreen()

        if start_from:
            debug_overlay = Gtk.Overlay()
            debug_button = Gtk.Button('Close')
            debug_button.set_halign(Gtk.Align.END)
            debug_button.set_valign(Gtk.Align.START)
            debug_button.connect('clicked', Gtk.main_quit)

            self._child = Gtk.EventBox()
            debug_overlay.add(self._child)
            debug_overlay.add_overlay(debug_button)
            self.add(debug_overlay)
            self._container = debug_overlay
        else:
            self._container = self

    def show_all(self):
        self._ctl.first_stage()
        super(MainWindow, self).show_all()

    def push(self, child):
        GLib.idle_add(self._do_push, child)

    def _do_push(self, child):
        if self._child:
            self._container.remove(self._child)
            self._child.destroy()

        self._child = child
        self._container.add(child)
        child.show_all()
        return False
