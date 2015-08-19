# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import subprocess
from gi.repository import Gtk
from kano.gtk3.buttons import KanoButton

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class
from kano_init_flow.ui.css import apply_styling_to_screen

from kano.network import is_internet


class Wifi(Stage):
    """
        The internet connection stage
    """

    id = 'wifi'
    _root = __file__

    def __init__(self, ctl):
        super(Wifi, self).__init__(ctl)

        apply_styling_to_screen(self.css_path('console.css'))

    def first_step(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1.widget)

    def second_scene(self):
        s2 = self._setup_second_scene()
        self._ctl.main_window.push(s2.widget)

    def third_scene(self):
        s3 = self._setup_third_scene()
        self._ctl.main_window.push(s3.widget)

    def next_stage(self):
        self._stage.ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('space-1-bg-4-3.png'),
                             self.media_path('space-1-bg-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('character.png')),
            Placement(0.08, 0.9, 0.45),
            Placement(0.12, 0.9, 0.5)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.png')),
            Placement(0.9, 0.9, 0.65),
            Placement(0.9, 0.9, 0.75)
        )

        scene.add_widget(
            SpeechBubble(text='Wicked', source=SpeechBubble.RIGHT),
            Placement(0.78, 0.72),
            Placement(0.79, 0.68)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('console.gif')),
            Placement(0.35, 0.925, 0.8),
            Placement(0.367, 0.888),
            self.second_scene
        )

        return scene

    def _setup_second_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            WifiConsole(self, self.third_scene),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0)
        )

        return scene

    def _setup_third_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('space-2-bg-4-3.png'),
                             self.media_path('space-2-bg-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('character.png')),
            Placement(0.08, 0.9, 0.45),
            Placement(0.12, 0.9, 0.5)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.png')),
            Placement(0.9, 0.9, 0.65),
            Placement(0.9, 0.9, 0.75)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('rocket.gif')),
            Placement(0.697, 0.597, 0.8),
            Placement(0.695, 0.275),
            self.first_scene
        )

        scene.add_widget(
            SpeechBubble(text='Wicked', source=SpeechBubble.RIGHT),
            Placement(0.78, 0.72),
            Placement(0.79, 0.68)
        )

        return scene

class WifiConsole(Gtk.Overlay):

    def __init__(self, stage, next_cb):
        super(WifiConsole, self).__init__()

        self._stage = stage
        self._next_cb = next_cb

        bg = Gtk.Image.new_from_file(self._stage.media_path('console-large.png'))
        fixed = Gtk.Fixed()

        self._eb = Gtk.EventBox()
        add_class(self._eb, 'console-content-area')
        self._eb.set_size_request(719, 543)

        self.add(bg)
        self.add_overlay(fixed)
        fixed.put(self._eb, 146, 157)

        self._eb.set_border_width(10)

        self.parental_question_screen()

    def parental_question_screen(self):
        self._clear()
        screen = ParentalScreen(self._stage, self.parental_screen, self.wifi_screen)
        self._eb.add(screen)
        self._eb.show_all()

    def parental_screen(self):
        self._clear()
        socket = ParentalControlGUI(self.wifi_screen)
        screen = ExternalApp(socket)

        eb = Gtk.EventBox()
        eb.add(screen)
        eb.set_margin_top(40)
        eb.set_margin_left(10)
        eb.set_margin_right(10)
        eb.set_margin_bottom(40)

        self._eb.add(eb)
        self._eb.show_all()

    def wifi_screen(self):
        self._clear()
        socket = WifiGUI(self._next_cb, self.troubleshoot_ethernet)
        screen = ExternalApp(socket)

        eb = Gtk.EventBox()
        eb.add(screen)
        eb.set_margin_top(30)
        eb.set_margin_left(100)
        eb.set_margin_right(100)
        eb.set_margin_bottom(20)

        self._eb.add(eb)
        self._eb.show_all()

    def troubleshoot_ethernet(self):
        self._clear()
        copy = """If you have access to an ethernet cable, try using that instead."""
        screen = SlideScreen(
            self._stage,
            self._stage.media_path('ethernet-cable.png'),
            0.0, 0.3, copy, 280,
            self.parental_question_screen,
            self.troubleshoot_router
        )

        self._eb.add(screen)
        self._eb.show_all()

    def troubleshoot_router(self):
        self._clear()
        copy = """Try moving your Kano closer to the internet wireless router."""
        screen = SlideScreen(
            self._stage,
            self._stage.media_path('router.png'),
            1.0, 0.25, copy, 330,
            self.troubleshoot_ethernet,
            self.parental_question_screen
        )
        self._eb.add(screen)
        self._eb.show_all()

    def _clear(self):
        for child in self._eb.get_children():
            self._eb.remove(child)


