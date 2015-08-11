# Parent for all Stages
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import Gtk


class Stage(object): #(Gtk.EventBox):
    def __init__(self):
        super(Stage, self).__init__()

        self._id = None

    def get_widget(self):
        pass
