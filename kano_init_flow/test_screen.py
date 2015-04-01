# test_screen.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# test screen and fake lxpanel

from template import Template
import kano_init_flow.constants as constants
from faux_panel import FauxPanel


class TestScreen():

    def __init__(self, win):

        self.win = win
        self.template = Template(constants.media + "made_it.png", "foo", "bar", "TEST")
        self.win.set_main_widget(self.template)

        # Make one of the kano button grab the focus
        self.template.kano_button.grab_focus()

        self.win.show_all()
