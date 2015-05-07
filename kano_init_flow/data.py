#!/usr/bin/env python

# data.py
#
# Copyright (C) 2014-2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Data functions for getting level specific data from the json

import json

from kano_init_flow.paths import DATA_FILE


def get_data(string):
    with open(DATA_FILE) as json_data:
        data = json.load(json_data)

    stage_data = data[string]

    return stage_data
