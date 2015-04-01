# faux_panel.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# fake lxpanel

from gi.repository import Gtk


class FauxPanel(Gtk.EventBox):
        # hthing
        # K menu image
        # expander
        # settings image
        # wifi image
        # speaker image
        # clock (label?)
    def __init__(self):
        Gtk.EventBox.__init__(self)        

        self._box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self._box)

        self.set_halign(Gtk.Align.FILL)
        self.set_valign(Gtk.Align.END)
        self.get_style_context().add_class("faux_panel")

        # FIXME store paths properly
        kbutton = Gtk.Image.new_from_file("/usr/share/kano-desktop/images/startmenu.png")

        settings_button = Gtk.Image.new_from_file("/usr/share/kano-settings/settings-widget.png")
        wifi_button = Gtk.Image.new_from_file("/usr/share/kano-settings/icon/widget-wifi.png")

        blank = Gtk.Invisible()

        speaker_button = Gtk.Image.new_from_file("/usr/share/icons/Kano/44x44/status/audio-volume-high.png")

        self._box.pack_start(kbutton, False, False, 0)
        self._box.pack_start(blank, True, False, 0)
        self._box.pack_start(wifi_button, False, False, 0)
        self._box.pack_start(settings_button, False, False, 0)
        self._box.pack_start(speaker_button, False, False, 0)

        # Fixme: get time working
        clock = Gtk.Label(" 88:88 ")

        self._box.pack_start(clock, False, False, 0)
