#!/usr/bin/env python

# data.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Data functions for getting level specific data from the json

import json


def get_data(stage):
    json_data = open('../data/tutorials.json')
    data = json.load(json_data)
    stage_data = data["TUTORIAL_" + str(stage)]
    return stage_data
