# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
from gi.repository import Gtk, Gdk, GLib

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, ActiveImage
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_avatar_gui.CharacterCreator import CharacterCreator
from kano.gtk3.buttons import KanoButton
from kano_init_flow.ui.components import NextButton


class Wardrobe(Stage):
    """
        The first screen where the judoka introduces himself
    """

    id = 'wardrobe'
    _root = __file__

    def __init__(self, ctl):
        super(Wardrobe, self).__init__(ctl)
        apply_styling_to_screen(self.css_path("wardrobe.css"))

    def first_scene(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1)

    def second_scene(self):
        s2 = self._setup_second_scene()
        self._ctl.main_window.push(s2)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()

        scene.set_background(self.media_path('scene-1600x1200.png'),
                             self.media_path('scene-1920x1080.png'))

        self._first_scene = scene

        scene.add_widget(
            SpeechBubble(
                text=_("Let's dress up your\ncharacter!"),
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.9, 0.4),
            Placement(0.85, 0.45)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("tailor-judoka.png")),
            Placement(0.85, 0.8, 0.85),
            Placement(0.8, 0.9, 0.85)
        )

        scene.add_widget(
            ActiveImage(self.media_path("outline.gif"),
                        hover=self.media_path("outline-hover.png")),
            Placement(0.5, 0.7, 0.95),
            Placement(0.45, 0.72, 0.95),
            self._char_creator_window
        )

        return scene

    def _create_blur(self):
        blur = Gtk.EventBox()

        screen = Gdk.Screen.get_default()
        width = screen.get_width()
        height = screen.get_height()

        blur.set_size_request(width, height)
        return blur

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

        CharacterWindow(self.second_scene)

    def _setup_second_scene(self):
        self._ctl.main_window.get_window().set_cursor(None)
        scene = Scene(self._ctl.main_window)
        scene.set_background(self.media_path('scene-1600x1200.png'),
                             self.media_path('scene-1920x1080.png'))

        # Need to get the character at this point.
        char_path = os.path.join(
            os.path.expanduser("~"), ".character-content/character.png"
        )

        scene.add_widget(
            Gtk.Image.new_from_file(char_path),
            Placement(0.5, 0.65, 0.69),
            Placement(0.45, 0.65, 0.69)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path("tailor-judoka.png")),
            Placement(0.85, 0.8, 0.85),
            Placement(0.85, 0.8, 0.85)
        )

        scene.add_widget(
            SpeechBubble(
                text=_("You look amazing!"),
                source=SpeechBubble.BOTTOM,
                scale=scene.scale_factor
            ),
            Placement(0.9, 0.4),
            Placement(0.9, 0.4)
        )

        scene.add_profile_icon()

        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.95, 0),
            Placement(0.45, 0.95, 0),
            self.next_stage,
            key=Gdk.KEY_space
        )

        return scene

    def _next_stage_wrapper(self, widget, event):
        self.next_stage()


class CharacterWindow(Gtk.Window):
    def __init__(self, cb):
        super(CharacterWindow, self).__init__()
        self.get_style_context().add_class("character_window")
        self.set_decorated(False)
        self.close_cb = cb

        self.char_edit = CharacterCreator(randomise=True)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)

        vbox.pack_start(self.char_edit, False, False, 0)
        button = KanoButton(_("OK"))
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
