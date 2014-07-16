#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import os

# setting up directories
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

media_local_init = os.path.join(dir_path, 'media', 'kano-init-flow')
media_usr_init = '/usr/share/kano-init-flow/media/kano-init-flow'

if os.path.exists(media_local_init):
    media_dir = media_local_init
elif os.path.exists(media_usr_init):
    media_dir = media_usr_init
else:
    raise Exception('Neither local nor usr media dir found!')

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

css_local_init = os.path.join(dir_path, 'kano_init_flow', 'CSS')
css_usr_init = '/usr/lib/python2.7/dist-packages/kano_init_flow/CSS'

if os.path.exists(css_local_init):
    css_dir = css_local_init
elif os.path.exists(css_usr_init):
    css_dir = css_usr_init
else:
    raise Exception('Neither local nor usr css dir found!')
