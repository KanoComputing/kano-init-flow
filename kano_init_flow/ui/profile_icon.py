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
from kano_init_flow.paths import common_css_path, common_media_path


class ProfileIcon(Gtk.Fixed):
    def __init__(self, use_default=False):
        super(ProfileIcon, self).__init__()
        apply_styling_to_screen(common_css_path("profile_world_icon.css"))

        username = get_mixed_username()
        username_label = Gtk.Label(username)
        username_label.get_style_context().add_class("heading_desktop_label")

        # this is faster
        if use_default:
            level_label = Gtk.Label("Level 1")
            level_label.get_style_context().add_class("subheading_desktop_label")

            progress_img = Gtk.Image.new_from_file(self._get_progress_path(0))
            avatar_img = Gtk.Image.new_from_file(self._get_local_avatar_path())
        else:
            level, progress, _ = calculate_kano_level()
            level_label = Gtk.Label("Level {}".format(level))

            progress_img = Gtk.Image.new_from_file(self._get_progress_path(progress))
            avatar_img = Gtk.Image.new_from_file(self._get_avatar_path())

        level_label.get_style_context().add_class("subheading_desktop_label")
        self.put(progress_img, 0, 0)
        self.put(avatar_img, 13, 13)
        self.put(username_label, 90, 20)
        self.put(level_label, 90, 38)

    def _get_local_avatar_path(self):
        return common_media_path("character_circ_ring.png")

    def _get_avatar_path(self):
        avatar_image_path = get_avatar_circ_image_path()
        if not os.path.exists(avatar_image_path):
            recreate_char(block=True)
            avatar_image_path = get_avatar_circ_image_path()

        # If it still doesn't exist leave it empty
        if not os.path.exists(avatar_image_path):
            # use default
            avatar_image_path = self._get_local_avatar_path()

        return avatar_image_path

    def _get_progress_path(self, progress):

        progress = int(progress * 100)
        progress_value = progress / 5
        progress_image_path = os.path.join('/usr/share/kano-profile/media/images/progress_icons/209x80/',
                                           '{}.png'.format(progress_value))
        if not os.path.exists(progress_image_path):
            return 'image_missing'

        return progress_image_path
