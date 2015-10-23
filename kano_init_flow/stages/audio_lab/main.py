# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk

from kano.gtk3.buttons import KanoButton
from kano.utils import play_sound, run_cmd
from kano_profile.tracker import track_action

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, ActiveImage
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.ui.utils import add_class, cb_wrapper, scale_image
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_settings.system.audio import hdmi_supported


class AudioLab(Stage):
    """
        The overscan setting window
    """

    id = 'audio-lab'
    _root = __file__

    def __init__(self, ctl):
        super(AudioLab, self).__init__(ctl)

        # Flag to check if the troubleshooting screen is open
        self._troubleshooting_open = False
        apply_styling_to_screen(self.css_path('audio-lab.css'))

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s)

    def help_leds(self):
        track_action('init-flow-audio-help-triggered')
        self.remove_overlays()
        self._setup_help_leds(self._scene)

    def help_power(self):
        self.remove_overlays()
        self._setup_help_power(self._scene)

    def help_jack(self):
        self.remove_overlays()

        # Set flag as troubleshooting screen is opened
        self._troubleshooting_open = True

        self._hide_console(self._scene)
        self._setup_help_jack(self._scene)

    def remove_overlays(self):
        # Set flag as troubleshooting screen is being closed
        self._troubleshooting_open = False

        for o in ['help-power', 'help-jack', 'help-leds']:
            self._scene.remove_widget(o)

    def _setup_first_scene(self):
        self._console_on = False

        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(self.media_path('audio-lab-bg-4-3.png'),
                             self.media_path('audio-lab-bg-16-9.png'))

        scene.add_widget(
            ActiveImage(self.media_path('tab.png'),
                        hover=self.media_path('tab-hover.png'),
                        down=self.media_path('tab-down.png')),
            Placement(0.6555, 0.52),
            Placement(0.5485, 0.5935),
            [self._tab_clicked, scene],
            key=Gdk.KEY_Tab
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('judoka.png')),
            Placement(0.95, 0.9),
            Placement(0.95, 0.9)
        )

        copy = 'Press the TAB key to play a song!'
        scene.add_widget(
            SpeechBubble(text=copy, source=SpeechBubble.BOTTOM,
                         source_align=0.8, scale=scene.scale_factor),
            Placement(0.95, 0.35),
            Placement(0.95, 0.45)
        )

        scene.schedule(40, self._show_hint, scene)

        return scene

    def _show_hint(self, scene):
        if not self._troubleshooting_open:
            scene.add_arrow(
                'right',
                Placement(0.4, 0.52),
                Placement(0.43, 0.5935),
                name='hint'
            )

    def _show_console(self, scene):
        if self._console_on:
            return
        self._console_on = True

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('console.png')),
            Placement(0.5, 1.0),
            Placement(0.5, 1.0),
            name='console-bg'
        )

        scene.add_widget(
            ConsoleScreen(self, scene, self._ctl.next_stage, self.help_jack),
            Placement(0.5155, 0.918),
            Placement(0.5155, 0.918),
            name='console-screen'
        )

    def _hide_console(self, scene):
        if not self._console_on:
            return

        scene.remove_widget('console-bg')
        scene.remove_widget('console-screen')
        self._console_on = False

    def _a_clicked(self, scene):
        play_sound('/usr/share/kano-media/sounds/kano_error.wav', True)
        self._show_console(scene)

    def _tab_clicked(self, scene):
        play_sound('/usr/share/kano-media/sounds/kano_test_sound.wav',
                   True)
        self._show_console(scene)

    def _d_clicked(self, scene):
        play_sound('/usr/share/kano-media/sounds/kano_init.wav', True)
        self._show_console(scene)

    def _setup_help_jack(self, scene):
        scene.add_widget(
            Notebook(
                self,
                self.media_path('jack.png'), 1.0, 0.5,
                'Plug in the blue cable',
                ['Check you\'ve plugged in the audio'],
                [{'label': 'NEXT',
                  'callback': self.help_leds,
                  'color': 'green'}]
            ),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0),
            modal=True,
            name='help-jack'
        )

    def _setup_help_leds(self, scene):
        scene.add_widget(
            Notebook(
                self,
                self.media_path('troubleshooting-sound.png'), 0.5, 0.3,
                'Can you see the blue light?',
                ['If the power plugs are connected correctly,',
                 'you should see a blue light.'],
                [{'label': 'YES', 'callback': self.remove_overlays, 'color': 'green'},
                 {'label': 'NO', 'callback': self.help_power, 'color': 'red'}]
            ),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0),
            modal=True,
            name='help-leds'
        )

    def _setup_help_power(self, scene):
        buttons = [{
            'label': 'TRY AGAIN',
            'callback': self.remove_overlays,
            'color': 'green'},
            {'label': 'SKIP',
            'callback':  self._ctl.next_stage,
            'color': 'grey'}
        ]
        if hdmi_supported:
            buttons.insert(1, {
                'label': 'USE TV SPEAKERS',
                'callback': self._set_to_hdmi,
                'color': 'blue'
            })

        print "buttons = {}".format(buttons)

        scene.add_widget(
            Notebook(
                self,
                self.media_path('power.png'), 0.8, 0.5,
                'No light? Check the GPIO',
                ['The cable has to be connected to these',
                 'pins exactly.'],
                buttons
            ),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0),
            modal=True,
            name='help-power'
        )

    def _set_to_hdmi(self):
        # Need sudo permissions to do this.
        run_cmd('sudo kano-init-flow-system-tool enable-tv-speakers')
        self._ctl.next_stage()


