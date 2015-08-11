# Parent for all Stages
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk
from .paths import get_asset_path


class Stage(object):
    def __init__(self):
        super(Stage, self).__init__()

        self._id = None
        self._root = None

    def get_widget(self):
        pass

    def media_path(self, filename):
        '''
            :params stage_path: the path of the current stage
            :type stage_path: str

            :params filename: the name of the file
            :type filename: str
        '''

        if not self._root:
            raise RuntimeError("Please define self._root == __file__")
        return get_asset_path(self._root, "media", filename)

    def css_path(self, filename):
        '''
            :params stage_path: the path of the current stage
            :type stage_path: str

            :params filename: the name of the file
            :type filename: str
        '''

        if not self._root:
            raise RuntimeError("Please define self._root == __file__")
        return get_asset_path(self._root, "CSS", filename)
