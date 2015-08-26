# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
from gi.repository import Gtk

from kano.gtk3.buttons import KanoButton
from kano.utils import is_monitor
from kano_settings.system.display import get_overscan_status, \
    write_overscan_values, set_overscan_status, launch_pipe


from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.ui.utils import cb_wrapper


class Quests(Stage):
    """
        The overscan setting window
    """

    id = 'quests'
    _root = __file__

    def __init__(self, ctl):
        super(Quests, self).__init__(ctl)

        apply_styling_to_screen(self.css_path('quests.css'))

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def second_scene(self):
        s = self._setup_second_scene()
        self._ctl.main_window.push(s.widget)

    def third_scene(self):
        s = self._setup_third_scene()
        self._ctl.main_window.push(s.widget)

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('quests-4-3.png'),
                             self.media_path('quests-16-9.png'))

        # Character path in the home directory
        character_path = os.path.join(
            os.path.expanduser("~"),
            ".character-content/character.png"
        )

        scene.add_widget(
            Gtk.Image.new_from_file(character_path),
            Placement(0.08, 0.9, 0.7),
            Placement(0.12, 0.9, 0.7)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('judoka.png')),
            Placement(0.6, 0.4, 1.0),
            Placement(0.62, 0.2, 1.0)
        )

        scene.add_widget(
            SpeechBubble(
                text="You did it! Now you know how\nto control your computer.\nThis was the first of many\nquests you'll find in the\nWorld of Kano",
                source=SpeechBubble.RIGHT
            ),
            Placement(0.22, 0.27),
            Placement(0.35, 0.18)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path("next-button.gif")),
            Placement(0.3, 0.5, 0),
            Placement(0.37, 0.43, 0),
            self.second_scene
        )

        return scene

    def _setup_second_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('quests-4-3.png'),
                             self.media_path('quests-16-9.png'))

        # Character path in the home directory
        character_path = os.path.join(
            os.path.expanduser("~"),
            ".character-content/character.png"
        )

        scene.add_widget(
            Gtk.Image.new_from_file(character_path),
            Placement(0.08, 0.9, 0.7),
            Placement(0.12, 0.9, 0.7)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('shine.gif')),
            Placement(0.52, 0.31, 1.0),
            Placement(0.553, 0.2, 1.0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('judoka.png')),
            Placement(0.6, 0.4, 1.0),
            Placement(0.62, 0.2, 1.0),
            self.third_scene
        )

        scene.add_widget(
            SpeechBubble(
                text="Click on my scroll to find\nout more and start the\nnext adventure...",
                source=SpeechBubble.RIGHT
            ),
            Placement(0.22, 0.27),
            Placement(0.35, 0.18)
        )

        '''scene.add_widget(
            Notebook(self, self.second_scene),
            Placement(0.45, 0.5, 0.0),
            Placement(0.45, 0.5, 0.0)
        )'''

        return scene

    def _setup_third_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            Scroll(self),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0)
        )

        return scene


class Scroll(Gtk.Overlay):
    def __init__(self, stage):
        super(Scroll, self).__init__()

        self._stage = stage

        self.add(Gtk.Image.new_from_file(stage.media_path('scroll.png')))

        fixed = Gtk.Fixed()
        self.add_overlay(fixed)

        self._eb = Gtk.EventBox()
        add_class(self._eb, 'scroll-content-area')
        self._eb.set_size_request(450, 487)

        fixed.put(self._eb, 100, 95)

        vbox = Gtk.VBox(False, 0)
        vbox.set_vexpand(True)
        vbox.set_hexpand(True)
        vbox.set_margin_left(10)
        vbox.set_margin_right(10)
        self._vbox = vbox
        self._eb.add(self._vbox)

        self.first_scroll()

    def first_scroll(self):
        self._clear()
        copy = [
            "Quests are a series of tasks that you",
            "can complete on your Kano to get",
            "great rewards."
        ]
        text_widgets = self._get_text_widgets(copy)

        chest = Gtk.Image.new_from_file(self._stage.media_path('chest-closed.png'))

        button = KanoButton('NEXT', color='orange')
        button.connect('clicked', cb_wrapper, self.second_scroll)

        text_widgets[0].set_margin_top(30)
        for w in text_widgets:
            self._vbox.pack_start(w, False, False, 0)

        chest.set_margin_top(60)
        self._vbox.pack_start(chest, False, False, 0)

        button.set_margin_top(70)
        button.set_margin_left(80)
        button.set_margin_right(80)
        self._vbox.pack_start(button, False, False, 0)

        self.show_all()

    def second_scroll(self):
        self._clear()
        ticks = Gtk.Image.new_from_file(self._stage.media_path('ticks.png'))

        copy = [
            "Complete all of the ticks in a",
            "quest to unlock rewards."
        ]
        text_widgets = self._get_text_widgets(copy)

        chest = Gtk.Image.new_from_file(self._stage.media_path('chest-open.png'))

        button = KanoButton('NEXT', color='orange')
        button.connect('clicked', cb_wrapper, self.third_scroll)

        ticks.set_margin_top(20)
        self._vbox.pack_start(ticks, False, False, 0)

        text_widgets[0].set_margin_top(40)
        for w in text_widgets:
            self._vbox.pack_start(w, False, False, 0)

        chest.set_margin_top(35)
        self._vbox.pack_start(chest, False, False, 0)

        button.set_margin_top(40)
        button.set_margin_left(80)
        button.set_margin_right(80)
        self._vbox.pack_start(button, False, False, 0)

        self.show_all()

    def third_scroll(self):
        self._clear()

        heading = Gtk.Label('New quest')
        add_class(heading, 'scroll-heading')

        world = Gtk.Image.new_from_file(self._stage.media_path('world.png'))

        copy = [
            "Journey to Kano World",
        ]
        text_widgets = self._get_text_widgets(copy)

        button = KanoButton('OK', color='orange')
        button.connect('clicked', cb_wrapper, self._stage._ctl.next_stage)

        heading.set_margin_top(35)
        self._vbox.pack_start(heading, False, False, 0)

        world.set_margin_top(35)
        self._vbox.pack_start(world, False, False, 0)

        text_widgets[0].set_margin_top(40)
        for w in text_widgets:
            self._vbox.pack_start(w, False, False, 0)

        button.set_margin_top(40)
        button.set_margin_left(80)
        button.set_margin_right(80)
        self._vbox.pack_start(button, False, False, 0)

        self.show_all()

    def _clear(self):
        for w in self._vbox.get_children():
            self._vbox.remove(w)
            w.destroy()

    def _get_text_widgets(self, lines):
        widgets = []
        for line in lines:
            label = Gtk.Label(line)
            label.set_line_wrap(False)
            label.set_justify(Gtk.Justification.LEFT)
            add_class(label, 'scroll-text')
            label.set_margin_bottom(8)
            widgets.append(label)

        return widgets
