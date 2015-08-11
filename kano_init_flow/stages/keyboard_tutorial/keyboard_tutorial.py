# The main class of the keyboard tutorial stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Controls the progression through the flow
#

import Gtk


from kano_init_flow.stage import Stage


class KeyboardTutorial(Stage):
    """
        The keyboard tutorial stage
    """

    def __init__(self):
        super(KeyboardTutorial, self).__init__()

        self._id = '5'

    def get_widget(self):
        return KeyboardTutorialScreen1()

    def _


class KeyboardTutorialScreen1(Gtk.EventBox):
    def __init__(self):
        pass
