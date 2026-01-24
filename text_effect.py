import re
from ui import ui_write, ui_print, ui_after

_message_queue = []
_is_running = False


def slow_print_char(text: str, cps: int = 30, punctuation_pause: bool = True):
    """
    Backwards-compatible wrapper that just uses suspense_print with a delay
    derived from cps. punctuation_pause is ignored but kept for signature.
    """
    cps = max(1, cps)
    delay = max(5, int(1000 / cps))
    suspense_print(text, delay=delay)


def slow_print_word(text: str, wps: float = 3.0, punctuation_pause: bool = True):
    """
    Backwards-compatible wrapper: just delegates to suspense_print.
    """
    suspense_print(text)


def suspense_print(text: str, delay: int = 30):
    """
    Queue text to be printed character-by-character using ui_after.
    Calls are processed sequentially so characters never overlap.
    """
    global _is_running

    if text is None:
        text = ""

    _message_queue.append((text, max(5, delay)))

    if not _is_running:
        _run_next()


def _run_next():
    global _is_running

    if not _message_queue:
        _is_running = False
        return

    _is_running = True
    text, delay = _message_queue.pop(0)
    chars = list(text)
    index_state = {"i": 0}

    def step():
        i = index_state["i"]
        if i >= len(chars):
            ui_print("")  # newline after this message
            _run_next()
            return

        ui_write(chars[i])
        index_state["i"] += 1
        ui_after(delay, step)

    step()
