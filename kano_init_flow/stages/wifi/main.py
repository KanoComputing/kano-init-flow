# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import subprocess
import threading

from gi.repository import Gtk, GLib
from kano.gtk3.buttons import KanoButton, OrangeButton
from kano.gtk3.cursor import attach_cursor_events
from kano.logging import logger
from kano_profile.tracker import track_action

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, ActiveImage
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.ui.components import NextButton

from kano.network import is_internet


class Wifi(Stage):
    """
        The internet connection stage
    """

    id = 'wifi'
    _root = __file__

    def __init__(self, ctl):
        super(Wifi, self).__init__(ctl)

        self._tries = 0
        apply_styling_to_screen(self.css_path('console.css'))

    def first_scene(self):
        # This is very slow
        if is_internet():
            self._ctl.next_stage()
            return

        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1)

    def second_scene(self):
        # TODO: uncomment before release
        # Jump directly at the end if we have internet
        if is_internet():
            track_action('init-flow-connected-already')
            self.connected_scene()
            return

        s2 = self._setup_second_scene()
        self._ctl.main_window.push(s2)

    def connected_scene(self):
        track_action('init-flow-connected')
        s3 = self._setup_connected_scene()
        self._ctl.main_window.push(s3)

    def disconnected_scene(self):
        track_action('init-flow-disconnected')
        s4 = self._setup_disconnected_scene()
        self._ctl.main_window.push(s4)

    def new_try(self):
        self._tries += 1
        if self._tries > 1:
            track_action('init-flow-wifi-retried')

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('space-1-bg-4-3.png'),
                             self.media_path('space-1-bg-16-9.png'))

        # scene.add_profile_icon()

        # scene.add_character(
        #    Placement(0.08, 0.9, 0.5),
        #    Placement(0.12, 0.9, 0.6)
        # )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.png')),
            Placement(0.9, 0.9, 0.65),
            Placement(0.9, 0.9, 0.75)
        )

        copy = [
            'Let\'s connect to the web!',
            '',
            'Get started by clicking',
            'the Wifi console!'
        ]
        sb = SpeechBubble(text='\n'.join(copy), source=SpeechBubble.BOTTOM,
                          scale=scene.scale_factor)
        scene.add_widget(
            sb,
            Placement(0.95, 0.55),
            Placement(0.94, 0.46)
        )

        scene.add_widget(
            ActiveImage(self.media_path('console.gif'),
                        hover=self.media_path('console-hover.gif')),
            Placement(0.35, 0.925, 0.8),
            Placement(0.367, 0.888),
            self.second_scene
        )

        scene.schedule(20, self._show_console_hint, scene, sb)

        return scene

    def _show_console_hint(self, scene, sb):
        sb.set_text("Click on the console\n" +
                    "in the lower part of\n" +
                    "the screen to continue.")
        scene.add_arrow(
            'down',
            Placement(0.36, 0.51),
            Placement(0.39, 0.4),
        )

    def _setup_second_scene(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        # scene.add_profile_icon()

        scene.add_widget(
            WifiConsole(self, self.connected_scene, self.next_stage),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0)
        )

        return scene

    def _setup_connected_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('space-2-bg-4-3.png'),
                             self.media_path('space-2-bg-16-9.png'))

        # scene.add_profile_icon()

        # scene.add_character(
        #    Placement(0.08, 0.9, 0.5),
        #    Placement(0.12, 0.9, 0.6)
        # )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.png')),
            Placement(0.9, 0.9, 0.65),
            Placement(0.9, 0.9, 0.75)
        )

        scene.add_widget(
            ActiveImage(self.media_path('rocket.gif'),
                        hover=self.media_path('rocket-hover.gif')),
            Placement(0.697, 0.597, 0.8),
            Placement(0.695, 0.275),
            self.next_stage
        )

        copy = 'We have signal! Great work.\n\n' + \
               'All aboard!\nWe can still make it on time!'
        scene.add_widget(
            SpeechBubble(text=copy, source=SpeechBubble.BOTTOM,
                         scale=scene.scale_factor),
            Placement(0.97, 0.57),
            Placement(0.95, 0.46)
        )

        scene.schedule(20, self._show_rocket_hint, scene)

        return scene

    def _show_rocket_hint(self, scene):
        scene.add_arrow(
            'right',
            Placement(0.45, 0.51),
            Placement(0.5, 0.3),
        )

    def _setup_disconnected_scene(self):
        scene = Scene(self._ctl.main_window)
        scene.set_background(self.media_path('space-1-bg-4-3.png'),
                             self.media_path('space-1-bg-16-9.png'))

        # scene.add_profile_icon()

        # scene.add_character(
        #    Placement(0.08, 0.9, 0.5),
        #    Placement(0.12, 0.9, 0.6)
        # )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('spaceman.png')),
            Placement(0.9, 0.9, 0.65),
            Placement(0.9, 0.9, 0.75)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('console.gif')),
            Placement(0.35, 0.925, 0.8),
            Placement(0.367, 0.888),
            self.second_scene
        )

        copy = [
            'Oh no, connection failed!',
            'We won\'t be able to make it',
            'to Kano World.',
            '',
            'To try again, click the console.'
        ]
        scene.add_widget(
            SpeechBubble(text='\n'.join(copy), source=SpeechBubble.BOTTOM,
                         scale=scene.scale_factor),
            Placement(0.97, 0.57),
            Placement(0.95, 0.46)
        )

        scene.add_widget(
            NextButton(),
            Placement(0.5, 0.99, 0),
            Placement(0.45, 0.99, 0),
            self.next_stage
            # key=Gdk.KEY_space
        )

        scene.schedule(20, self._show_rocket_hint, scene)

        return scene


