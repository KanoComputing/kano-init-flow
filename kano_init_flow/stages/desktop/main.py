# The desktop stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import subprocess
from gi.repository import Gtk, Gdk, GLib
from kano_profile.tracker import track_action

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.world_icon import WorldIcon
from kano_init_flow.ui.components import NextButton
from kano_avatar_gui.CharacterCreator import CharacterCreator
from kano.gtk3.buttons import KanoButton
from kano.logging import logger
from kano.gtk3.apply_styles import apply_styling_to_screen


class Desktop(Stage):
    """
        The desktop video replacement flow
    """

    id = 'desktop'
    _root = __file__

    def __init__(self, ctl):
        super(Desktop, self).__init__(ctl)

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def second_scene(self):
        s = self._setup_second_scene()
        self._ctl.main_window.push(s.widget)

    def third_scene(self):
        s = self._setup_third_scene()
        self._ctl.main_window.push(s.widget)

    def fourth_scene(self):
        s = self._setup_fourth_scene()
        self._ctl.main_window.push(s.widget)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):
        self._first_scene = scene = Scene(self._ctl.main_window)
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        # Pass the callback of what we want to launch in the profile icon
        scene.add_profile_icon(self._char_creator_window)

        # Add judoka
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("left-pointing-judoka.png")),
            Placement(0.4, 0.4),
            Placement(0.2, 0.4)
        )

        scene.add_widget(
            SpeechBubble(
                text='Welcome to the desktop!\n'
                     'Click on this icon to set up\n'
                     'your profile',
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.4, 0.1),
            Placement(0.2, 0.1)
        )

        # Shortcut
        '''
        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.5),
            Placement(0.5, 0.5),
            self.second_scene
        )
        '''

        return scene

    def _char_creator_window(self):
        self._blur = self._create_blur()

        # Add watch cursor
        watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
        self._ctl.main_window.get_window().set_cursor(watch_cursor)

        self._first_scene.add_widget(
            self._blur,
            Placement(0, 0),
            Placement(0, 0)
        )
        self._blur.get_style_context().add_class("blur")
        self._first_scene.show_all()

        while Gtk.events_pending():
            Gtk.main_iteration()

        CharacterWindow(self.second_scene, self.css_path("style.css"))
        self._ctl.main_window.get_window().set_cursor(None)

    def _setup_second_scene(self):
        self._second_scene = scene = Scene(self._ctl.main_window)
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_profile_icon()
        self._add_world_icon(scene, self._launch_registration)

        # Add judoka
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("right-pointing-judoka.png")),
            Placement(0.6, 0.45),
            Placement(0.8, 0.45)
        )

        scene.add_widget(
            SpeechBubble(
                text='This icon is Kano World!\n'
                     'This is where Judokas make\n'
                     'and share projects togther\n'
                     'online.',
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.6, 0.1),
            Placement(0.8, 0.1)
        )

        # Shortcut
        # scene.add_widget(
        #    NextButton(),
        #    Placement(0.5, 0.5),
        #    Placement(0.5, 0.5),
        #    self.third_scene
        # )

        return scene

    def _setup_third_scene(self):
        scene = Scene(self._ctl.main_window)
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_profile_icon()
        self._add_world_icon(scene)

        scene.add_widget(
            SpeechBubble(
                text='This is the Taskbar! Here you can\n'
                     'manage settings and make\n'
                     'changes to the computer.',
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.5, 0.4),
            Placement(0.5, 0.4)
        )
        # Add judoka
        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("taskbar-judoka.png")),
            Placement(0.5, 0.8),
            Placement(0.5, 0.8)
        )

        self._add_taskbar(scene)

        scene.add_widget(
            NextButton(),
            Placement(0.7, 0.8, 0),
            Placement(0.7, 0.8, 0),
            self.fourth_scene,
        )

        return scene

    def _setup_fourth_scene(self):
        scene = Scene(self._ctl.main_window)
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        # Pass the callback of what we want to launch in the profile icon
        scene.add_profile_icon()
        self._add_world_icon(scene)

        # Go through all the desktop icons and add them to the desktop
        # Either go through all files in a folder with a specific pattern, or
        # just list them in an array

        # All icons are in /usr/share/icons/Kano/88x88/apps (apart from the
        # translucent one)
        icon_grid = Gtk.Grid()
        icon_grid.set_row_spacing(50)
        icon_grid.set_column_spacing(50)
        parent_dir = "/usr/share/kano-desktop/icons"
        parent_dir_2 = "/usr/share/icons/Kano/88x88/apps"

        # Order the icons needed
        icon_files = [
            os.path.join(parent_dir, "snake.png"),
            os.path.join(parent_dir, "pong.png"),
            os.path.join(parent_dir, "make-minecraft.png"),
            os.path.join(parent_dir, "sonicpi.png"),
            os.path.join(parent_dir, "internet-desktop.png"),
            os.path.join(parent_dir, "apps.png"),
            os.path.join(parent_dir, "kano-homefolder.png"),
            os.path.join(parent_dir_2, "kano-draw.png"),
            os.path.join(parent_dir_2, "linux-story.png"),
            os.path.join(parent_dir, "scratch.png"),
            os.path.join(parent_dir_2, "video.png"),
            os.path.join(parent_dir, "plus-icon.png")

        ]
        row = 1
        column = 0

        for f in icon_files:
            icon = Gtk.Image.new_from_file(f)
            icon_grid.attach(icon, column, row, 1, 1)
            column += 1

            if column >= 7:
                column = 0
                row -= 1

        scene.add_widget(
            icon_grid,
            Placement(0.5, 0.9, 0),
            Placement(0.5, 0.9, 0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("apps-judoka.png")),
            Placement(0.7, 0.6),
            Placement(0.7, 0.6)
        )

        scene.add_widget(
            SpeechBubble(
                text='And these are your apps! With\n'
                     'them you can make amazing\n'
                     'code creations to share in\n'
                     'Kano World',
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.7, 0.25),
            Placement(0.7, 0.25)
        )

        scene.add_widget(
            NextButton(),
            Placement(0.8, 0.4, 0),
            Placement(0.8, 0.4, 0),
            self.next_stage
        )

        return scene

    def _add_world_icon(self, scene, callback=None):
        scene.add_widget(
            WorldIcon(),
            Placement(0.97, 0.05, 0),
            Placement(0.97, 0.05, 0),
            callback
        )

    def _add_taskbar(self, scene):
        # Need to collect the icons from the taskbar
        taskbar = Gtk.EventBox()

        # Make the the right width and height
        taskbar.set_size_request(scene.get_width(), 50)

        scene.add_widget(
            taskbar,
            Placement(1, 0, 0),
            Placement(1, 0, 0)
        )

        return taskbar

    def _launch_registration(self):
        self._blur = self._create_blur()

        # Add watch cursor
        watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
        self._ctl.main_window.get_window().set_cursor(watch_cursor)

        self._second_scene.add_widget(
            self._blur,
            Placement(0, 0),
            Placement(0, 0)
        )

        self._second_scene.show_all()

        while Gtk.events_pending():
            Gtk.main_iteration()

        try:
            p = subprocess.Popen(['/usr/bin/kano-login', '-r'])
            p.wait()
        except Exception:
            logger.debug("kano-login failed to launch")

        self._ctl.main_window.get_window().set_cursor(None)
        GLib.idle_add(self.next_stage)

    def _create_blur(self):
        blur = Gtk.EventBox()

        screen = Gdk.Screen.get_default()
        width = screen.get_width()
        height = screen.get_height()

        blur.get_style_context().add_class("blur")
        blur.set_size_request(width, height)
        return blur


class CharacterWindow(Gtk.Window):
    def __init__(self, cb, css_path):
        super(CharacterWindow, self).__init__()

        apply_styling_to_screen(css_path)
        self.get_style_context().add_class("character_window")
        self.set_decorated(False)
        self.close_cb = cb

        self.char_edit = CharacterCreator(randomise=True)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)

        vbox.pack_start(self.char_edit, False, False, 0)
        button = KanoButton("OK")
        button.connect("clicked", self.close_window)
        button.pack_and_align()

        self.connect("delete-event", Gtk.main_quit)
        self.set_keep_above(True)

        vbox.pack_start(button.align, False, False, 10)
        self.show_all()

        self.char_edit.show_pop_up_menu_for_category("judoka-faces")
        self.char_edit.select_category_button("judoka-faces")

    def close_window(self, widget):
        self.char_edit.save()
        self.destroy()
        GLib.idle_add(self.close_cb)
