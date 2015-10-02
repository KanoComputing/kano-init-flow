# The profile desktop icon
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk
from kano.gtk3.apply_styles import apply_styling_to_screen
from kano_init_flow.paths import common_css_path


class WorldIcon(Gtk.Fixed):
    def __init__(self, offline=True):
        super(WorldIcon, self).__init__()
        apply_styling_to_screen(common_css_path("profile_world_icon.css"))

        kano_world_label = Gtk.Label("Kano World")
        kano_world_label.get_style_context().add_class("heading_desktop_label")

        # world icon path
        img_path = "/usr/share/kano-desktop/icons/kano-world-launcher.png"
        icon_img = Gtk.Image.new_from_file(img_path)

        self.put(icon_img, 0, 0)

        # Check here if there is a token (which there shouldn't be)
        if offline:
            status_label = Gtk.Label("OFFLINE")
            self.put(status_label, 60, 39)
        else:
            status_label = Gtk.Label("ONLINE")
            self.put(status_label, 68, 39)

        status_label.get_style_context().add_class("subheading_desktop_label")
        self.put(kano_world_label, 30, 21)
