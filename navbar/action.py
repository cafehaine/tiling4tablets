import asyncio
from typing import Dict, Callable

from navbar import get_connection

ACTIONS: Dict[str, Callable] = dict()

def try_get_action(name: str) -> Callable:
    if name in ACTIONS:
        return ACTIONS[name]
    print("Could not find action {}. Returning nop.".format(name))
    return ACTIONS['nop']

def __call_command(command: str) -> None:
    """ Call an i3 command. """
    conn = get_connection()
    asyncio.create_task(conn.command(command))

def register_action(func):
    """ A decorator that registers a function as an action. """
    ACTIONS[func.__name__] = func
    return func

@register_action
def nop(*args):
    """ Do nothing. """

@register_action
def kill_focused_window():
    """ Kill the focused window. ONLY WORKS IN SWAY """
    __call_command("kill")

@register_action
def back():
    """ Send the browser-back mouse-click to the curently focused window. """

@register_action
def run_command(command: str):
    """ Runs a command. """

@register_action
def run_i3_command(command: str):
    """ Run an i3 command. """
    __call_command(command)
