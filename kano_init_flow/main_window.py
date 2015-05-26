# main_window.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The main window
#

from gi.repository import Gtk, Gdk
import os
import sys

from kano.gtk3.apply_styles import apply_common_to_screen
from kano.gtk3.application_window import ApplicationWindow

from kano_init_flow.reboot_screen import RebootScreen
from kano_init_flow.paths import CSS_DIR

# Window class
class MainWindow(ApplicationWindow):

    def __init__(self, first_screen, reboot=False):
        apply_common_to_screen()
        specific_css = Gtk.CssProvider()
        css_path = os.path.join(CSS_DIR, "kano-init-flow.css")
        specific_css.load_from_path(css_path)
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen,
            specific_css,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        # We need this for backwards compatibility
        self.need_reboot = reboot
        # Create main window
        ApplicationWindow.__init__(self, title=_("Kano"), width=2, height=2)
        # This needs to be here to get the resizing correct for the screens
        self.show_all()
        # This is to get position right when the window resizes
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        # Start on first_screen
        first_screen(self)

    def clear_win(self):
        self.remove_main_widget()

    # hacky fix - reset height allocation for the window
    def reset_allocation(self):

        allocation = self.get_allocation()
        allocation.width = 1
        allocation.height = 1
        self.size_allocate(allocation)

    # hacky fix - shrink height of window
    def shrink(self):
        self.resize(590, 100)

    def exit_flow(self):
        if self.need_reboot:
            self.clear_win()
            RebootScreen(self)
        else:
            # Init flow completed
            sys.exit(0)
