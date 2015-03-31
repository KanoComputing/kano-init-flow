# faux_panel.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# fake lxpanel

from gi.repository import Gtk


class FauxPanel(Gtk.Box):
        # hthing
        # K menu image
        # expander
        # settings image
        # wifi image
        # speaker image
        # clock (label?)
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        # FIXME store paths properly
        kbutton = Gtk.Image.new_from_file("/usr/share/kano-desktop/images/startmenu.png")

        settings_button = Gtk.Image.new_from_file("/usr/share/kano-settings/settings-widget.png")
        wifi_button = Gtk.Image.new_from_file("/usr/share/kano-settings/icon/widget-wifi.png")

        blank = Gtk.Invisible()

        # FIXME speaker image 
        speaker_button = Gtk.Image.new_from_file("/usr/share/kano-settings/icon/widget-wifi.png")

        self.pack_start(kbutton, False, False, 0)
        self.pack_start(blank, True, False, 0)
        self.pack_start(settings_button, False, False, 0)
        self.pack_start(wifi_button, False, False, 0)
        self.pack_start(speaker_button, False, False, 0)

        # Fixme: get time working
        clock = Gtk.Label(" 88:88 ")

        self.pack_start(clock, False, False, 0)