class WifiConsole(Gtk.Overlay):

    def __init__(self, stage, connected_cb, disconnected_cb):
        super(WifiConsole, self).__init__()

        self._stage = stage
        self._connected_cb = connected_cb
        self._disconnected_cb = disconnected_cb

        console_img_path = self._stage.media_path('console-large.png')
        bg = Gtk.Image.new_from_file(console_img_path)
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
        screen = ParentalScreen(self._stage,
                                self.parental_screen,
                                self.wifi_screen)
        self._eb.add(screen)
        self._eb.show_all()

    def parental_screen(self):
        self._clear()
        socket = ParentalControlGUI(self.wifi_screen)
        screen = ExternalApp(self._stage, socket)

        eb = Gtk.EventBox()
        eb.add(screen)
        eb.set_margin_top(20)
        eb.set_margin_left(10)
        eb.set_margin_right(10)
        eb.set_margin_bottom(20)

        self._eb.add(eb)
        self._eb.show_all()

    def wifi_screen(self):
        self._clear()
        socket = WifiGUI(self._connected_cb, self.troubleshoot_option)
        screen = ExternalApp(self._stage, socket)

        self._stage.new_try()

        eb = Gtk.EventBox()
        eb.add(screen)

        eb.set_margin_top(40)
        eb.set_margin_left(10)
        eb.set_margin_right(10)
        eb.set_margin_bottom(40)

        self._eb.add(eb)
        self._eb.show_all()

    def troubleshoot_option(self):
        self._clear()
        screen = TroubleshootOrDisconnect(
            self._stage,
            self.troubleshoot_ethernet,
            self.are_you_sure
        )
        self._eb.add(screen)
        self._eb.show_all()

        track_action('init-flow-wifi-troubleshoot-triggered')

    def troubleshoot_ethernet(self):
        self._clear()
        copy = 'If you have access to an ethernet cable, ' +\
               'try using that instead.'
        screen = SlideScreen(
            self._stage,
            self._stage.media_path('ethernet-cable.png'),
            0.0, 0.3, copy, 280,
            self.wifi_screen,
            self.troubleshoot_router
        )

        self._eb.add(screen)
        self._eb.show_all()

    def troubleshoot_router(self):
        self._clear()
        copy = 'Try moving your Kano closer to the internet wireless router.'
        screen = SlideScreen(
            self._stage,
            self._stage.media_path('router.png'),
            1.0, 0.25, copy, 330,
            self.troubleshoot_ethernet,
            self.contact_us
        )
        self._eb.add(screen)
        self._eb.show_all()

    def contact_us(self):
        self._clear()
        copy = 'Having trouble connecting? Find us at help.kano.me and we\'ll come to the rescue!'
        screen = SlideScreen(
            self._stage,
            self._stage.media_path('judoka-call-centre.png'),
            0.5, 0.37, copy, 200,
            self.troubleshoot_router,
            self.wifi_screen
        )
        self._eb.add(screen)
        self._eb.show_all()

    def are_you_sure(self):
        self._clear()
        screen = AreYouSure(self._stage,
                            self.wifi_screen,
                            self._disconnected_cb)

        self._eb.add(screen)
        self._eb.show_all()

    def _clear(self):
        for child in self._eb.get_children():
            self._eb.remove(child)


