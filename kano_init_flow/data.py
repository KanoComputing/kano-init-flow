#!/usr/bin/env python

# data.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Data functions for getting level specific data from the json

import json
import os


def get_data_file():

    # setting up local data path
    data_local = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'init-flow.json'))
    data_usr = "/usr/lib/python2.7/dist-packages/kano_init_flow/data/init-flow.json"

    if os.path.exists(data_local):
        data_file = data_local
    elif os.path.exists(data_usr):
        data_file = data_usr
    else:
        raise Exception('Neither local nor usr data found!')

    return data_file


def get_data(string):
    filename = get_data_file()
    json_data = open(filename)
    data = json.load(json_data)
    stage_data = data[string]
    return stage_data
