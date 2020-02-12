from typing import Dict, Callable

ACTIONS: Dict[str, Callable] = dict()

def register_action(func):
    """ A decorator that registers a function as an action. """
    ACTIONS[func.__name__] = func
    return func

@register_action
def nop():
    """ Do nothing. """

@register_action
def kill_focused_window():
    """ Kill the focused window. ONLY WORKS IN SWAY """

@register_action
def run_command(command: str):
    """ Runs a command. """
