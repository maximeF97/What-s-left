from Player import player
from rooms import old_bunker
from combat import combats
import random
def main():
    print("welcome to what's left of us")
    print("decade after a mysterious blast from outer space decimated most of the world in the blink of an eye , you are one of the few survivors trying to navigate the ruins of civilization trying to find what actually happened and what's left of us.")
    running = True
    while running:
        print("\nWhat do you want to do?")
        print("1) Start game")
        print("2) Quit")

        choice = input("> ")

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

