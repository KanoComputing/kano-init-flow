# The Status class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Keeps user's progression through the init flow
#

from gi.repository import Gtk, GLib, GObject, Gdk

from kano.gtk3.apply_styles import apply_common_to_screen
from kano.logging import logger

from kano_init_flow.controller import Controller
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

        screen = Gdk.Screen.get_default()
        width = screen.get_width()
        height = screen.get_height()
        self.set_size_request(width, height + 1)
        self.set_position(Gtk.WindowPosition.CENTER)

        overlay = Gtk.Overlay()
        self._child = Gtk.EventBox()
        overlay.add(self._child)
        self.add(overlay)
        self._container = overlay
        self._container.set_halign(Gtk.Align.CENTER)
        self._container.set_valign(Gtk.Align.CENTER)

        emergency_exit = Gtk.EventBox()
        emergency_exit.set_halign(Gtk.Align.START)
        emergency_exit.set_valign(Gtk.Align.START)
        emergency_exit.set_size_request(20, 20)
        emergency_exit.connect('button-release-event', self._emergency_exit_cb)
        overlay.add_overlay(emergency_exit)

        if start_from:
            debug_button = Gtk.EventBox()
            debug_button.add(Gtk.Label('Close'))
            debug_button.set_halign(Gtk.Align.END)
            debug_button.set_valign(Gtk.Align.START)
            debug_button.connect('button-release-event', Gtk.main_quit)
            overlay.add_overlay(debug_button)

    def _emergency_exit_cb(self, widget, data=None):
        self._emergency_counter += 1
        msg = "Emergency button pressed {}x".format(self._emergency_counter)
        logger.warn(msg)
        if self._emergency_counter >= self.EMERGENCY_EXIT_CLICKS:
            logger.warn("Emergency exiting the init flow")
            self._ctl.complete()
            Gtk.main_quit()

    @property
    def return_value(self):
        return self._ctl.return_value

    def prepare_first_stage(self):
        return self._ctl.first_stage()

    def push(self, child):
        GLib.idle_add(self._do_push, child)

    def set_key_events_handlers(self, press=None, release=None):
        if self._keypress_signal_id:
            GObject.signal_handler_disconnect(self, self._press_signal_id)
            GObject.signal_handler_disconnect(self, self._release_signal_id)

        if press:
            self._press_signal_id = self.connect('key-press-event', press)

        if release:
            self._release_signal_id = self.connect('key-release-event',
                                                   release)

    def _do_push(self, child):
        if self._child:
            self._container.remove(self._child)
            self._child.destroy()

        self._child = child
        self._container.add(child)
        child.show_all()
        return False
