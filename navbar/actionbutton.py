from typing import Callable, List, Union

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .action import try_get_action

ConfigAction = Union[str, List]

class ActionButton(Gtk.Button):
    def __init__(self, icon: str, press: ConfigAction, long_press: ConfigAction):
        super().__init__(label=icon)
        self.press = press
        self.long_press = long_press
        self.connect('clicked', self.call_action)

    def call_action(self, button: Gtk.Button) -> None:
        #TODO call press or long_press depending on click duration
        self.call_press()

    def call_press(self) -> None:
        if isinstance(self.press, str):
            func = try_get_action(self.press)
            func()
        elif isinstance(self.press, list):
            func = try_get_action(self.press[0])
            func(*self.press[1:])
