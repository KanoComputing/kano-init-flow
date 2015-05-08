# common.py
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Common functions/utils
#

import json

CONF_FILE = '/boot/init.conf'

def get_init_conf():
    """ Loads system boot config. """
    try:
        with open(CONF_FILE, 'r') as conf_file:
            return json.load(conf_file)
    except Exception:
        return {}
