# The MainWindow class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Show the MainWindow
#

import os
import json

from kano.utils import ensure_dir
from kano.logging import logger

from .paths import STATUS_FILE_PATH


class StatusError(Exception):
    pass


class Status(object):
    _status_file = STATUS_FILE_PATH

    _singleton_instance = None

    @staticmethod
    def get_instance():
        if not Status._singleton_instance:
            Status()

        return Status._singleton_instance

    def __init__(self):
        if Status._singleton_instance:
            raise Exception('This class is a singleton!')
        else:
            Status._singleton_instance = self

        self._location = None
        self._completed = False

        # Initialise as True, and change if debug mode is set
        self._saving_enabled = True

        ensure_dir(os.path.dirname(self._status_file))
        if not os.path.exists(self._status_file):
            self.save()
        else:
            self.load()

    def load(self):
        with open(self._status_file, 'r') as status_file:
            try:
                data = json.load(status_file)
            except Exception:
                # Initialise the file again if it is corrupted
                logger.warn("The status file was corrupted.")
                self.save()
                return

            if 'location' in data:
                self._location = data['location']

            if 'completed' in data:
                self._completed = data['completed']

    def save(self):
        if not self._saving_enabled:
            return

        data = {
            'location': self._location,
            'completed': self._completed
        }

        with open(self._status_file, 'w') as status_file:
            json.dump(data, status_file)

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, c):
        self._completed = c

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def debug_mode(self):
        return not self._saving_enabled

    def set_debug_mode(self, start_from):
        self._saving_enabled = False
        self._location = start_from
