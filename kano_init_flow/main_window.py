# The Status class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Keeps user's progression through the init flow
#

from gi.repository import Gtk, GLib, GObject

from kano.gtk3.apply_styles import apply_common_to_screen
from .controller import Controller
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.paths import common_css_path


class MainWindow(Gtk.Window):
    """
        Manages the full-screen top level window of the application.
    """

    EMERGENCY_EXIT_CLICKS = 5

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

        self._keypress_signal_id = None
        self._emergency_counter = 0

        apply_common_to_screen()
        apply_styling_to_screen(common_css_path('scene.css'))
        apply_styling_to_screen(common_css_path('speech_bubble.css'))

        self.set_decorated(False)
        self.fullscreen()

        overlay = Gtk.Overlay()
        self._child = Gtk.EventBox()
        overlay.add(self._child)
        self.add(overlay)
        self._container = overlay

        emergency_exit = Gtk.Button()
        emergency_exit.set_halign(Gtk.Align.START)
        emergency_exit.set_valign(Gtk.Align.START)
        emergency_exit.set_size_request(20, 20)
        emergency_exit.connect('clicked', self._emergency_exit_cb)
        overlay.add_overlay(emergency_exit)

        if start_from:
            debug_button = Gtk.Button('Close')
            debug_button.set_halign(Gtk.Align.END)
            debug_button.set_valign(Gtk.Align.START)
            debug_button.connect('clicked', Gtk.main_quit)
            overlay.add_overlay(debug_button)

    def _emergency_exit_cb(self, widget, data=None):
        print 'emergency'
        self._emergency_counter += 1
        if self._emergency_counter >= self.EMERGENCY_EXIT_CLICKS:
            self._ctl.complete()
            Gtk.main_quit()

    @property
    def return_value(self):
        return self._ctl.return_value

    def prepare_first_stage(self):
        return self._ctl.first_stage()

    def push(self, child):
        GLib.idle_add(self._do_push, child)

    def set_key_events_handler(self, handler=None):
        if self._keypress_signal_id:
            GObject.signal_handler_disconnect(self, self._keypress_signal_id)

        if handler:
            self._keypress_signal_id = self.connect('key-release-event', handler)

    def _do_push(self, child):
        if self._child:
            self._container.remove(self._child)
            self._child.destroy()

        self._child = child
        self._container.add(child)
        child.show_all()
        return False
