from typing import Callable, List, Union

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ConfigAction = Union[str, List]

class ActionButton(Gtk.Button):
    def __init__(self, press: ConfigAction, long_press: ConfigAction):
        super().__init__(label="Test")
        self.press = press
        self.long_press = long_press
        self.connect('clicked', self.call_action)

    def call_action(self, button: Gtk.Button) -> None:
        print("press", self.press)
