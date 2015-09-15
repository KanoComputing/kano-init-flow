# The profile desktop icon
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
from gi.repository import Gtk
from kano_profile.profile import get_avatar_circ_image_path, recreate_char
from kano_profile.badges import calculate_kano_level
from kano_world.functions import get_mixed_username
from kano.gtk3.apply_styles import apply_styling_to_screen
from kano_init_flow.paths import common_css_path


class ProfileIcon(Gtk.Fixed):
    def __init__(self):
        super(ProfileIcon, self).__init__()
        apply_styling_to_screen(common_css_path("profile_icon.css"))

        username = get_mixed_username()
        username_label = Gtk.Label(username)
        username_label.get_style_context().add_class("username_desktop_label")

        level, progress, _ = calculate_kano_level()
        level_label = Gtk.Label("Level {}".format(level))
        level_label.get_style_context().add_class("level_desktop_label")

        progress_img = Gtk.Image.new_from_file(self._get_progress_path(progress))
        avatar_img = Gtk.Image.new_from_file(self._get_avatar_path())
        self.put(progress_img, 0, 0)
        self.put(avatar_img, 12, 12)
        self.put(username_label, 90, 20)
        self.put(level_label, 90, 38)

    def _get_avatar_path(self):
        avatar_image_path = get_avatar_circ_image_path()
        if not os.path.exists(avatar_image_path):
            recreate_char(block=True)
            avatar_image_path = get_avatar_circ_image_path()

        # If it still doesn't exist leave it empty
        if not os.path.exists(avatar_image_path):
            return 'image_missing'

        return avatar_image_path

    def _get_progress_path(self, progress):

        progress = int(progress * 100)
        progress_value = progress / 5
        progress_image_path = os.path.join('/usr/share/kano-profile/media/images/progress_icons/209x80/',
                                           '{}.png'.format(progress_value))
        if not os.path.exists(progress_image_path):
            return 'image_missing'

        return progress_image_path
