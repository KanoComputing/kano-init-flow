#!/usr/bin/env python

# common.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Common functions/utils
#

import json

def get_init_conf():
    """ Loads system boot config. """
    try:
        with open("/boot/init.conf", "r") as f:
            return json.load(f)
    except:
        return {}
