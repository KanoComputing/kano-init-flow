# The Controller class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Controls the progression through the flow
#

from .status import Status


class Controller(object):
    """
        Controls the flow through the setup procedure.

        The MainWindow class uses it to determine what comes next.
    """

    def __init__(self):
        pass
