# The old-design overscan screen
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk

from kano.gtk3.buttons import KanoButton
from kano.utils import is_monitor, run_cmd
from kano_settings.system.display import get_overscan_status, \
    write_overscan_values, set_overscan_status, launch_pipe
from kano_profile.tracker import track_action


from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, ActiveImage
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.ui.utils import cb_wrapper


class OverscanOld(Stage):
    """
        The overscan setting window
    """

    id = 'overscan-old'
    _root = __file__

    def __init__(self, ctl):
        super(OverscanOld, self).__init__(ctl)

        self._overscan_ctl = OverscanControl()

        apply_styling_to_screen(self.css_path('overscan-old.css'))

    def first_scene(self):
        if is_monitor():
            self._ctl.next_stage()
            return

        track_action('init-flow-overscan-needed')
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1)

    def save_and_exit(self):
        self._overscan_ctl.reset() # TODO remove
        self._overscan_ctl.save_changes()
        self._ctl.next_stage()

    def _setup_first_scene(self):
        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        self._scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('arrow-up.png')),
            Placement(0.5, 0.0, 1.0),
            Placement(0.5, 0.0, 1.0)
        )

        self._scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('arrow-down.png')),
            Placement(0.5, 1.0, 1.0),
            Placement(0.5, 1.0, 1.0)
        )

        self._scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('arrow-left.png')),
            Placement(0.0, 0.5, 1.0),
            Placement(0.0, 0.5, 1.0)
        )

        self._scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('arrow-right.png')),
            Placement(1.0, 0.5, 1.0),
            Placement(1.0, 0.5, 1.0)
        )

        self._scene.add_widget(
            Window1(self, self._ctl.next_stage, self.next_window),
            Placement(0.5, 0.5, 1.0),
            Placement(0.5, 0.5, 1.0),
            modal=False,
            name='window1'
        )

        return scene

    def next_window(self):
        self._scene.remove_widget('window1')
        self._scene.add_widget(
            Window2(self, self._overscan_ctl, self._ctl.next_stage),
            Placement(0.5, 0.5, 0.0),
            Placement(0.5, 0.5, 0.0),
            modal=False,
            name='window2'
        )

        self._scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('blank.png')),
            Placement(0.5, 0.0, 0),
            Placement(0.50, 0.0, 0),
            self._overscan_ctl.zoom_out,
            key=Gdk.KEY_Up
        )
        self._scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('blank.png')),
            Placement(0.5, 1.0, 0),
            Placement(0.50, 1.0, 0),
            self._overscan_ctl.zoom_in,
            key=Gdk.KEY_Down
        )


class Window1(Gtk.EventBox):
    def __init__(self, stage, yes_cb, no_cb):
        super(Window1, self).__init__()

        add_class(self, 'overscan-window')

        head_img = Gtk.Image.new_from_file(stage.media_path('hint1.png'))
        box = Gtk.VBox()
        self.add(box)

        box.pack_start(head_img, False, False, 0)

        heading = Gtk.Label('Are the lines touching the edges of your screen?')
        heading.set_margin_top(25)
        heading.set_margin_bottom(25)
        add_class(heading, 'notebook-heading')
        box.pack_start(heading, False, False, 0)

        heading = Gtk.Label('Make sure you can see all four lines')
        heading.set_margin_bottom(35)
        add_class(heading, 'notebook-text')
        box.pack_start(heading, False, False, 0)

        buttons = Gtk.HBox(halign=Gtk.Align.CENTER)
        buttons.set_margin_bottom(25)
        yes = KanoButton('YES', color='green')
        yes.connect('clicked', cb_wrapper, yes_cb)
        buttons.pack_start(yes, False, False, 0)
        no = KanoButton('NO', color='red')
        no.connect('clicked', cb_wrapper, no_cb)
        buttons.pack_start(no, False, False, 10)

        box.pack_start(buttons, False, False, 0)


class Window2(Gtk.EventBox):
    def __init__(self, stage, overscan_ctl, next_cb):
        super(Window2, self).__init__()

        add_class(self, 'overscan-window')

        head_img = Gtk.Image.new_from_file(stage.media_path('hint2.png'))
        box = Gtk.VBox()
        self.add(box)

        box.pack_start(head_img, False, False, 0)

        heading = Gtk.Label('Use UP and DOWN keys')
        heading.set_margin_top(25)
        heading.set_margin_bottom(25)
        add_class(heading, 'notebook-heading')
        box.pack_start(heading, False, False, 0)

        text1 = Gtk.Label('Stretch or shrink your screen, until the white lines')
        text1.set_margin_bottom(5)
        add_class(text1, 'notebook-text')
        box.pack_start(text1, False, False, 0)

        text2 = Gtk.Label('are lined up with the edges')
        text2.set_margin_bottom(25)
        add_class(text2, 'notebook-text')
        box.pack_start(text2, False, False, 0)

        buttons = Gtk.HBox(halign=Gtk.Align.CENTER)
        buttons.set_margin_bottom(25)
        done = KanoButton('DONE', color='green')
        buttons.pack_start(done, False, False, 0)
        done.connect('clicked', cb_wrapper, next_cb)

        box.pack_start(buttons, False, False, 0)


class OverscanControl(object):
    def __init__(self):
        # launch_pipe()
        # The command below initialises the overscan pipe as root
        # TODO: This would be nice to refactor.
        run_cmd('sudo kano-init-flow-system-tool init-overscan-pipe')

        self._enabled = True
        self._step = 10
        self._original = get_overscan_status()
        self._current = get_overscan_status()

    def zoom_in(self):
        if self._enabled:
            if max(self._current.values()) < 250:
                self._change_overscan(self._step)

    def zoom_out(self):
        if self._enabled:
            self._change_overscan(-self._step)

    def reset(self, *_):
        """ Restore overscan if any changes were made """

        if self._original != self._current:
            self._current = self._original
            set_overscan_status(self._original)

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def save_changes(self):
        if self._original != self._current:
            write_overscan_values(self._current)

    def _change_overscan(self, change):
        """
        Increment (or decrement) the overscan setting
        :param change: Number to add to the overscan setting
        """

        for side, value in self._current.iteritems():
            # Do allow negative values
            self._current[side] = max(value + change, 0)

        set_overscan_status(self._current)
