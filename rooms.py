
from combat import combats
def old_bunker(player):
    while True:
        print("you are in an old bunker and you see a dusty old table with the items of you fallen friend on it.")
        print("1) Inspect the table")
        print("2) open the door")
        print("3) go back")
        choice = input("> ")

        if choice == "1":
            
            
            if not player["bunker_items_taken"]:
                print("you find a rusty knife and a old_key.")
                player['inventory'].append('old_key')
                player['inventory'].append('rusty knife')
                player["bunker_items_taken"] = True
                print("items added to your inventory.")
            else:
                print("The table is empty.")
        elif choice == "2":
            if "old_key"  in player["inventory"]:
                print ("you use the old_key to unlock the door and step outside into the wasteland.")
                player["bunker_door_unlocked"] = True
                wasteland(player)
                return
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
            if "rusty knife" not in player["inventory"]:
                print("You have nothing to fight with.")
                return

            alien = {
                "health": 6,
                "hit_chance": 60
            }

            result = combats(player, alien)

            if result == "win":
                print("You approached the alien with your rusty knife.")
                print("It spits acid, but you manage to stab it.")
                wasteland_cross_road(player)
                return

            elif result == "run":
                print("You escape back to the bunker.")
                return

            elif result == "lose":
                print("Game over.")
                exit()

        elif choice == "2":
            print("you kept your distance and observed the alien, it seemed harmless and eventually walked away.")
            print("you survived for now...")
            wasteland_cross_road(player)
            return
        elif choice == "3":
            print("you ran away from the alien, tripping over a rock and injuring yourself, losing 1 health point.")
            player["health"] -= 1
            print(f"your health is now {player['health']}")
            print("you survived for now...")
            return
        else:
            print("Invalid choice")

def wasteland_cross_road(player):
    print("you arived at a a crossroad you see and old post with two signs.")
    while True:
        print("1) follow the sign to the left 'grove_town'")
        print("2) follow the sign to the right 'hospital'")
        print("3) you dont trust signs and walk straight ahead into the wasteland")
        choice = input("> ")
        if choice == "1":
            print("you follow the sign to grove_town")
            grove_town(player)
            return
        elif choice == "2":
            print("you follow the sign to the hospital")
            hospital(player)
            return
        elif choice == "3":
            print("you walk straight ahead into the wasteland")
            wasteland3(player)
            return

def grove_town(player):
    print("you arrived at grove_town, nothing remains but the ruins of a police station and a few burned down houses.")
    while True:
        print("1) explore the police station")
        print("2) explore the burned down houses")
        print("3) go back to the crossroad")
        choice = input("> ")
        if choice == "1":
            police_station(player)
        elif choice == "2":
            burned_houses(player)
        elif choice == "3":
            print("you go back to the crossroad")
            wasteland_cross_road(player)
            return
        else:
            print("Invalid choice")

def police_station(player):
    while True:
        print("you enter the police station, you see something move to another room but when you enter you only see a desk with a mug on it.")
        print("1) inspect the mug")
        print("2) go back to main room") 
        choice = input("> ")
        
        if choice == "1":
            if not player["has_seen_alien"]:
                print("you try to grab the mug when sudenly it turn back into an small alien creature and attacks you!")
                player["has_seen_alien"] = True
                alien = {
                    "health": 4,
                    "hit_chance": 65
                }
                result = combats(player, alien)

                if result == "win":
                    print("You defeated the small alien creature and found some supplies.")
                    player['inventory'].append('revolver')
                    player['inventory'].append(3 * ' revolver_ammo')
                    player['inventory'].append('police station key')
                    print("revolver and ammo added to your inventory.")
                    return
                    
                elif result == "run":
                    print("You escaped back to grove_town.")
                elif result == "lose":
                    print("Game over.")
                    exit()
            else:
                print("nothing else to do here, you go back to the main room of the police station")
                return
        elif choice == "2":
            print("you go back to the main room of the police station")
            while True:
                print("1) explore the cells")
                print("2) explore the evidence room")
                print("3) exit the police station")
                choice = input("> ")
                if choice =="1":
                    print("you enter the cells")
                    if not player["has police station prisoner was freed"]:
                        print("you find empty cells but in one of them there is an man locked inside wit a note tape to the cell door'he is an alien dont let it out'.")
                        while True:
                            print("1) free the prisoner")
                            print("2) leave him locked up")
                            choice = input("> ")
                            if choice =="1":
                                print("you free the prisoner that suddenly transforms into a hostile alien and attacks you!")
                                alien = {
                                    "health": 20,
                                    "hit_chance": 70
                                }
                                result = combats(player, alien)

                                if result == "win":
                                    print("You defeated the alien prisoner.")
                                    player['inventory'].append('hospital safe key')
                                    player["has police station prisoner was freed"] = True
                                    return
                                    
                                elif result == "run":
                                    print("You escaped back to grove_town.")
                                    player["has police station prisoner was freed"] = False
                                    return
                                elif result == "lose":
                                    print("Game over.")
                                    exit()
                            elif choice =="2":
                                print("you leave the prisoner locked up.")
                                player["has police station prisoner was freed"] = False
                                break
                            else:
                                print("Invalid choice")

                        
                        
                if choice =="2":
                    print("you enter the evidence room")
                    if "police station key"  in player["inventory"]:
                        print ("you use the police station key to unlock the door.")
                        if not player["has police station evidence room itemstaken"]:
                            print("you find some ammo and a medkit.")
                            player['inventory'].append('medkit')
                            player['inventory'].append(2 * 'revolver_ammo')
                            player["has police station evidence room itemstaken"] = True
                            print("medkit added to your inventory.")
                        else:
                            print("the evidence room is empty.")
                    else:
                        print("the door is locked. you need a key to open it.")
                if choice =="3":
                    print("you exit the police station")
                    grove_town(player)
                    return
                else:
                    print("Invalid choice")
        else:
            print("Invalid choice") 
def burned_houses(player):
    print("you explore the burned down houses and find an leaking healing salve, you une it before it run out and recover 3 health points.")
    player["health"] += 3
    print(f"your health is now {player['health']}")
def hospital(player):
    print("you arrived at the hospital, the building is mostly intact but the front door is locked.")
    while True:
        print("1) try to force the door open")
        print("2) look for another way in")
        print("3) go back to the crossroad")
        choice = input("> ")
        if choice == "1":
            print("you try to force the door open but it is too sturdy, you hurt yourself in the attempt losing 1 health point.")
            player["health"] -= 1
            print(f"your health is now {player['health']}")
        elif choice == "2":
            print("you find a side entrance that is slightly ajar and manage to slip inside.")
            hospital_inside(player)
            return
        elif choice == "3":
            print("you go back to the crossroad")
            wasteland_cross_road(player)
            return
        else:
            print("Invalid choice")