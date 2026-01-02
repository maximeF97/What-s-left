from Player import player
from rooms import old_bunker
from combat import combats
import random
from save_system import save_game, load_game
from systems import  handle_global_input, get_choice, gain_xp
from inventory import use_item 
def main():
    print("welcome to what's left of us")
    print("decade after a mysterious blast from outer space decimated most of the world in the blink of an eye , you are one of the few survivors trying to navigate the ruins of civilization trying to find what actually happened and what's left of us.")
    running = True
    while running:
        print("\nWhat do you want to do?")
        print("1) Start game")
        print("2) Quit")
        print("L) Load game")
        choice = get_choice()

        
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            print("you finishted the last of your rations time to face the world out there again.")
            print(f"health: {player['health']}")
            old_bunker(player)
        elif choice == "2":
            print("goodbye!")
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

