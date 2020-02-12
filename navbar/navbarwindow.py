import asyncio

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, Gdk, GtkLayerShell

from yaml import safe_load

from .action import ACTIONS

class NavBarWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Navbar")
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.auto_exclusive_zone_enable(self)
        css_provider = Gtk.CssProvider()
        Gtk.CssProvider.load_from_path(css_provider, "navbar/test.css")

        #Gtk.StyleContext.add_provider(self.get_style_context(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=False, spacing=0)
        self.add(self.main_box)

        self.load_config()

        self.set_horizontal()

    def set_vertical(self):
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, 0)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, 1)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, 1)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, 1)

    def set_horizontal(self):
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, 1)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, 0)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, 1)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, 1)

    def on_toggle_click(self, button):
        if self.main_box.get_orientation() == Gtk.Orientation.VERTICAL:
            self.main_box.set_orientation(Gtk.Orientation.HORIZONTAL)
            self.set_horizontal()
        else:
            self.main_box.set_orientation(Gtk.Orientation.VERTICAL)
            self.set_vertical()

    def load_config(self):
        with open("navbar/config.yml") as data:
            print(safe_load(data))
