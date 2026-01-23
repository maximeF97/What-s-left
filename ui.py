# ui.py
_output_callback = None
_input_callback = None

def set_ui(output_fn, input_fn):
    global _output_callback, _input_callback
    _output_callback = output_fn
    _input_callback = input_fn

def ui_print(text):
    if _output_callback:
        _output_callback(text)
    else:
        print(text)

def ui_input(prompt="> "):
    if _input_callback:
        return _input_callback(prompt)
    return input(prompt)
def ui_write(text):
    if _output_callback:
        _output_callback(text)
    else:
        print(text, end="")