# The Kano World overview
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
from gi.repository import Gtk, GdkPixbuf
from kano.gtk3.buttons import KanoButton
from kano.gtk3.apply_styles import apply_styling_to_screen


class MainWindow(Gtk.Window):

    # Dimensions of the window: width = 1000, height = 677.4

    def __init__(self):
        super(MainWindow, self).__init__()
        self.set_decorated(False)
        self.set_size_request(500, 400)
        self.connect("delete-event", Gtk.main_quit)
        self.slide1()
        apply_styling_to_screen(self.css_path("style.css"))

    def slide1(self):
        fixed = Gtk.Fixed()

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.media_path("apps-slide.png"),
            1000,
            678
        )
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        title1 = Gtk.Label(_("Get Started"))
        title1.get_style_context().add_class("title")
        title2 = Gtk.Label(_("Apps"))
        title2.get_style_context().add_class("title")
        desc = Gtk.Label(
            _("Create and play with\n" \
              "Kano's Apps to make and save your\n" \
              "own code masterpieces, from games\n" \
              "and minecraft world, to art and music pieces...")
        )
        desc.get_style_context().add_class("description")

        next_button = KanoButton(_("NEXT"))
        next_button.connect("clicked", self.slide2_wrapper)

        fixed.put(image, 0, 0)
        fixed.put(title1, 460, 40)
        fixed.put(title2, 60, 400)
        fixed.put(desc, 60, 450)
        fixed.put(next_button, 460, 580)

        self.add(fixed)

        self.show_all()

    def slide2(self):
        self.clear_window()
        fixed = Gtk.Fixed()

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.media_path("world-slide.png"),
            1000,
            678
        )
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        title = Gtk.Label(_("Kano World"))
        title.get_style_context().add_class("title")
        desc = Gtk.Label(
            _("Show off and share your creations to friends\n" \
              "family and other Kano users on Kano World.\n\n" \
              "Why not check it out now by clicking on the\n" \
              "icon to see what people have made today.")
        )
        desc.get_style_context().add_class("description")

        next_button = KanoButton(_("LET'S GO"))
        next_button.connect("clicked", Gtk.main_quit)

        fixed.put(image, 0, 0)
        fixed.put(title, 415, 370)
        fixed.put(desc, 310, 420)
        fixed.put(next_button, 440, 580)

        self.add(fixed)

        self.show_all()

    def slide2_wrapper(self, widget):
        self.slide2()

    def clear_window(self):
        for child in self.get_children():
            self.remove(child)

    def media_path(self, filename):
        '''
            :params filename: the name of the file
            :type filename: str
        '''
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(parent_dir, "media", filename)
        if not os.path.exists(path):
            raise OSError("Path {} doesn't exist".format(path))
        return path

    def css_path(self, filename):
        '''
            :params filename: the name of the file
            :type filename: str
        '''
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(parent_dir, "css", filename)
        if not os.path.exists(path):
            raise OSError("Path {} doesn't exist".format(path))
        return path