class ConsoleScreen(Gtk.EventBox):
    def __init__(self, stage, scene, yes_cb, no_cb):
        super(ConsoleScreen, self).__init__()

        self.set_size_request(368*scene.scale_factor, 179*scene.scale_factor)
        add_class(self, 'console-screen')

        if scene.scale_factor > 0.8:
            add_class(self, 'font-large')
        else:
            add_class(self, 'font-small')

        vbox = Gtk.VBox(False, 0)
        vbox.set_halign(Gtk.Align.CENTER)

        question = Gtk.Label('Can you hear a sound?')
        question.set_line_wrap(True)
        question.set_justify(Gtk.Justification.CENTER)
        question.set_valign(Gtk.Align.CENTER)
        add_class(question, 'console-screen-question')

        vbox.pack_start(question, True, False, 0)

        hbox = Gtk.HBox(False, 20)
        hbox.set_halign(Gtk.Align.CENTER)
        hbox.set_valign(Gtk.Align.CENTER)

        yes = KanoButton('YES')
        yes.connect('clicked', cb_wrapper, yes_cb)

        no = KanoButton('NO', color='red')
        no.connect('clicked', cb_wrapper, no_cb)

        hbox.pack_start(yes, False, False, 0)
        hbox.pack_start(no, False, False, 0)

        vbox.pack_start(hbox, True, False, 0)
        self.add(vbox)


class Notebook(Gtk.Overlay):
    def __init__(self, stage, image_path, image_scale, image_align,
                 title, copy, buttons):
        super(Notebook, self).__init__()

        self.add(Gtk.Image.new_from_file(stage.media_path('lonely-notebook.png')))

        fixed = Gtk.Fixed()
        self.add_overlay(fixed)

        self._eb = Gtk.EventBox()
        add_class(self._eb, 'notebook-content-area')
        self._eb.set_size_request(415, 460)

        fixed.put(self._eb, 20, 70)

        vbox = Gtk.VBox(False, 0)
        vbox.set_vexpand(True)
        vbox.set_hexpand(True)
        vbox.set_margin_left(10)
        vbox.set_margin_right(10)

        img = scale_image(Gtk.Image.new_from_file(image_path), image_scale)
        img_align = Gtk.Alignment.new(image_align, 0.5, 0, 0)
        img_align.add(img)
        img_align.set_vexpand(True)
        img_align.set_hexpand(True)
        vbox.pack_start(img_align, False, False, 0)

        heading = Gtk.Label(title)
        add_class(heading, 'notebook-heading')

        copy_widgets = []
        for line in copy:
            l = Gtk.Label(line)
            l.set_line_wrap(False)
            l.set_justify(Gtk.Justification.CENTER)
            add_class(l, 'notebook-text')
            l.set_halign(Gtk.Align.CENTER)
            copy_widgets.append(l)

        # Pack heading
        vbox.pack_start(heading, False, False, 0)
        heading.set_margin_top(15)
        heading.set_margin_bottom(15)

        for w in copy_widgets:
            vbox.pack_start(w, False, False, 3)

        hbox = Gtk.HBox(False, 10)
        hbox.set_margin_top(15)
        hbox.set_halign(Gtk.Align.CENTER)
        for b in buttons:
            button = KanoButton(b['label'], color=b['color'])
            button.connect('clicked', cb_wrapper, b['callback'])
            hbox.pack_start(button, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        self._eb.add(vbox)
