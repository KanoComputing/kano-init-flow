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

    self._id = 'bugs-world'

    def __init__(self, ctl):
        super(BugsWorld, self).__init__(ctl)

    def first_step(self):
        main = BugsWorldMainWidget()
        self._ctl.main_window.push(main)

    def next_step(self):
        pass


class BugsWorldMainWidget(Gtk.EventBox):
    def __init__(self):
        pass
