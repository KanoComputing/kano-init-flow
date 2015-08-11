# The bugs world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk


from kano_init_flow.stage import Stage


class BugsWorld(Stage):
    """
        The keyboard tutorial stage
    """

    def __init__(self):
        super(BugsWorld, self).__init__()

        self._id = 'bugs-world'

    def get_widget(self):
        return BugsWorldMainWidget()


class BugsWorldMainWidget(Gtk.EventBox):
    def __init__(self):
        pass
