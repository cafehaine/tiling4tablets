import asyncio
from time import time
from typing import Callable, List, Union

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Gdk, GdkPixbuf

from .action import try_get_action

LONG_PRESS_TIME = 0.8
ICON_SIZE = 32

ConfigAction = Union[str, List]

class ActionButton(Gtk.Button):
    def __init__(self, icon: str, press: ConfigAction, long_press: ConfigAction):
        super().__init__()
        self.icon = icon
        self.load_icon()
        self.press = press
        self.long_press = long_press
        self.button_down = False
        self.button_down_timestamp = None
        self.button_timer_handle = None
        self.connect('button-press-event', self.press_event)
        self.connect('button-release-event', self.release_event)
        self.connect('leave-notify-event', self.leave_event)

    def load_icon(self):
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("navbar/themes/default/icons/"+self.icon+".svg", ICON_SIZE, ICON_SIZE)
        except GLib.Error:
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("navbar/themes/default/icons/default.svg", ICON_SIZE, ICON_SIZE)
            except GLibError:
                print("COULD NOT LOAD ICON OR DEFAULT ICON")
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.set_image(image)

    def press_event(self, button: 'ActionButton', event: Gdk.Event):
        """ On button press, if button is 1, mark time stamp. """
        if event.get_button()[1] == 1:
            self.button_down = True
            self.button_down_timestamp = time()

            event_loop = asyncio.get_event_loop()
            self.button_timer_handle = event_loop.call_later(LONG_PRESS_TIME, self.timer_event)
        else:
            self.button_down = False

    def release_event(self, button: 'ActionButton', event: Gdk.Event):
        """ On button release, call press or long_press if appropriate. """
        if self.button_timer_handle is not None:
            self.button_timer_handle.cancel()

        if event.get_button()[1] == 1 and self.button_down:
            if time() - self.button_down_timestamp >= LONG_PRESS_TIME:
                self.call_long_press()
            else:
                self.call_press()
        self.button_down = False

    def leave_event(self, button: 'ActionButton', event: Gdk.Event):
        """ On cursor leave, stop considering button is down. """
        self.button_down = False

    def timer_event(self):
        """ Call long_press and reset button_down after timer is ellapsed. """
        self.call_long_press()
        self.button_down = False

    def call_press(self) -> None:
        """ Execute the press action. """
        if isinstance(self.press, str):
            func = try_get_action(self.press)
            func()
        elif isinstance(self.press, list):
            func = try_get_action(self.press[0])
            func(*self.press[1:])
        print(func.__name__)

    def call_long_press(self) -> None:
        """ Execute the long_press action. """
        if isinstance(self.press, str):
            func = try_get_action(self.long_press)
            func()
        elif isinstance(self.press, list):
            func = try_get_action(self.long_press[0])
            func(*self.long_press[1:])
        print(func.__name__)