class TroubleshootOrDisconnect(Gtk.Box):
    def __init__(self, stage, troubleshoot_cb, skip_cb):
        super(TroubleshootOrDisconnect, self).__init__(
            orientation=Gtk.Orientation.VERTICAL
        )

        self._stage = stage

        self.set_hexpand(False)
        self.set_vexpand(False)
        self.set_margin_left(40)
        self.set_margin_right(40)

        # heading = Gtk.Label('Troubleshoot')
        # add_class(heading, 'console-screen-heading')

        desc = Gtk.Label('Oops there was a problem connecting to internet.')
        desc.set_line_wrap(True)
        add_class(desc, 'console-screen-desc')

        img_path = self._stage.media_path("troubleshooting.png")
        image = Gtk.Image.new_from_file(img_path)

        troubleshoot = KanoButton('FIX IT')
        troubleshoot.connect('clicked', self._cb_wrapper, troubleshoot_cb)

        skip = KanoButton('SKIP', color="orange")
        skip.connect('clicked', self._cb_wrapper, skip_cb)

        buttons = Gtk.HBox(False, 0)
        buttons.pack_start(troubleshoot, True, True, 20)
        buttons.pack_start(skip, True, True, 0)

        # self.pack_start(heading, False, False, 30)
        self.pack_start(desc, False, False, 40)
        self.pack_start(image, False, False, 20)
        self.pack_start(buttons, False, False, 30)

    def _cb_wrapper(self, widget, cb):
        cb()
        return True


class AreYouSure(Gtk.Box):
    def __init__(self, stage, try_again_cb, skip_cb):
        super(AreYouSure, self).__init__(orientation=Gtk.Orientation.VERTICAL)

        self._stage = stage

        self.set_hexpand(False)
        self.set_vexpand(False)
        self.set_margin_left(40)
        self.set_margin_right(40)

        heading = Gtk.Label('Are You Sure?')
        heading.set_margin_top(20)
        add_class(heading, 'console-screen-heading')

        desc = Gtk.Label(
            "Kano uses WiFi to stay up to date" +
            "\nwith all new software updates, apps" +
            "\nand features."
        )
        desc.set_justify(Gtk.Justification.CENTER)
        desc.set_line_wrap(True)
        add_class(desc, 'console-screen-desc')

        try_again = KanoButton('TRY AGAIN')
        try_again.connect('clicked', self._cb_wrapper, try_again_cb)

        skip = KanoButton('YES I WANT TO SKIP', color="grey")
        skip.connect('clicked', self._cb_wrapper, skip_cb,
                     'init-flow-wifi-skipped')

        buttons = Gtk.HBox(False, 0)
        buttons.pack_start(try_again, True, True, 20)
        buttons.pack_start(skip, True, True, 0)

        self.pack_start(heading, False, False, 30)
        self.pack_start(desc, False, False, 40)
        self.pack_start(buttons, False, False, 40)

    def _cb_wrapper(self, widget, cb, tracking_event=None):
        if tracking_event:
            track_action(tracking_event)
        cb()
        return True


class ParentalScreen(Gtk.VBox):
    def __init__(self, stage, now_cb, later_cb):
        super(ParentalScreen, self).__init__(False, 0)

        self.set_hexpand(False)
        self.set_vexpand(False)
        self.set_margin_left(40)
        self.set_margin_right(40)

        heading = Gtk.Label('Parental controls')
        add_class(heading, 'console-screen-heading')

        copy = 'Allow Kano content + updates in, ' + \
               'keep suspicious websites out!'
        desc = Gtk.Label(copy)
        desc.set_line_wrap(True)
        add_class(desc, 'console-screen-desc')

        # TODO: Add image
        padlock = Gtk.Image.new_from_file(stage.media_path('padlock.png'))

        later = KanoButton('GOT IT')
        later.connect('clicked', self._cb_wrapper, later_cb, 'init-flow-parental-skipped')
        later.set_size_request(200, 50)

        now = OrangeButton('SET NOW')
        now.connect('clicked', self._cb_wrapper, now_cb, 'init-flow-parental-set')

        emptylabel = Gtk.Label("       ")

        buttons = Gtk.ButtonBox()
        buttons.set_layout(Gtk.ButtonBoxStyle.SPREAD)
        buttons.pack_start(emptylabel, True, True, 0)
        buttons.pack_start(later, True, True, 20)
        buttons.pack_start(now, True, True, 20)

        self.pack_start(heading, False, False, 30)
        self.pack_start(desc, False, False, 20)
        self.pack_start(padlock, False, False, 10)
        self.pack_start(buttons, True, True, 30)

    def _cb_wrapper(self, widget, cb, tracking_event=None):
        if tracking_event:
            track_action(tracking_event)
        cb()
        return True


