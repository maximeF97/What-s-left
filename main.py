from Player import player
from rooms import old_bunker
from combat import combats
import random
def main():
    print("welcome to what's left of us")

    running = True
    while running:
        print("\nWhat do you want to do?")
        print("1) Start game")
        print("2) Quit")

        choice = input("> ")

        if choice == "1":
            print("you wake up in an old abandon bunker, the last survivor of the apocalypse.")
            print(f"health: {player['health']}")
            old_bunker(player)
        elif choice == "2":
            print("goodbye!")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

