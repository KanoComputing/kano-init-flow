#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import os

# setting up directories
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

media_local_tutorial = os.path.join(dir_path, 'media', 'kano-tutorial')
media_usr_tutorial = '/usr/share/kano-init-flow/media/kano-tutorial'

if os.path.exists(media_local_tutorial):
    media_dir = media_local_tutorial
elif os.path.exists(media_usr_tutorial):
    media_dir = media_usr_tutorial
else:
    raise Exception('Neither local nor usr media dir found!')

local_tutorial = os.path.join(dir_path, 'kano_tutorial')
usr_tutorial = '/usr/lib/python2.7/dist-packages/kano_tutorial'

if os.path.exists(local_tutorial):
    tutorial_dir = local_tutorial
elif os.path.exists(usr_tutorial):
    tutorial_dir = usr_tutorial
else:
    raise Exception('Neither local nor usr css dir found!')

css_dir = os.path.join(tutorial_dir, "CSS")
