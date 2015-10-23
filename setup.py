#!/usr/bin/env python

# setup.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import os
from distutils.core import setup


pkg_data = ["media/*", "css/*"]


def get_stages():
    stages = []
    stages_root = 'kano_init_flow/stages'
    entries = os.listdir(stages_root)
    for e in entries:
        if os.path.isdir(os.path.join(stages_root, e)):
            stages.append("kano_init_flow.stages.{}".format(e))

    return stages


def get_stages_data():
    stages = get_stages()
    data = {}

    for s in stages:
        root = s.replace('.', '/')
        for f in pkg_data:
            subdir = f.split('/')[0]
            if os.path.isdir(os.path.join(root, subdir)):
                if s not in data:
                    data[s] = []
                data[s].append(f)

    return data


def merge_dicts(a, b):
    res = a.copy()
    res.update(b)
    return res

setup(
    name='kano-init-flow',
    version='2.2.0',
    description='The init flow for Kano OS',
    author='Kano Computing',
    author_email='help@kano.me',
    packages=['kano_init_flow', 'kano_init_flow.stages', 'kano_init_flow.ui',
              'kano_init_flow.kw_slideshow'] + get_stages(),
    scripts=['bin/kano-init-flow', 'bin/kano-init-flow-system-tool',
             'bin/kano-world-slideshow'],
    package_data=merge_dicts({"kano_init_flow.ui": pkg_data,
                              "kano_init_flow.kw_slideshow": pkg_data,
                             }, get_stages_data())
)
