# Gui stuff
import pgi
pgi.require_version('Gtk', '3.0')
from pgi.repository import Gtk, Gdk

# XDG stuff to fetch the application list
from os.path import join
from glob import glob
from xdg import Menu, DesktopEntry
from subprocess import call

# String manipulation thingies
import unicodedata
import re

def remove_accents(input_str):
    """
    function by MiniQuark over at stackoverflow
    https://stackoverflow.com/a/517974/2279323
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def run_entry(entry):
    call(['exo-open',entry.path])

def fetch_application_list():
    application_directories = [join(p,'applications') for p in Menu.xdg_data_dirs]

    entries = []
    names = []

    for directory in application_directories:
        for f in glob(join(directory,"**/*.desktop"), recursive=True):
            entry = DesktopEntry.DesktopEntry(f)
            if not entry.getNoDisplay() and entry.getName() not in names:
                names.append(entry.getName())
                entry.path = f
                entries.append(entry)

    return sorted(entries, key=lambda e: remove_accents(e.getName().lower()))

class FlowBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="TouchLauncher")
        self.set_border_width(0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(6)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox.set_column_spacing(10)
        flowbox.set_row_spacing(10)
        flowbox.set_border_width(20)

        self.fill_flowbox(flowbox)

        scrolled.add(flowbox)

        self.add(scrolled)
        self.show_all()
        self.fullscreen()

    def fill_flowbox(self, flowbox):
        for app in fetch_application_list():
            icon = Gtk.Image.new_from_icon_name(app.getIcon(),6)
            icon.set_pixel_size(128)
            button = Gtk.Button(label=app.getName(), image=icon, image_position=Gtk.PositionType.TOP, always_show_image=True)
            button.app = app
            button.connect("clicked", lambda e:(run_entry(e.app), Gtk.main_quit()))
            flowbox.add(button)


win = FlowBoxWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
