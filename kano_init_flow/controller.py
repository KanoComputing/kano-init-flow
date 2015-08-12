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

    def __init__(self, main_window, start_from=None):
        """
            :param start_from: Overrides the status and makes the init flow
                               start from this stage.
            :type start_from: str
        """

        self._main_window = main_window

        self._status = Status.get_instance()
        if start_from:
            self._status.debug_mode(start_from)

        self._stages = [
            BugsWorld
        ]

    @property
    def main_window(self):
        return self._main_window

    def first_stage(self):
        """
            Runs the first stage.

            Note: The first stage is determined by the location variable from
            the status file, not necessarily the very first stage.
        """

        if len(self._stages):
            index = self._get_stage_index(self._status.location)
            stage_ctl = self._stages[index](self)
            stage_ctl.first_step()
        else:
            raise RuntimeError('No flow stages available')

    def next_stage(self):
        """
            This callback is passed over to each stage to be called once
            it's over and the control should be handed to the subsequent one.
        """

        index = self._get_stage_index(self._status.location)
        if index is not None and index < len(self._stages) - 1:
            stage_ctl = self._stages[index + 1](self)
            stage_ctl.first_step()
        else:
            # TODO: Exit the application, there are no more stages to do.
            pass

    def _get_stage_index(self):
        index = None
        for i, s in enumerate(self._stages):
            if s.id == loc:
                index = i
                break

        return index

    def _get_stage_class_by_id(self, stage_id):
        index = self._get_stage_index(stage_id)
        return self._stages[index] if index else None
