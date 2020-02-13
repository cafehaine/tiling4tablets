import asyncio

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, GtkLayerShell

from i3ipc.aio import Connection
from i3ipc import Event

from .navbarwindow import NavBarWindow
from . import set_connection

window = NavBarWindow()
window.show_all()
window.connect("destroy", Gtk.main_quit)

async def gtk_main_loop():
    """ Asyncronous Gtk event loop. """
    while True:
        await asyncio.sleep(0.02)
        while Gtk.events_pending():
            Gtk.main_iteration()

async def main():
    """ Set up the connection to i3/sway and wait for events. """
    c = await Connection(auto_reconnect=True).connect()
    set_connection(c)

    def on_output(self, e):
        #TODO At the moment, those events are not emitted by sway.
        # When https://github.com/swaywm/sway/pull/4020 is implemented and
        # merged, those events could be used to detect the orientation and move
        # the bar accordingly.
        print(e)

    c.on(Event.OUTPUT, on_output)

    await c.main()

asyncio.get_event_loop().create_task(gtk_main_loop())
asyncio.get_event_loop().run_until_complete(main())
