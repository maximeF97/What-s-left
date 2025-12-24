from Player import player

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
        elif choice == "2":
            print("goodbye!")
        else:
            print("Invalid choice")
def old_bunker():
    while
    print("you are in an old bunker and you see a dusty old table with the items of you fallen friend on it.")
    print("1) Inspect the table")
    print("2) open the door")
    print("3) go back")
    choice = input("> ")

    if choice == "1":
        print("you find a rusty knife and a old_key.")
        player['inventory'].append('rusty knife')
        if "old_key" not in player["inventory"]:
            player['inventory'].append('old_key')
        print("items added to your inventory.")
    elif choice == "2":
        if "old_key"  in player["inventory"]:
            print ("you use the old_key to unlock the door and step outside into the wasteland.")
        print("the door is locked. you need a key to open it.")
    elif choice == "3":
        return
    else:
        print("Invalid choice")
if __name__ == "__main__":
    main()

