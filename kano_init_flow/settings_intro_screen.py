# settings_intro_screen
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Tells user they will configure display and audio
#

import os

from kano_init_flow.template import Template
from kano_init_flow.audio_screen import AudioScreen
from kano_init_flow.paths import MEDIA_DIR


class SettingsIntroScreen(object):
    """
    Screen to begin the setup of the system. Introduces the settings
    which will be adjusted
    """

    def __init__(self, win):
        self.win = win
        self.win.set_resizable(True)

        self.template = Template(
            img_path=os.path.join(MEDIA_DIR, "update_successful.png"),
            title="You have the power!",
            description="Now let's test your computer's sound and screen.",
            button1_text="TEST SOUND"
        )
        self.template.kano_button.connect("button_release_event", self.activate)
        self.template.kano_button.connect("key_release_event", self.activate)
        self.win.set_main_widget(self.template)
        self.win.shrink()

        # Make the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()

    def activate(self, _, event):
        """ Go to the audio screen """

         # If enter key is pressed or mouse button is clicked
        if not hasattr(event, 'keyval') or event.keyval == 65293:

            self.win.clear_win()
            AudioScreen(self.win)
