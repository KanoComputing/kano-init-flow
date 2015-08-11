# Parent for all Stages
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

class Stage(object):
    def __init__(self, ctl):
        super(Stage, self).__init__()

        self._ctl = ctl

    def first_step(self):
        pass

    def next_step(self):
        pass
