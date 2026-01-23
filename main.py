from Player import player as player, apply_setup_to_player
from character_setup import choose_name_and_stats
from rooms import old_bunker, wasteland
from combat import combats
import random
from systems import handle_global_input, get_choice, gain_xp
from inventory import use_item
from text_effect import suspense_print

try:
    from save_system import save_game, load_game, load_menu_interactive
    HAS_INTERACTIVE_LOAD = True
except ImportError:
    from save_system import save_game, load_game
    load_menu_interactive = None
    HAS_INTERACTIVE_LOAD = False


def _start_new_game():
    setup = choose_name_and_stats()
    apply_setup_to_player(player, setup)

    suspense_print("You finished the last of your rations. Time to face the world.")
    suspense_print(f"Health: {player['health']}")
    player.setdefault("scene", "OldBunker")
    old_bunker(player)


def resume_game(player):
    scene = (player.get("scene") or "").lower()
    if scene in ("oldbunker", "old_bunker", "bunker"):
        return old_bunker(player)
    elif scene in ("wasteland",):
        return wasteland(player)
    return old_bunker(player)


def start_game():
    suspense_print("Welcome to What's Left of Us.")
    suspense_print(
        "Decades after a mysterious blast from outer space decimated most of the world "
        "in the blink of an eye, you are one of the few survivors trying to understand "
        "what happened — and what’s left of us."
    )
    main_menu()


def main_menu():
    suspense_print("\nWhat do you want to do?")
    suspense_print("1) Start new game")
    suspense_print("2) Quit")
    suspense_print("C) Continue")
    suspense_print("L) Load game")
    if HAS_INTERACTIVE_LOAD:
        suspense_print("I) Interactive Load Menu")
    suspense_print("S) Save current game")

    choice = get_choice()

    if handle_global_input(choice, player):
        return

    if choice == "1":
        _start_new_game()

    elif choice == "2":
        suspense_print("Goodbye.")
        return

    elif choice.lower() == "c":
        loaded = load_game()
        if not loaded:
            return
        player.clear()
        player.update(loaded)
        suspense_print("Game loaded.")
        resume_game(player)

    elif choice.lower() == "l":
        loaded = load_game()
        if not loaded:
            return
        player.clear()
        player.update(loaded)
        suspense_print("Game loaded.")
        resume_game(player)

    elif HAS_INTERACTIVE_LOAD and choice.lower() == "i":
        loaded = load_menu_interactive()
        if not loaded:
            return
        player.clear()
        player.update(loaded)
        suspense_print("Game loaded.")
        resume_game(player)

    elif choice.lower() == "s":
        if not player:
            suspense_print("Nothing to save.")
            return
        player.setdefault("scene", "OldBunker")
        save_game(player)
        suspense_print("Game saved.")

    else:
        suspense_print("Invalid choice.")
        main_menu()