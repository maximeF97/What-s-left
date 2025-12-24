from Player import player
from combat import combats
def old_bunker(player):
    while True:
        print("you are in an old bunker and you see a dusty old table with the items of you fallen friend on it.")
        print("1) Inspect the table")
        print("2) open the door")
        print("3) go back")
        choice = input("> ")

        if choice == "1":
            print("you find a rusty knife and a old_key.")
            
            if "old_key" not in player["inventory"]:
                player['inventory'].append('old_key')
                player['inventory'].append('rusty knife')
                player["bunker_items_taken"] = True
                print("items added to your inventory.")
            else:
                print("The table is empty.")
            print("items added to your inventory.")
        elif choice == "2":
            if "old_key"  in player["inventory"]:
                print ("you use the old_key to unlock the door and step outside into the wasteland.")
                player["bunker_door_unlocked"] = True
                wasteland(player)
            else:
                print("the door is locked. you need a key to open it.")
        elif choice == "3":
            return
        else:
            print("Invalid choice")

def wasteland(player):
    print("you took you first steps into the wasteland")
    print("everithing is desolate and quiet... when sudenly you hear a shivering noise behind you.")
    
    if not player["has_seen_alien"]:
        print("an small alien creature stands in the distance, looking at you with curious eyes.")
        player["has_seen_alien"] = True
    
    while True:
        print("what do you want to do?")
        print("1) approach the alien with your rusty knife")
        print("2) keep your distance and observe")
        print("3) run away")
        choice = input("> ")
        if choice == "1":
            alien = {
                "health": 6,
                "hit_chance": 60  # percent
            }
            if "rusty knife" in player["inventory"]:
                result = combats(player, alien)

            if result == "win":
                print(" you aproched the alien with your rusty knife, it speeted acid at you, causing you to lose  health points.")
                print("you then successfuly stabbed the alien who shrieked and colapsed.")
                return


            elif result == "lose":
                print("Game over.")
                exit()
            else:
                print("You have nothing to fight with.")
            print(f"your health is now {player['health']}")
            print("you survived for now...")
            return
        elif choice == "2":
            print("you kept your distance and observed the alien, it seemed harmless and eventually walked away.")
            print("you survived for now...")
            return
        elif choice == "3":
            print("you ran away from the alien, tripping over a rock and injuring yourself, losing 1 health point.")
            player["health"] -= 1
            print(f"your health is now {player['health']}")
            print("you survived for now...")
            return
        else:
            print("Invalid choice")