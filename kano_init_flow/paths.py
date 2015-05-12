# paths.py
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Paths to resource files and directories
#

import os

def get_installed_dir(local_path, system_path, err_msg):
    """
    Get the installed directory, prioritising the local_path

    :param local_path: Development path to resource
    :param system_path: Installed system path to resource
    :err_msg: Error message to raise on error
    :returns: Directory which exists
    :raises Exception: If neither directory exists
    """

    if os.path.exists(local_path):
        return local_path
    elif os.path.exists(system_path):
        return system_path
    else:
        raise Exception(err_msg)

# setting up directories
DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PYTHON_DIR = '/usr/lib/python2.7/dist-packages/kano_init_flow'

MEDIA_DIR = get_installed_dir(
    local_path=os.path.join(DIR_PATH, 'media', 'kano-init-flow'),
    system_path='/usr/share/kano-init-flow/media/kano-init-flow',
    err_msg='Neither local nor usr media dir found!'
)


INIT_DIR = get_installed_dir(
    local_path=os.path.join(DIR_PATH, 'kano_init_flow'),
    system_path=PYTHON_DIR,
    err_msg='Neither local nor usr css dir found!'
)

CSS_DIR = os.path.join(INIT_DIR, 'CSS')
