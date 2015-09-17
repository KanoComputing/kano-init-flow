# The profile desktop icon
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk
from kano.gtk3.apply_styles import apply_styling_to_screen
from kano_init_flow.paths import common_css_path


class WorldIcon(Gtk.Fixed):
    def __init__(self):
        super(WorldIcon, self).__init__()
        apply_styling_to_screen(common_css_path("profile_icon.css"))

        kano_world_label = Gtk.Label("Kano World")
        kano_world_label.get_style_context().add_class("username_desktop_label")

        # Check here if there is a token (which there shouldn't be)
        status_label = Gtk.Label("OFFLINE")
        status_label.get_style_context().add_class("level_desktop_label")

        # world icon path
        img_path = "/usr/share/kano-desktop/icons/kano-world-launcher.png"
        icon_img = Gtk.Image.new_from_file(img_path)

        self.put(icon_img, 0, 0)
        self.put(kano_world_label, 10, 20)
        self.put(status_label, 10, 38)
