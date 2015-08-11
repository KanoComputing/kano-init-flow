# The Controller class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Controls the progression through the flow
#

from .status import Status

from .stages.bugs_world import BugsWorld

class Controller(object):
    """
        Controls the flow through the setup procedure.

        The MainWindow class uses it to determine what comes next.
    """

    def __init__(self, start_from=None):
        """
            :param start_from: Overrides the status and makes the init flow
                               start from this stage.
            :type start_from: str
        """

        self._status = Status.get_instsance()
        self._status.debug_mode(start_from)
