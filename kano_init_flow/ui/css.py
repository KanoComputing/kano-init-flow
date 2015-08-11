# Get media and CSS directories for the current stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk


def get_gtk_priority(priority):
    '''
        :param priority: The level of the CSS and whether it will be
                         overwritten
        :type priority: int
    '''

    priority_list = [
        Gtk.STYLE_PROVIDER_PRIORITY_FALLBACK,
        Gtk.STYLE_PROVIDER_PRIORITY_THEME,
        Gtk.STYLE_PROVIDER_PRIORITY_SETTINGS,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        Gtk.STYLE_PROVIDER_PRIORITY_USER
    ]

    return priority_list[priority]


def apply_styling_to_screen(css_file, priority=3):
    '''
        :param css_file: The full filepath of the CSS file
        :type css_file: str
        :param priority: How easily the CSS can be overwritten
        :type priority: int
    '''

    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(css_file)

    screen = Gdk.Screen.get_default()
    style_context = Gtk.StyleContext()

    gtk_priority = get_gtk_priority(priority)

    style_context.add_provider_for_screen(
        screen,
        css_provider,
        gtk_priority
    )


def apply_styling_to_widget(widget, path, priority=3):
    '''
        :param widget: The widget we want to apply the styling to.
        :type widget: Gtk.Widget

        :param css_file: The full filepath of the CSS file.
        :type css_file: str

        :param priority: How easily the CSS can be overwritten.
        :type priority: int
    '''

    provider = Gtk.CssProvider()
    provider.load_from_path(path)
    style_context = widget.get_style_context()
    gtk_priority = get_gtk_priority(priority)
    style_context.add_provider(provider, gtk_priority)