class SlideScreen(Gtk.Overlay):
    def __init__(self, stage, bg_path, bg_x_align, bg_y_align, text,
                 text_margin, back_cb, fwd_cb):
        super(SlideScreen, self).__init__()

        self._stage = stage
        bg = Gtk.Image.new_from_file(bg_path)
        align = Gtk.Alignment.new(bg_x_align, bg_y_align, 0, 0)
        align.add(bg)

        self.add(align)

        back = Gtk.Button()
        back_arr = stage.media_path('navigation-arrow-left.png')
        back.add(Gtk.Image.new_from_file(back_arr))
        back.set_halign(Gtk.Align.CENTER)
        back.set_valign(Gtk.Align.CENTER)
        back.set_margin_left(25)
        back.connect('clicked', self._cb_wrapper, back_cb)
        attach_cursor_events(back)

        fwd = Gtk.Button()
        fwd_arr = stage.media_path('navigation-arrow-right.png')
        fwd.add(Gtk.Image.new_from_file(fwd_arr))
        fwd.set_halign(Gtk.Align.CENTER)
        fwd.set_valign(Gtk.Align.CENTER)
        fwd.set_margin_right(25)
        fwd.connect('clicked', self._cb_wrapper, fwd_cb)
        attach_cursor_events(fwd)

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
    def __init__(self, stage, socket_widget):
        super(ExternalApp, self).__init__()
        self.loading_bar = Gtk.Image.new_from_file(
            stage.media_path("loading_bar.gif")
        )
        self.add(self.loading_bar)

        # Pack the socket in a box so the socket doesn't stretch to
        # fill the overlay
        box = Gtk.Box()
        box.pack_start(socket_widget, False, False, 0)
        self.add_overlay(box)


class ConsoleContainer(Gtk.Fixed):
    width = 690
    height = 543

    def __init__(self):
        super(ConsoleContainer, self).__init__()

        self.socket = Gtk.Socket()
        self.socket.connect("map-event", self.launch_plug_process)
        self.get_style_context().add_class("console_socket")
        self.put(self.socket, 0, 0)
        self._unplug_called = False
        self.socket.connect("plug-added", self.resize_image)

    def resize_image(self, widget):
        self.socket.set_size_request(self.width, self.height)

    def launch_plug_process(self, widget, event):
        thread = threading.Thread(target=self._do_launch_plug_process)
        thread.daemon = True
        thread.start()

    def _do_launch_plug_process(self):
        pass

    def _emit_plug_removed(self):
        self.socket.emit('plug-removed')


class ParentalControlGUI(ConsoleContainer):
    height = 500

    # For now, make the kano-settings path local while it's not installed
    # by default on the system
    def __init__(self, wifi_cb):
        super(ParentalControlGUI, self).__init__()
        self.socket.connect("plug-removed", self._cb_wrapper, wifi_cb)

    def _cb_wrapper(self, widget, wifi_cb):
        if not self._unplug_called:
            self._unplug_called = True
            wifi_cb()

    def _do_launch_plug_process(self):
        try:
            script_path = os.path.join("/usr/bin/kano-settings")
            socket_id = self.socket.get_id()
            cmd = "sudo {} --plug={} --onescreen --label=set-parental-password".format(
                script_path, socket_id
            )

            p = subprocess.Popen(cmd, shell=True)
            p.wait()
        except Exception:
            # We need to make sure this doesn't kill the init flow
            logger.warn('kano-settings failed during the init flow')

        GLib.idle_add(self._emit_plug_removed)


class WifiGUI(ConsoleContainer):

    # There are two callbacks passed.
    # The first is the space landscape shown when the user successfully
    # connects to the internet.
    # The second is the space landscape where you are prompted to connect
    # to the internet again.
    def __init__(self, connected_cb, fail_cb):
        super(WifiGUI, self).__init__()
        self.socket.connect(
            "plug-removed",
            self._cb_wrapper,
            connected_cb,
            fail_cb
        )

    def _cb_wrapper(self, widget, connected_cb, fail_cb):
        # if there is internet, then the user suceeded with connecting
        if is_internet():
            connected_cb()
        else:
            fail_cb()

    def _do_launch_plug_process(self):
        try:
            script_path = os.path.join("/usr/bin/kano-wifi-gui")
            socket_id = self.socket.get_id()
            cmd = "sudo {} --plug={}".format(script_path, socket_id)

            p = subprocess.Popen(cmd, shell=True)
            p.wait()
            # To get the returncode (which is 100 if the user clicks SKIP, use
            # p.returncode

        except Exception:
            # We need to make sure this doesn't kill the init flow
            logger.warn('kano-wifi-gui failed during the init flow')

        GLib.idle_add(self._emit_plug_removed)