class ParentalScreen(Gtk.VBox):
    def __init__(self, stage, now_cb, later_cb):
        super(ParentalScreen, self).__init__(False, 0)

        self.set_hexpand(False)
        self.set_vexpand(False)
        self.set_margin_left(40)
        self.set_margin_right(40)

        heading = Gtk.Label('Parental controls')
        add_class(heading, 'console-screen-heading')

        desc = Gtk.Label("""Kano Wifi is a safe place for kids, and you can set specific safety guidelines yourself.""")
        desc.set_line_wrap(True)
        add_class(desc, 'console-screen-desc')

        # TODO: Add image
        padlock = Gtk.Image.new_from_file(stage.media_path('padlock.png'))

        now = KanoButton('SET NOW')
        now.connect('clicked', self._cb_wrapper, now_cb)

        later = KanoButton('LATER')
        later.connect('clicked', self._cb_wrapper, later_cb)

        buttons = Gtk.HBox(False, 0)
        buttons.pack_start(now, True, True, 20)
        buttons.pack_start(later, True, True, 0)

        self.pack_start(heading, False, False, 30)
        self.pack_start(desc, False, False, 20)
        self.pack_start(padlock, False, False, 10)
        self.pack_start(buttons, False, False, 30)

    def _cb_wrapper(self, widget, cb):
        cb()
        return True


class SlideScreen(Gtk.Overlay):
    def __init__(self, stage, bg_path, bg_x_align, bg_y_align, text, text_margin, back_cb, fwd_cb):
        super(SlideScreen, self).__init__()

        self._stage = stage
        bg = Gtk.Image.new_from_file(bg_path)
        align = Gtk.Alignment.new(bg_x_align, bg_y_align, 0, 0)
        align.add(bg)

        self.add(align)

        back = Gtk.Button()
        back.add(Gtk.Image.new_from_file(stage.media_path('navigation-arrow-left.png')))
        back.set_halign(Gtk.Align.CENTER)
        back.set_valign(Gtk.Align.CENTER)
        back.set_margin_left(25)
        back.connect('clicked', self._cb_wrapper, back_cb)

        fwd = Gtk.Button()
        fwd.add(Gtk.Image.new_from_file(stage.media_path('navigation-arrow-right.png')))
        fwd.set_halign(Gtk.Align.CENTER)
        fwd.set_valign(Gtk.Align.CENTER)
        fwd.set_margin_right(25)
        fwd.connect('clicked', self._cb_wrapper, fwd_cb)

        help_text = Gtk.Label(text)
        add_class(help_text, 'console-screen-help-text')
        help_text.set_line_wrap(True)
        help_text.set_justify(Gtk.Justification.CENTER)
        help_text.set_valign(Gtk.Align.CENTER)
        help_text.set_halign(Gtk.Align.CENTER)
        help_text.set_margin_left(20)
        help_text.set_margin_right(20)
        help_text.set_margin_top(text_margin)

        hbox = Gtk.HBox(False, 0)
        hbox.pack_start(back, False, False, 0)
        hbox.pack_start(help_text, True, False, 0)
        hbox.pack_start(fwd, False, False, 0)

        self.add_overlay(hbox)

    def _cb_wrapper(self, widget, cb):
        cb()
        return True


class ExternalApp(Gtk.Overlay):
    def __init__(self, socket_widget):
        super(ExternalApp, self).__init__()

        # TODO: Needs changing
        loading_label = Gtk.Label("LOADING {}".format(socket_widget.__class__.__name__))
        add_class(loading_label, 'console-screen-loading')
        self.add(loading_label)
        socket = socket_widget
        self.add_overlay(socket)


class ConsoleSocket(Gtk.Socket):
    def __init__(self):
        super(ConsoleSocket, self).__init__()
        self.get_style_context().add_class("console_socket")


class ParentalControlGUI(ConsoleSocket):
    # For now, make the kano-settings path local while it's not installed
    # by default on the system
    def __init__(self, wifi_cb):
        super(ParentalControlGUI, self).__init__()
        self.connect("map-event", self.launch_parental_control)
        self.connect("plug-removed", self._cb_wrapper, wifi_cb)

    def _cb_wrapper(self, widget, wifi_cb):
        wifi_cb()
        return True

    def launch_parental_control(self, widget, event):
        script_path = os.path.join("/usr/bin/kano-settings")
        socket_id = self.get_id()
        cmd = "sudo {} --plug={} --onescreen --label=advanced".format(
            script_path, socket_id
        )
        subprocess.Popen(cmd, shell=True)


class WifiGUI(ConsoleSocket):
    def __init__(self, success_cb, fail_cb):
        super(WifiGUI, self).__init__()
        self.connect("map-event", self.launch_wifi_gui)
        self.connect("plug-removed", self._cb_wrapper, success_cb, fail_cb)

    def _cb_wrapper(self, widget, success_cb, fail_cb):
        # if there is internet, then the user suceeded with connecting
        if is_internet():
            success_cb()
        else:
            fail_cb()

    def launch_wifi_gui(self, widget, event):
        script_path = os.path.join("/usr/bin/kano-wifi-gui")
        socket_id = self.get_id()
        cmd = "sudo {} --plug={}".format(script_path, socket_id)
        subprocess.Popen(cmd, shell=True)
