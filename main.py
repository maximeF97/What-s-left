from Player import player as player, apply_setup_to_player
from character_setup import choose_name_and_stats
from rooms import old_bunker
from combat import combats
import random
from save_system import save_game, load_game
from systems import handle_global_input, get_choice, gain_xp
from inventory import use_item

def start_game():
    """Run character creation and apply the result to the module-level player dict."""
    setup = choose_name_and_stats()
    apply_setup_to_player(player, setup)
    return player

def main():
    print("welcome to what's left of us")
    print("decade after a mysterious blast from outer space decimated most of the world in the blink of an eye , you are one of the few survivors trying to navigate the ruins of civilization trying to find what actually happened and what's left of us.")
    running = True
    while running:
        print("\nWhat do you want to do?")
        print("1) Start new game")
        print("2) Quit")
        print("L) Load game")
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
            old_bunker(player)

        # Quit
        elif choice == "2":
            print("goodbye!")
            running = False

        # Load saved game (both 'L' and 'l')
        elif choice.lower() == "l":
            loaded = load_game()
            if not loaded:
                # load_game already prints an error message
                continue
            # update the module-level player dict in-place so other modules keep referencing it
            player.clear()
            player.update(loaded)
            print("Game loaded. Resuming from your saved state.")
            print(f"health: {player.get('health', 'unknown')}")
            # Jump into a room/state after loading:
            old_bunker(player)

        # Save current game (both 'S' and 's')
        elif choice.lower() == "s":
            # Check if there is something meaningful to save
            if not player or (isinstance(player, dict) and not player.get("name") and not player.get("player_name")):
                print("No player data to save. Start or load a game first.")
                continue
            save_game(player)

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
