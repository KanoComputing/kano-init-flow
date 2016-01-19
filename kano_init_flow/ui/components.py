# components.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A collection of useful components used throughout the UI.
#

from gi.repository import Gtk

from kano_init_flow.ui.scene import ActiveImage
from kano_init_flow.paths import common_media_path


class NextButton(ActiveImage):
    def __init__(self):
        super(NextButton, self).__init__(
            common_media_path('next-button.gif'),
            common_media_path('next-button-hover.png'),
            common_media_path('next-button-down.png')
        )


class ExternalApp(Gtk.Overlay):
    def __init__(self, stage, socket_widget):
        super(ExternalApp, self).__init__()
        self.loading_bar = Gtk.Image.new_from_file(
            stage.media_path("loading_bar.gif")
        )
        self.add(self.loading_bar)

        # Pack the socket in a box so the socket doesn't stretch to
        # fill the overlay
        box = Gtk.Box()
        box.pack_start(socket_widget, False, False, 0)
        self.add_overlay(box)
