#!/usr/bin/env python

# keyboard_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gtk, Gdk, GObject
GObject.threads_init()
import threading
from internet_screen import InternetScreen
from update_screen import UpdateScreen
from kano.network import is_internet
import kano_settings.keyboard.keyboard_layouts as keyboard_layouts
import kano_settings.keyboard.keyboard_config as keyboard_config
from kano.gtk3.heading import Heading
from kano.gtk3.buttons import KanoButton
from kano_settings.config_file import get_setting, set_setting


class KeyboardScreen(Gtk.Box):
    continents = ['Africa', 'America', 'Asia', 'Australia', 'Europe', 'Others']

    def __init__(self, _win):
        self.selected_layout = None
        self.selected_country = None
        self.selected_variant = None

        self.selected_continent_index = 1
        self.selected_country_index = 21
        self.selected_variant_index = 0
        self.selected_continent_hr = "America"
        self.selected_country_hr = "USA"
        self.selected_variant_hr = "generic"

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.win = _win
        self.win.add(self)

        # Heading
        self.heading = Heading("Keyboard", "Where do you live? So I can set your keyboard")
        self.heading.container.set_size_request(590, -1)

        heading_align = Gtk.Alignment()
        heading_align.add(self.heading.container)

        # Set padding around heading
        self.heading_align = Gtk.Alignment(yscale=0, yalign=0.5)

        # Button
        self.kano_button = KanoButton("APPLY CHANGES")
        self.kano_button.set_sensitive(False)  # Make sure continue button is enabled
        self.kano_button.connect("button_release_event", self.apply_changes)
        button_box = Gtk.ButtonBox(spacing=10)
        button_box.set_layout(Gtk.ButtonBoxStyle.SPREAD)
        button_box.add(self.kano_button)
        button_box.set_margin_bottom(30)

        # Create Continents Combo box
        self.continents_combo = Gtk.ComboBoxText.new()
        for c in self.continents:
            self.continents_combo.append_text(c)
        self.continents_combo.connect("changed", self.on_continent_changed)

        # Create Countries Combo box
        self.countries_combo = Gtk.ComboBoxText.new()
        self.countries_combo.connect("changed", self.on_country_changed)
        self.countries_combo.props.valign = Gtk.Align.CENTER

        # Create Advance mode checkbox
        self.advance_button = Gtk.CheckButton("Advanced options")
        self.advance_button.set_can_focus(False)
        self.advance_button.props.valign = Gtk.Align.CENTER
        self.advance_button.connect("clicked", self.on_advance_mode)
        self.advance_button.set_active(False)

        # Create Variants Combo box
        self.variants_combo = Gtk.ComboBoxText.new()
        self.variants_combo.connect("changed", self.on_variants_changed)
        self.variants_combo.props.valign = Gtk.Align.CENTER

        # Set up default values in dropdown lists
        self.set_defaults("continent")
        self.set_defaults("country")
        self.set_defaults("variant")

        # Ceate various dropdown boxes so we can resize the dropdown lists appropriately
        # We create two boxes side by side, and then stack the country dropdow lists in one, and one by itself in the other

        #   dropdown_box_countries     dropdown_box_keys
        # |                        |                        |
        # |-------continents-------|   Advance option       |
        # |                        |                        |
        # |                        |                        |
        # |-------countries -------|--------variants--------|
        # |                        |                        |

        dropdown_box_countries = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        dropdown_box_countries.set_size_request(230, 30)
        dropdown_box_countries.props.valign = Gtk.Align.CENTER
        dropdown_box_keys = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        dropdown_box_keys.set_size_request(230, 30)
        dropdown_box_countries.pack_start(self.continents_combo, False, False, 0)
        dropdown_box_countries.pack_start(self.countries_combo, False, False, 0)
        dropdown_box_keys.pack_start(self.advance_button, False, False, 0)
        dropdown_box_keys.pack_start(self.variants_combo, False, False, 0)
        dropdown_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        dropdown_container.pack_start(dropdown_box_countries, False, False, 0)
        dropdown_container.pack_start(dropdown_box_keys, False, False, 0)

        valign = Gtk.Alignment(xalign=0.5, yalign=0, xscale=0, yscale=0)
        valign.set_padding(15, 30, 0, 0)
        valign.add(dropdown_container)

        self.pack_start(heading_align, False, False, 0)
        self.pack_start(valign, False, False, 0)
        self.pack_start(button_box, False, False, 0)

        # show all elements except the advanced mode
        self.refresh_window()

    def go_to_next_screen(self):
        self.win.clear_win()
        # Check first for internet
        if not is_internet():
            InternetScreen(self.win)
        else:
            UpdateScreen(self.win)

    def refresh_window(self):
        self.win.show_all()
        self.variants_combo.hide()

    def apply_changes(self, widget, event):

        # Check for changes from default
        if not (self.selected_country.lower() == "us" and self.selected_variant == "generic"):

            # This is a callback called by the main loop, so it's safe to
            # manipulate GTK objects:
            watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
            self.win.get_window().set_cursor(watch_cursor)
            self.kano_button.set_sensitive(False)

            def lengthy_process():
                keyboard_config.set_keyboard(self.selected_country, self.selected_variant)

                def done():
                    self.win.get_window().set_cursor(None)
                    self.kano_button.set_sensitive(True)
                    self.go_to_next_screen()

                GObject.idle_add(done)

            thread = threading.Thread(target=lengthy_process)
            thread.start()

        # keyboard does not need updating
        else:
            self.go_to_next_screen()

    def update_config(self):

        # Add new configurations to config file.
        set_setting("Keyboard-continent-index", self.selected_continent_index)
        set_setting("Keyboard-country-index", self.selected_country_index)
        set_setting("Keyboard-variant-index", self.selected_variant_index)
        set_setting("Keyboard-continent-human", self.selected_continent_hr)
        set_setting("Keyboard-country-human", self.selected_country_hr)
        set_setting("Keyboard-variant-human", self.selected_variant_hr)

    # setting = "variant", "continent" or "country"
    def set_defaults(self, setting):

        # Set the default info on the dropdown lists
        # "Keyboard-continent":continents_combo, "Keyboard-country", "Keyboard-variant"]:

        active_item = get_setting("Keyboard-" + setting + "-index")

        if setting == "continent":
            self.continents_combo.set_active(int(active_item))
        elif setting == "country":
            self.countries_combo.set_active(int(active_item))
        elif setting == "variant":
            self.variants_combo.set_active(int(active_item))
        else:
            return

    def set_variants_to_generic(self):
        self.variants_combo.set_active(0)

    def on_continent_changed(self, combo):

        continent = self.selected_continent_hr
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            continent = model[tree_iter][0]

        self.selected_continent_hr = str(continent)
        self.selected_continent_index = str(combo.get_active())

        self.kano_button.set_sensitive(False)

        self.fill_countries_combo(self.selected_continent_hr)

    def on_country_changed(self, combo):

        country = None
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            country = model[tree_iter][0]

        if not country:
            return

        # Remove entries from variants combo box
        self.variants_combo.remove_all()
        self.selected_country_hr = str(country)
        self.selected_country_index = combo.get_active()

        # Refresh variants combo box
        self.selected_country = keyboard_config.find_country_code(country, self.selected_layout)
        variants = keyboard_config.find_keyboard_variants(self.selected_country)
        self.variants_combo.append_text("generic")
        if variants is not None:
            for v in variants:
                self.variants_combo.append_text(v[0])

        self.set_variants_to_generic()

    def on_variants_changed(self, combo):
        global selected_variant_index

        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            variant = model[tree_iter][0]
            self.kano_button.set_sensitive(True)
            if variant == "generic":
                self.selected_variant = self.selected_variant_hr = str(variant)
                self.selected_variant_index = 0
                return
            # Select the variant code
            variants = keyboard_config.find_keyboard_variants(self.selected_country)
            if variants is not None:
                for v in variants:
                    if v[0] == variant:
                        self.selected_variant = v[1]
                        self.selected_variant_index = combo.get_active()
                        self.selected_variant_hr = str(variant)

    def on_advance_mode(self, widget):

        if int(self.advance_button.get_active()):
            self.variants_combo.show()
        else:
            self.variants_combo.hide()

    def work_finished_cb(self):
        # Finished updating keyboard
        pass

    def fill_countries_combo(self, continent):

        continent = continent.lower()

        if continent == 'africa':
            self.selected_layout = keyboard_layouts.layouts_africa
        elif continent == 'america':
            self.selected_layout = keyboard_layouts.layouts_america
        elif continent == 'asia':
            self.selected_layout = keyboard_layouts.layouts_asia
        elif continent == 'australia':
            self.selected_layout = keyboard_layouts.layouts_australia
        elif continent == 'europe':
            self.selected_layout = keyboard_layouts.layouts_europe
        elif continent == 'others':
            self.selected_layout = keyboard_layouts.layouts_others

        self.selected_continent_hr = continent

        # Remove entries from countries and variants combo box
        self.countries_combo.remove_all()
        self.variants_combo.remove_all()

        sorted_countries = sorted(self.selected_layout)

        # Refresh countries combo box
        for country in sorted_countries:
            self.countries_combo.append_text(country)
