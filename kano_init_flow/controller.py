# The Controller class
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Controls the progression through the flow
#

import os
import json
from gi.repository import Gtk
from kano.logging import logger
from kano_profile.tracker import session_start, session_end, \
    track_data, track_action

from .status import Status
from .paths import OLD_FIRST_BOOT_FILE
from .ui.utils import trigger_led_speaker

from .stages.wifi import Wifi
from .stages.overscan_old import OverscanOld
from .stages.drag_and_drop import DragAndDrop
from .stages.quests import Quests
from .stages.audio_lab import AudioLab
from .stages.light_lab import LightLab
from .stages.bugs import Bugs
from .stages.intro import Intro
from .stages.wardrobe import Wardrobe
from .stages.blocks import Blocks
from .stages.kano_world import KanoWorld
from .stages.pi_hdmi import PiHdmi
from .stages.pi_wifi import PiWifi
from .stages.pi_keyboard import PiKeyboard
from .stages.pi_complete import PiComplete
from .stages.pi_audio import PiAudio
from .stages.desktop import Desktop


class Controller(object):
    """
        Controls the flow through the setup procedure.

        The MainWindow class uses it to determine what comes next.
    """

    INIT_CONF = '/boot/init.conf'

    FINISHED_FIRST_BOOT = 0  # 0 means that this was the first complete boot
    NOT_FIRST_BOOT = 1       # 1 means that the init flow was completed before

    def __init__(self, main_window, start_from=None):
        """
            :param start_from: Overrides the status and makes the init flow
                               start from this stage.
            :type start_from: str
        """

        self._main_window = main_window

        self._status = Status.get_instance()
        if start_from:
            self._status.set_debug_mode(start_from)

        # This is used to store values need for multiple screens
        # Referenced in self.get_var, self.set_var and self.has_var
        self._vars_map = {}

        self._return_value = self.FINISHED_FIRST_BOOT
        self._tracking_session = None

        self._stages = [
            Intro,
            PiHdmi,
            OverscanOld,
            PiKeyboard,
            DragAndDrop,
            Bugs,
            # Wardrobe,
            # Blocks,
            PiAudio,
            AudioLab,
            # LightLab,
            PiWifi,
            Wifi,
            # KanoWorld
            # Quests,
            PiComplete,
            Desktop
        ]

    @property
    def main_window(self):
        return self._main_window

    def first_stage(self):
        """
            Runs the first stage.

            Note: The first stage is determined by the location variable from
            the status file, not necessarily the very first stage.
        """

        if not self._status.debug_mode:
            if self._status.completed:
                self._return_value = self.NOT_FIRST_BOOT
                return False

            if os.path.exists(OLD_FIRST_BOOT_FILE):
                self._return_value = self.NOT_FIRST_BOOT
                self.complete()
                return False

            if self._should_skip_init_flow():
                self.complete()
                return False

        self._main_window.set_key_events_handlers()

        if len(self._stages):
            index = 0
            if self._status.location is not None:
                index = self._get_stage_index(self._status.location)
                track_data('init-flow-resumed', {'stage': self._status.location})
            else:
                track_action('init-flow-started')

            stage_ctl = self._stages[index](self)
            stage_ctl.first_scene()
        else:
            raise RuntimeError('No flow stages available')

        self._tracking_session = session_start(stage_ctl.id, os.getpid())
        return True

    def next_stage(self):
        """
            This callback is passed over to each stage to be called once
            it's over and the control should be handed to the subsequent one.
        """
        if self._status.location is None:
            self._status.location = self._stages[0].id
            index = 0
        else:
            index = self._get_stage_index(self._status.location)

        # Finish the previous tracking session
        if self._tracking_session is not None:
            session_end(self._tracking_session)

        self._main_window.set_key_events_handlers()

        if index is not None and index < len(self._stages) - 1:
            stage_ctl = self._stages[index + 1](self)
            self._status.location = self._stages[index + 1].id
            self._status.save()

            # Start a new tracking session
            self._tracking_session = session_start(stage_ctl.id, os.getpid())

            stage_ctl.first_scene()
            trigger_led_speaker()
        else:
            self._status.completed = True
            self._status.save()
            track_action('init-flow-finished')
            Gtk.main_quit()

    def complete(self):
        self._status.location = self._stages[-1].id
        self._status.completed = True
        self._status.save()

    def set_var(self, prop_name, value):
        self._vars_map[prop_name] = value

    def get_var(self, prop_name):
        if self.has_var(prop_name):
            return self._vars_map[prop_name]

        return None

    def has_var(self, prop_name):
        return prop_name in self._vars_map

    @property
    def return_value(self):
        return self._return_value

    def _get_stage_index(self, stage_id):
        index = None
        for i, s in enumerate(self._stages):
            if s.id == stage_id:
                index = i
                break

        return index

    def _get_stage_class_by_id(self, stage_id):
        index = self._get_stage_index(stage_id)
        return self._stages[index] if index else None

    def _should_skip_init_flow(self):
        if os.path.exists(self.INIT_CONF):
            with open(self.INIT_CONF, 'r') as f:
                try:
                    init_conf = json.load(f)
                    return ('kano_init_flow' in init_conf and
                            'skip' in init_conf['kano_init_flow'] and
                            init_conf['kano_init_flow']['skip'])
                except:
                    logger.warn('Failed to parse init.conf')

        return False
