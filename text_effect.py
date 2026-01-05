import sys
import time
import re

def slow_print_word(text: str, wps: float = 3.0, punctuation_pause: bool = True) -> None:
    """
    Print text word-by-word.
    wps: words per second (lower = slower, e.g., 2.0 for suspense)
    punctuation_pause: add extra delay after punctuation.
    """
    if wps <= 0:
        wps = 0.1
    base_delay = 1.0 / wps
    # Split words, preserving trailing spaces so formatting looks natural
    words = re.findall(r"\S+\s*", text)

    for w in words:
        sys.stdout.write(w)
        sys.stdout.flush()

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
    sys.stdout.write("\n")
    sys.stdout.flush()


def slow_print_char(text: str, cps: int = 28, punctuation_pause: bool = True) -> None:
    """
    Print text character-by-character.
    cps: characters per second (lower = slower, e.g., 20 for suspense)
    """
    if cps <= 0:
        cps = 1
    base_delay = 1.0 / cps

    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()

        extra = 0.0
        if punctuation_pause:
            if ch in (".", "!", "?"):
                extra = base_delay * 8
            elif ch in (",", ";", ":"):
                extra = base_delay * 4

        time.sleep(base_delay + extra)

    sys.stdout.write("\n")
    sys.stdout.flush()


def suspense_print(text: str) -> None:
    """
    Handy default for suspenseful narration: slower words with punctuation pauses.
    """
    slow_print_word(text, wps=4, punctuation_pause=True)