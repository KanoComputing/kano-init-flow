#
# Path constants
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os

from kano.utils import get_home


STATUS_FILE_PATH = os.path.join(get_home(), '.init-flow.json')


def get_asset_path(stage_path, directory, filename):
    '''
        :params stage_path: the path of the current stage
        :type stage_path: str

        :params directory: the directory name we're interested in
        :type directory: str

        :params filename: the name of the file
        :type filename: str
    '''
    stage_dir = os.path.dirname(os.path.abspath(stage_path))
    path = os.path.join(stage_dir, directory, filename)

    if not os.path.exists(path):
        raise OSError("Path {} doesn't exist".format(path))

    return path


def common_css_path(filename):
    '''
        :params filename: the name of the file
        :type filename: str
    '''
    return get_asset_path(__file__, "ui/css", filename)


def common_media_path(filename):
    '''
        :params filename: the name of the file
        :type filename: str
    '''

    return get_asset_path(__file__, "ui/media", filename)
