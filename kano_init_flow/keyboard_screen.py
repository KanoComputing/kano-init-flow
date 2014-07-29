#!/usr/bin/env python

# keyboard_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import sys
from gi.repository import Gtk, GObject
GObject.threads_init()
import threading
import kano_settings.keyboard.keyboard_layouts as keyboard_layouts
import kano_settings.keyboard.keyboard_config as keyboard_config
from kano.gtk3.heading import Heading
from kano.gtk3.buttons import KanoButton
import kano_settings.components.fixed_size_box as fixed_size_box
from kano_settings.config_file import get_setting, set_setting

selected_layout = None
selected_country = None
selected_variant = None

selected_continent_index = 1
selected_country_index = 21
selected_variant_index = 0
selected_continent_hr = "America"
selected_country_hr = "USA"
selected_variant_hr = "generic"

variants_combo = None
countries_combo = None
continents_combo = None

continents = ['Africa', 'America', 'Asia', 'Australia', 'Europe', 'Others']

DROPDOWN_CONTAINER_HEIGHT = 118


class WorkerThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback

    def run(self):
        # Apply the keyboard changes
        keyboard_config.set_keyboard(selected_country, selected_variant)

        # The callback runs a GUI task, so wrap it!
        GObject.idle_add(self.callback)


class KeyboardScreen(Gtk.Box):

    def __init__(self, _win):
        global continents_combo, variants_combo, countries_combo

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.win = _win
        self.win.add(self)

        # Contains all the settings
        settings = fixed_size_box.Fixed()

        # Heading
        self.heading = Heading("Keyboard", "Where do you live? So I can set your keyboard")
        self.heading.container.set_size_request(590, -1)

        heading_align = Gtk.Alignment()
        heading_align.set_padding(60, 0, 0, 0)
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
        continents_combo = Gtk.ComboBoxText.new()
        for c in continents:
            continents_combo.append_text(c)
        continents_combo.connect("changed", self.on_continent_changed)

        # Create Countries Combo box
        countries_combo = Gtk.ComboBoxText.new()
        countries_combo.connect("changed", self.on_country_changed)
        countries_combo.props.valign = Gtk.Align.CENTER

        # Create Advance mode checkbox
        self.advance_button = Gtk.CheckButton("Advanced options")
        self.advance_button.set_can_focus(False)
        self.advance_button.props.valign = Gtk.Align.CENTER
        self.advance_button.connect("clicked", self.on_advance_mode)
        self.advance_button.set_active(False)

        # Create Variants Combo box
        variants_combo = Gtk.ComboBoxText.new()
        variants_combo.connect("changed", self.on_variants_changed)
        variants_combo.props.valign = Gtk.Align.CENTER

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
        dropdown_box_countries.pack_start(continents_combo, False, False, 0)
        dropdown_box_countries.pack_start(countries_combo, False, False, 0)
        dropdown_box_keys.pack_start(self.advance_button, False, False, 0)
        dropdown_box_keys.pack_start(variants_combo, False, False, 0)
        dropdown_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        dropdown_container.pack_start(dropdown_box_countries, False, False, 0)
        dropdown_container.pack_start(dropdown_box_keys, False, False, 0)

        valign = Gtk.Alignment(xalign=0.5, yalign=0, xscale=0, yscale=0)
        padding_above = (settings.height - DROPDOWN_CONTAINER_HEIGHT) / 2
        valign.set_padding(padding_above, 0, 0, 0)
        valign.add(dropdown_container)
        settings.box.pack_start(valign, False, False, 0)

        self.pack_start(heading_align, False, False, 0)
        self.pack_start(settings.box, False, False, 0)
        self.pack_start(button_box, False, False, 0)

        # show all elements except the advanced mode
        self.refresh_window()

    def refresh_window(self):
        global variants_combo
        self.win.show_all()
        variants_combo.hide()

    def apply_changes(self, widget, event):
        global variants_combo

        # Check for changes
        if selected_country != "USA" and selected_variant != "generic":
            # Apply changes
            thread = WorkerThread(self.work_finished_cb)
            thread.start()

            # Save the changes in the config
            self.update_config()

        # Exit
        sys.exit(0)

    def update_config(self):

        # Add new configurations to config file.
        set_setting("Keyboard-continent-index", selected_continent_index)
        set_setting("Keyboard-country-index", selected_country_index)
        set_setting("Keyboard-variant-index", selected_variant_index)
        set_setting("Keyboard-continent-human", selected_continent_hr)
        set_setting("Keyboard-country-human", selected_country_hr)
        set_setting("Keyboard-variant-human", selected_variant_hr)

    # setting = "variant", "continent" or "country"
    def set_defaults(self, setting):
        global continents_combo, countries_combo, variants_combo

        # Set the default info on the dropdown lists
        # "Keyboard-continent":continents_combo, "Keyboard-country", "Keyboard-variant"]:

        active_item = get_setting("Keyboard-" + setting + "-index")

        if setting == "continent":
            continents_combo.set_active(int(active_item))
        elif setting == "country":
            countries_combo.set_active(int(active_item))
        elif setting == "variant":
            variants_combo.set_active(int(active_item))
        else:
            return

    def set_variants_to_generic(self):
        global variants_combo
        variants_combo.set_active(0)

    def on_continent_changed(self, combo):
        global selected_continent_hr, selected_continent_index

        continent = selected_continent_hr
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            continent = model[tree_iter][0]

        selected_continent_hr = str(continent)
        selected_continent_index = str(combo.get_active())

        self.kano_button.set_sensitive(False)

        self.fill_countries_combo(selected_continent_hr)

    def on_country_changed(self, combo):
        global selected_country, selected_country_index, selected_country_hr, selected_layout, variants_combo

        country = None
        tree_iter = combo.get_active_iter()

        if tree_iter is not None:
            model = combo.get_model()
            country = model[tree_iter][0]

        if not country:
            return

        # Remove entries from variants combo box
        variants_combo.remove_all()
        selected_country_hr = str(country)
        selected_country_index = combo.get_active()

        # Refresh variants combo box
        selected_country = keyboard_config.find_country_code(country, selected_layout)
        variants = keyboard_config.find_keyboard_variants(selected_country)
        variants_combo.append_text("generic")
        if variants is not None:
            for v in variants:
                variants_combo.append_text(v[0])

        self.set_variants_to_generic()

    def on_variants_changed(self, combo):
        global selected_variant, selected_variant_hr, selected_variant_index

        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            variant = model[tree_iter][0]
            self.kano_button.set_sensitive(True)
            if variant == "generic":
                selected_variant = selected_variant_hr = str(variant)
                selected_variant_index = 0
                return
            # Select the variant code
            variants = keyboard_config.find_keyboard_variants(selected_country)
            if variants is not None:
                for v in variants:
                    if v[0] == variant:
                        selected_variant = v[1]
                        selected_variant_index = combo.get_active()
                        selected_variant_hr = str(variant)

    def on_advance_mode(self, widget):
        global variants_combo

        if int(self.advance_button.get_active()):
            variants_combo.show()
        else:
            variants_combo.hide()

    def work_finished_cb(self):
        # Finished updating keyboard
        pass

    def fill_countries_combo(self, continent):
        global countries_combo, variants_combo, selected_layout, selected_continent_hr

        continent = continent.lower()

        if continent == 'africa':
            selected_layout = keyboard_layouts.layouts_africa
        elif continent == 'america':
            selected_layout = keyboard_layouts.layouts_america
        elif continent == 'asia':
            selected_layout = keyboard_layouts.layouts_asia
        elif continent == 'australia':
            selected_layout = keyboard_layouts.layouts_australia
        elif continent == 'europe':
            selected_layout = keyboard_layouts.layouts_europe
        elif continent == 'others':
            selected_layout = keyboard_layouts.layouts_others

        selected_continent_hr = continent

        # Remove entries from countries and variants combo box
        countries_combo.remove_all()
        variants_combo.remove_all()

        sorted_countries = sorted(selected_layout)

        # Refresh countries combo box
        for country in sorted_countries:
            countries_combo.append_text(country)
