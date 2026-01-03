from Player import player as player, apply_setup_to_player
from character_setup import choose_name_and_stats
from rooms import old_bunker, wasteland
from combat import combats
import random
from systems import handle_global_input, get_choice, gain_xp
from inventory import use_item

# Prefer importing interactive load if available
try:
    from save_system import save_game, load_game, load_menu_interactive
    HAS_INTERACTIVE_LOAD = True
except ImportError:
    from save_system import save_game, load_game
    load_menu_interactive = None
    HAS_INTERACTIVE_LOAD = False


def start_game():
    """Run character creation and apply the result to the module-level player dict."""
    setup = choose_name_and_stats()
    apply_setup_to_player(player, setup)
    return player


def resume_game(player):
    """
    Route to the correct room/state based on the saved scene.
    Fallback to old_bunker if no scene is known.
    """
    scene = (player.get("scene") or "").lower()
    if scene in ("oldbunker", "old_bunker", "bunker"):
        return old_bunker(player)
    elif scene in ("wasteland",):
        return wasteland(player)
    # TODO: add more scene mappings here
    return old_bunker(player)


def main():
    print("welcome to what's left of us")
    print("decade after a mysterious blast from outer space decimated most of the world in the blink of an eye , you are one of the few survivors trying to navigate the ruins of civilization trying to find what actually happened and what's left of us.")
    running = True
    while running:
        print("\nWhat do you want to do?")
        print("1) Start new game")
        print("2) Quit")
        print("C) Continue (latest or last-selected)")
        print("L) Load game (auto last-selected or latest)")
        if HAS_INTERACTIVE_LOAD:
            print("I) Interactive Load Menu")
        print("S) Save current game")

        choice = get_choice()

        # Allow global handlers to intercept input (e.g. debug keys)
        if handle_global_input(choice, player):
            continue

        # Start new game: create player and immediately enter first scene
        if choice == "1":
            start_game()  # creates/overwrites player values in-place
            print("you finishted the last of your rations time to face the world out there again.")
            print(f"health: {player['health']}")
            # Ensure an initial scene so saves know where to resume
            player.setdefault("scene", "OldBunker")
            old_bunker(player)

        # Quit
        elif choice == "2":
            print("goodbye!")
            running = False

        # Continue: instantly load latest or last-selected
        elif choice.lower() == "c":
            loaded = load_game()
            if not loaded:
                # load_game already prints an error message
                continue
            # Update the module-level player dict in-place so other modules keep referencing it
            player.clear()
            player.update(loaded)
            print("Game loaded. Resuming from your saved state.")
            print(f"health: {player.get('health', 'unknown')}")
            resume_game(player)

        # Load saved game (both 'L' and 'l') - same behavior, routes to saved scene
        elif choice.lower() == "l":
            loaded = load_game()
            if not loaded:
                continue
            player.clear()
            player.update(loaded)
            print("Game loaded. Resuming from your saved state.")
            print(f"health: {player.get('health', 'unknown')}")
            resume_game(player)

        # Interactive load menu (if available): lets you select a specific save, defaults to last-selected
        elif HAS_INTERACTIVE_LOAD and choice.lower() == "i":
            loaded = load_menu_interactive()
            if not loaded:
                continue
            player.clear()
            player.update(loaded)
            print("Game loaded. Resuming from your saved state.")
            print(f"health: {player.get('health', 'unknown')}")
            resume_game(player)

        # Save current game (both 'S' and 's')
        elif choice.lower() == "s":
            # Check if there is something meaningful to save
            if not player or (isinstance(player, dict) and not player.get("name") and not player.get("player_name")):
                print("No player data to save. Start or load a game first.")
                continue
            # Ensure we persist scene so we can resume to the correct place
            player.setdefault("scene", "OldBunker")
            save_game(player)

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()