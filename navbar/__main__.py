import asyncio

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, GtkLayerShell

from i3ipc.aio import Connection
from i3ipc import Event

from .navbar import NavBarWindow

window = NavBarWindow()
window.show_all()
window.connect("destroy", Gtk.main_quit)

async def gtk_main_loop():
    while True:
        await asyncio.sleep(0.1)
        while Gtk.events_pending():
            Gtk.main_iteration()

async def main():
    #TODO bind on OutputEvent to listen to screen rotation events.
    c = await Connection(auto_reconnect=True).connect()
    def on_window(self, e):
        print(e)
    c.on(Event.WINDOW, on_window)

    await c.main()

asyncio.get_event_loop().create_task(gtk_main_loop())
asyncio.get_event_loop().run_until_complete(main())
