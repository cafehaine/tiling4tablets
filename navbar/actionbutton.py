from time import time
from typing import Callable, List, Union

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from .action import try_get_action

LONG_PRESS_TIME = 0.8

ConfigAction = Union[str, List]

class ActionButton(Gtk.Button):
    def __init__(self, icon: str, press: ConfigAction, long_press: ConfigAction):
        super().__init__(label=icon)
        self.press = press
        self.long_press = long_press
        self.button_down = False
        self.button_down_timestamp = None
        self.connect('button-press-event', self.press_event)
        self.connect('button-release-event', self.release_event)
        self.connect('leave-notify-event', self.leave_event)

    def press_event(self, button: 'ActionButton', event: Gdk.Event):
        """ On button press, if button is 1, mark time stamp. """
        if event.get_button()[1] == 1:
            self.button_down = True
            self.button_down_timestamp = time()
            #TODO run callback in the future with asyncio to call
            # call_long_press after LONG_PRESS_TIME even if click was not
            # released
        else:
            self.button_down = False

    def release_event(self, button: 'ActionButton', event: Gdk.Event):
        """ On button release, call press or long_press if appropriate. """
        if event.get_button()[1] == 1 and self.button_down:
            if time() - self.button_down_timestamp >= LONG_PRESS_TIME:
                self.call_long_press()
            else:
                self.call_press()
        self.button_down = False

    def leave_event(self, button: 'ActionButton', event: Gdk.Event):
        """ On cursor leave, stop considering button is down. """
        self.button_down = False

    def call_press(self) -> None:
        """ Execute the press action. """
        if isinstance(self.press, str):
            func = try_get_action(self.press)
            func()
        elif isinstance(self.press, list):
            func = try_get_action(self.press[0])
            func(*self.press[1:])

    def call_long_press(self) -> None:
        """ Execute the long_press action. """
        if isinstance(self.press, str):
            func = try_get_action(self.long_press)
            func()
        elif isinstance(self.press, list):
            func = try_get_action(self.long_press[0])
            func(*self.long_press[1:])
