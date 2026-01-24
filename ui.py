# ui.py
_output_callback = None   # line output (with newline)
_write_callback = None    # raw text output (no newline)
_input_callback = None
_after_callback = None    # scheduler: after_fn(ms, fn, *args)
_inventory_callback = None
_equipment_callback = None

def set_ui(output_fn, input_fn, write_fn=None, after_fn=None, inventory_fn=None, equipment_fn=None):
    """
    Connects the game logic to the active UI.
    - output_fn(text): print a full line
    - write_fn(text): append raw text (no newline)
    - input_fn(prompt): blocking input
    - after_fn(ms, fn, *args): schedule a callback
    - inventory_fn(inventory_dict): update inventory display
    - equipment_fn(player_dict): update equipment/stats display
    """
    global _output_callback, _write_callback, _input_callback, _after_callback, _inventory_callback, _equipment_callback
    _output_callback = output_fn
    _write_callback = write_fn or output_fn
    _input_callback = input_fn
    _after_callback = after_fn
    _inventory_callback = inventory_fn
    _equipment_callback = equipment_fn


def ui_print(text: str):
    if _output_callback:
        _output_callback(text)
    else:
        print(text)


def ui_write(text: str):
    if _write_callback:
        _write_callback(text)
    else:
        print(text, end="")


def ui_input(prompt: str = "> "):
    if _input_callback:
        return _input_callback(prompt)
    raise RuntimeError("ui_input called but no UI input callback is set")


def ui_after(delay_ms: int, callback, *args):
    """
    Schedule callback(*args) after delay_ms milliseconds.
    Falls back to immediate call if no UI scheduler is set.
    """
    if _after_callback:
        _after_callback(delay_ms, callback, *args)
    else:
        callback(*args)


def ui_update_inventory(inventory: dict):
    """
    Update the inventory display in the GUI.
    Falls back to no-op if no callback is set.
    """
    if _inventory_callback:
        _inventory_callback(inventory)


def ui_update_equipment(player: dict):
    """
    Update the equipment/stats display in the GUI.
    Falls back to no-op if no callback is set.
    """
    if _equipment_callback:
        _equipment_callback(player)