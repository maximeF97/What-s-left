import time
import re
from ui import ui_write, ui_print

# Set to True if you ever want real delays in pure terminal mode.
ENABLE_TEXT_DELAYS = False


def slow_print_word(text: str, wps: float = 3.0, punctuation_pause: bool = True) -> None:
    if wps <= 0:
        wps = 0.1

    base_delay = 1.0 / wps
    words = re.findall(r"\S+\s*", text)

    for w in words:
        ui_write(w)

        if ENABLE_TEXT_DELAYS:
            extra = 0.0
            if punctuation_pause:
                trimmed = w.strip()
                if trimmed.endswith(("...", "…")):
                    extra = base_delay * 2.5
                elif trimmed.endswith((".", "!", "?")):
                    extra = base_delay * 2.0
                elif trimmed.endswith((",", ";", ":")):
                    extra = base_delay * 1.25
            time.sleep(base_delay + extra)

    ui_print("")  # newline


def slow_print_char(text: str, cps: int = 28, punctuation_pause: bool = True) -> None:
    if cps <= 0:
        cps = 1

    base_delay = 1.0 / cps

    for ch in text:
        ui_write(ch)

        if ENABLE_TEXT_DELAYS:
            extra = 0.0
            if punctuation_pause:
                if ch in (".", "!", "?"):
                    extra = base_delay * 8
                elif ch in (",", ";", ":"):
                    extra = base_delay * 4
            time.sleep(base_delay + extra)

    ui_print("")  # newline


def suspense_print(text: str) -> None:
    slow_print_word(text, wps=6, punctuation_pause=True)
