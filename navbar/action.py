import asyncio
from typing import Dict, Callable

from navbar import get_connection

ACTIONS: Dict[str, Callable] = dict()

def try_get_action(name: str) -> Callable:
    """ Return the specified action, or nop. """
    if name in ACTIONS:
        return ACTIONS[name]
    print("Could not find action {}. Returning nop.".format(name))
    return ACTIONS['nop']

def __call_command(command: str) -> None:
    """ Call an i3 command. """
    conn = get_connection()
    asyncio.create_task(conn.command(command))

async def __send_back_to_focused_window() -> None:
    """ Move the mouse over the focused window then send the back button. """
    conn = get_connection()
    tree = await conn.get_tree()
    focused_rect = tree.find_focused().rect
    win_center_x = focused_rect.x + focused_rect.width // 2
    win_center_y = focused_rect.y + focused_rect.height // 2
    print("center: {} {}".format(win_center_x, win_center_y))
    await conn.command("seat * cursor set {} {}".format(win_center_x, win_center_y))
    await conn.command("seat * cursor press button8")
    await conn.command("seat * cursor release button8")

def register_action(func):
    """ A decorator that registers a function as an action. """
    ACTIONS[func.__name__] = func
    return func

@register_action
def nop(*args):
    """ Do nothing. """

@register_action
def kill_focused_window():
    """ Kill the focused window. """
    __call_command("kill")

@register_action
def back():
    """ Send the browser-back mouse-click to the curently focused window.

    This is only meant to be used with a touchscreen, since the cursor is moved
    arround in order to send the button to the correct window.
    """
    asyncio.create_task(__send_back_to_focused_window())

@register_action
def run_command(command: str):
    """ Runs a command. """

@register_action
def run_i3_command(command: str):
    """ Run an i3 command. """
    __call_command(command)
