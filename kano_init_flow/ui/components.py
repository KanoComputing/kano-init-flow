# components.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A collection of useful components used throughout the UI.
#

from kano_init_flow.ui.scene import ActiveImage
from kano_init_flow.paths import common_media_path


class NextButton(ActiveImage):
    def __init__(self):
        super(NextButton, self).__init__(
            common_media_path('next-button.gif'),
            common_media_path('next-button-hover.png'),
            common_media_path('next-button-down.png')
        )
