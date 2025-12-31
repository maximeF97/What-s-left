from unittest import result
from systems import use_item, gain_xp, handle_global_input, get_choice
from Player import skill_check
from combat import combats
import random
def old_bunker(player):
    while True:
        print("you are in an old bunker and you see a dusty old table with the items of you fallen friend on it.")
        print("1) Inspect the table")
        print("2) open the door")
        print("3) go back")
        print("I) Open inventory")

        choice = get_choice()

        
        if handle_global_input(choice, player):
            continue
        

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

def new_func():
    choice = input("> ")
    return choice

def fight_enemy(player, enemy):
    result = combats(player, enemy)
    if result["result"] == "win":
        gain_xp(player, enemy.get("xp", 0))
        return True
    exit()
def wasteland(player):
    while True:
        print("you took you first steps into the wasteland")
        print("everithing is desolate and quiet... when sudenly you hear a shivering noise behind you.")
        
        if not player["has_seen_alien"]:
            print("an small alien creature stands in the distance, looking at you with curious eyes.")
            player["has_seen_alien"] = True
        
        
            print("what do you want to do?")
            print("1) approach the alien with your rusty knife")
            print("2) keep your distance and observe")
            print("3) run away")
            print("I) Open inventory")

            choice = get_choice()

            
            if handle_global_input(choice, player):
                continue
            
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
                    gain_xp(player, result["xp"])
                    print("You approached the alien with your rusty knife.")
                    print("It spits acid, but you manage to stab it.")
                    player["has_seen_alien"] = True
                    wasteland_cross_road(player)
                    return

                elif result == "run":
                    print("You escape back to the bunker.")
                    old_bunker(player)
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
        print("I) Open inventory")

        choice = get_choice()

        
        if handle_global_input(choice, player):
            continue
        
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
        print("I) Open inventory")

        choice = get_choice()

        
        if handle_global_input(choice, player):
            continue
        
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
        print("\nYou are inside the ruined police station you see something to in a other room but when you go there you only see a mug on a desk.")
        print("1) Inspect the desk")
        print("2) Explore the cells")
        print("3) Enter the evidence room")
        print("4) Leave the police station")
        print("I) Open inventory")
        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        

        if choice == "1":
            inspect_desk(player)

        elif choice == "2":
            explore_cells(player)

        elif choice == "3":
            evidence_room(player)

        elif choice == "4":
            print("You leave the police station.")
            return

        else:
            print("Invalid choice.")

def inspect_desk(player):
    if not player.get("has_seen_police_station_alien", False):
        print("The mug suddenly transforms into a small alien!")

        alien = {"health": 4, "hit_chance": 65, "xp": 25}
        result = combats(player, alien)

        player["has_seen_police_station_alien"] = True

        if result["result"] == "win":
            gain_xp(player, result["xp"])
            print("You defeat the alien and find supplies.")
            player["inventory"].append("revolver")
            player["inventory"].extend(["revolver_ammo"] * 3)
            player["inventory"].append("police_station_key")
            gain_xp(player, 15)  # bonus XP

        elif result["result"] == "lose":
            exit()
    else:
        print("Just an empty desk and a broken mug.")


def explore_cells(player):
    while True:
        if player["has_freed_police_station_prisoner"]:
            print("The cells are empty.")
            return

        print("A man is locked in a cell. A note reads: 'Do not free him. He is an alien.'")
        print("1) Free him")
        print("2) Leave him")
        print("I) Open inventory")

        choice = get_choice()

            
        if handle_global_input(choice, player):
            continue



        if choice == "1":
            print("The prisoner transforms into a large hostile alien!")

            alien = {"health": 15, "hit_chance": 70, "xp": 100}
            result = combats(player, alien)

            if result["result"] == "win":
                gain_xp(player, result["xp"])
                print("You defeated the alien prisoner.")
                player["inventory"].append("hospital_safe_key")
                gain_xp(player, 30)
                player["has_freed_police_station_prisoner"] = True

            elif result["result"] == "lose":
                exit()
        elif choice == "2":
            print("You leave the prisoner locked up.")
            return
        
def evidence_room(player):
    if "police_station_key" not in player["inventory"]:
        print("The door is locked.")
        return

    if player["has_unlocked_police_station_evidence_room"]:
        print("The evidence room is empty.")
        return

    print("You find ammo and a medkit.")
    player["inventory"].extend(["revolver_ammo"] * 2)
    player["inventory"].append("medkit")
    player["has_unlocked_police_station_evidence_room"] = True

def burned_houses(player):
    
    if not player.get("burned_houses_looted", False):
        print("you explore the burned down houses and find an leaking healing salve, you une it before it run out and recover 3 health points.")
        player["health"] += 3
        print(f"your health is now {player['health']}")
        player["burned_houses_looted"] = True
    else:
        print("nothing else of interest here")
    

def hospital(player):
    print("you arrived at the hospital, the building is mostly intact but the front door is locked.")
    while True:
        print("1) try to lockpick the door open")
        print("2) look for another way in")
        print("3) look through the windows")
        print("4) go back to the crossroad")
        print("I) Open inventory")
        choice = get_choice()   

        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("has_oppened_hospital_lock", False):
                print("the door is already unlocked, you enter the hospital.")
                hospital_inside(player)
                return
            else:
                if "bobby_pins" in player["inventory"]:
                    if skill_check(player, "lockpicking", 50):
                        print("you successfully lockpick the door and enter the hospital.")
                        player["has_oppened_hospital_lock"] = True
                        hospital_inside(player)
                        return
                    else:
                        print("you failed to lockpick the door.")
                else:
                    print("you don't have any bobby pins.")
        elif choice == "2":
            print("you find a side entrance but there is a weird looking cactus.")
            hospital_side_entrance(player)
            return
        elif choice == "3":
            if player["has_pass_window_check"]:
                print("you already looked through the windows and saw the alien inside the hospital.")
                continue
            else:
                print("you try to look through the dirty windows and see moving shadows.")
                if skill_check(player, "perception", 40):
                    print("you clearly see an alien moving inside the hospital, better be careful.")
                    player["has_pass_window_check"] = True
                else:
                    print("you can't see much through the dirty windows.")

        elif choice == "4":
            print("you go back to the crossroad")
            wasteland_cross_road(player)
            return
        else:
            print("Invalid choice")

def hospital_side_entrance(player):

    while True:
        print("1) sneak past the cactus")
        print("2) shoot the cactus with your revolver")
        print("3) go back to the hospital entrance")
        print("I) Open inventory")
        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            print("the paranoia of the metamorph wastelang is geting to you and  you try to sneak past the evil cactus.")
            if skill_check(player, "stealth", 50):
                print("you successfully sneak past the cactus and enter the hospital through the side entrance.")
                hospital_inside(player)
                return
            else:
                print("you failed to sneak past the cactus but lucky for you the castus is just a cactus...")
                hospital_inside(player)
                return
        elif choice == "2":
            if "revolver" not in player["inventory"]:
                print("You don't have a revolver.")
                continue
            if player["has_killed_cactus"]:
                print("the cactus is already destroyed.")
                continue
            if "revolver_ammo" not in player["inventory"]:
                print("Click. You're out of ammo.")
                continue
            
            print("you shoot the cactus and it turn out that the evil cactus was juste a inocent plants...")
            player["inventory"].remove("revolver_ammo")
            cactus = {
                "health": 1,
                "hit_chance": 0,   # never hits
                "damage": 0,       # no damage
                "xp": 0            # no XP reward
                }

            result = combats(player, cactus)
            if result["result"] == "win":
                print("You killed the only vegetation left in the wasteland for miles...")
                player["has_killed_cactus"] = True
                hospital_inside(player)
                
                return
            

            elif result["result"] == "lose":
                exit()
        
        elif choice == "3":
            print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            print("Invalid choice")

def hospital_inside(player):
    while True:
        if not player.get("hospital_metamorph_killed", False):

            if player.get("has_pass_window_check", False):
                hospital_metamorph_encounter(player)
                continue

            print("You step inside the hospital and a hidden tentacle trips you!")
            player["health"] -= 2
            if player["health"] <= 0:
                print("You collapse from your injuries...")
                exit()

            print(f"You lose 2 health points. Health: {player['health']}")
            fight_enemy(player, {"health": 10, "hit_chance": 75, "xp": 70})
            player["hospital_metamorph_killed"] = True
            print("You defeated the alien metamorph.")
            continue
        print("You are inside the hospital. The alien metamorph lies dead.")

        print("1) get up the stairs to the second floor")
        print("2) search the hospital right room")
        print("3) search the room ahead")
        print("4) search the left room")
        print("5) go to the back door")
        print("6) go back to the hospital entrance")
        print("I) Open inventory")  
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            print("you go up to the first floor and see two doors.")
            hospital_first_floor(player)
        elif choice == "2":
            print("you search the room and find a safe with 3 keyholes.")
            if not player.get("has_opened_hospital_safe", False):

                if "hospital_safe_key" in player["inventory"] and "second_hospital_safe_key" in player["inventory"] and "third_hospital_safe_key" in player["inventory"]:
                    print("you use the hospital safe keys to open the safe and find some medical supplies,a alien laser rifle,and a alien energy cell.")
                    player["inventory"].append("medkit")
                    player["inventory"].append("healing_salve")
                    player["inventory"].append("alien_laser_rifle")
                    player["inventory"].append("alien_energy_cell")
                    player["has_opened_hospital_safe"] = True
                    continue
                else:
                    print("you need some keys to open the safe.")
                    continue
            else:
                print("the safe is already opened.")
                continue
        elif choice == "3":
            scavenger_room(player)
        elif choice == "4":
            if not player.get("has_hospital_left_room_been_searched", False):
                print("you search the left there is an bobby pin on the floor and stairs going down to the basement.")
                player["inventory"].append("bobby_pins")
                player["has_hospital_left_room_been_searched"] = True
                print("you pick up the bobby pins and add them to your inventory.")
                print("you take the stairs going down to the basement.")
                hospital_basement(player)
                return
            else:
                print("you take the stairs going down to the basement again.")
                hospital_basement(player)
        elif choice == "5":
            if not player.get("has_oppen hospital_back_door", False)
                if "hospital_back_door_key" in player["inventory"]:
                    print("you use the key and go toward the wasteland")
                else:
                    print("the door is locked you need a key")
        elif choice == "6":
            print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            print("Invalid choice")
def scavenger_room(player):
    while True:
        if not player.get("hospital_scavenger_killed", False):
                print("you enter the room ahead to find the remains of a scavenger, you notice some piece of his head have been altered with strange alien technology.")
                if skill_check(player, "perception", 20):
                    print("you see a red light blinking on the scavenger's head, indicating some sort of active alien tech.")

                else:
                    print("you don't notice anything unusual appart for the scavenger's head.")

                print("1) search the body")
                print("2) shoot the body with your revolver, just to be sure")
                print("I) Open inventory")
                choice = get_choice()
                if handle_global_input(choice, player):
                    continue

                if choice == "1":
                    print("you try to search the body but suddenly the scavenger comes back to life as a hostile alien cyborg!")
                    cyborg_alien = {"health": 11, "hit_chance": 70, "xp": 80}
                    result = combats(player, cyborg_alien)  
                    if result["result"] == "win":
                        gain_xp(player, result["xp"])
                        print("You defeated the alien cyborg scavenger.")
                        player["hospital_scavenger_killed"] = True
                        player["inventory"].append("alien_implant")
                        
                        return
                    elif result["result"] == "lose":    
                        exit()
                elif choice == "2":
                    if "revolver" not in player["inventory"]:
                        print("You don't have a revolver.")
                        continue
                    if "revolver_ammo" not in player["inventory"]:
                        print("Click. You're out of ammo.")
                        continue
                    if skill_check(player, "luck", 30):
                        player["inventory"].remove("revolver_ammo")
                        print("you shoot the body with your revolver, just to be sure,you hit for a near fatal wound the scavenger awakens like a cyborg and attacks you!")
                        hurt_cyborg_alien = {"health": 4, "hit_chance": 70, "xp": 80}
                        result = combats(player, hurt_cyborg_alien)
                        if result["result"] == "win":
                            gain_xp(player, result["xp"])
                            print("You defeated the alien cyborg scavenger.")
                            player["hospital_scavenger_killed"] = True
                            player["inventory"].append("alien_implant")
                            return
                        elif result["result"] == "lose":
                            exit()
                    else:
                        player["inventory"].remove("revolver_ammo")
                        print("you shoot the body with your revolver, you miss and the scavenger awakens like a cyborg and attacks you!")
                        cyborg_alien = {"health": 11, "hit_chance": 70, "xp": 80}
                        result = combats(player, cyborg_alien)  
                        if result["result"] == "win":
                            gain_xp(player, result["xp"])
                            print("You defeated the alien cyborg scavenger.")
                            player["hospital_scavenger_killed"] = True
                            player["inventory"].append("alien_implant")
                            return
                        elif result["result"] == "lose":
                            exit()
                else:
                    print("Invalid choice")            
        else:
            print("you enter the room ahead to that The scavenger lies motionless. Whatever it was, it's dead.")                

def hospital_metamorph_encounter(player):
    while True:
        print("You are inside the hospital. You remember seeing an alien through the window earlier but dont remember seeing that chair.")
        print("1) shoot the chair with your revolver")
        print("2) aproach the chair")
        print("3) go back to the hospital entrance")
        print("I) Open inventory")
    
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if "revolver" not in player["inventory"]:
                print("You don't have a revolver.")
                continue
            if "revolver_ammo" not in player["inventory"]:
                print("Click. You're out of ammo.")
                continue
            print("you sneak and shoot the chair for critical dammage whitch killed the alien metamorph")
            player["hospital_metamorph_killed"] = True
            player["inventory"].append("healing_salve")

            gain_xp(player, 50)
            player["inventory"].remove("revolver_ammo")
            return
        elif choice == "2":
            print("you aproach the chair and the alien metamorph attacks you!")
            alien = {"health": 10, "hit_chance": 75, "xp": 70}
            result = combats(player, alien)

            if result["result"] == "win":
                gain_xp(player, result["xp"])
                player["inventory"].append("healing_salve")
                print("You defeated the alien metamorph.")
                player["hospital_metamorph_killed"] = True  
                return

            elif result["result"] == "lose":
                exit()
        elif choice == "3":
            print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            print("Invalid choice")  

def hospital_basement(player):
    
    print(
        "You enter the basement. As you descend the stairs, you hear pained moans coming from below.\n"
        "At the bottom, a large alien stands before you — humanoid, wearing a white lab coat."
    )

    while True:
        print("\n1) Try to sneak attack the alien")
        print("2) Charge at the alien with your weapon drawn")
        print("3) Look around the room")
        print("4) Go back upstairs")
        print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # ───────────────────────────────
        # Sneak attack
        # ───────────────────────────────
        if choice == "1":
            if player.get("has_defeated_hospital_boss", False):
                hospital_basement_boss_defeated(player)
                return

            print("You attempt to sneak closer...")
            if skill_check(player, "stealth", 40):
                print("You catch the alien off guard!")
                alien = {"health": 15, "hit_chance": 70, "xp": 150}
            else:
                print("You fail to sneak — the alien turns toward you!")
                alien = {"health": 20, "hit_chance": 70, "xp": 150}

            result = combats(player, alien)
            if result["result"] == "win":
                finish_hospital_boss(player, result["xp"])
                return
            else:
                exit()

        # ───────────────────────────────
        # Direct attack
        # ───────────────────────────────
        elif choice == "2":
            if player.get("has_defeated_hospital_boss", False):
                hospital_basement_boss_defeated(player)
                return

            print("You charge at the alien!")
            alien = {"health": 20, "hit_chance": 70, "xp": 150}
            result = combats(player, alien)

            if result["result"] == "win":
                finish_hospital_boss(player, result["xp"])
                return
            else:
                exit()

        # ───────────────────────────────
        # Look around
        # ───────────────────────────────
        elif choice == "3":
            if not player.get("has_defeated_hospital_boss", False):
                print("you see a jailed man but the alien blocks your path — you’ll need to deal with it first.")
            else:
                hospital_basement_boss_defeated(player)
                return

        # ───────────────────────────────
        # Leave
        # ───────────────────────────────
        elif choice == "4":
            print("You retreat back upstairs.")
            hospital_inside(player)
            return

        else:
            print("Invalid choice.")

def finish_hospital_boss(player, xp):
    gain_xp(player, xp)
    print("You defeated the alien scientist.")

    player["inventory"].extend([
        "second_hospital_safe_key",
        "alien_scientist_suit",
        "hospital_back_door_key"
    ])

    player["has_defeated_hospital_boss"] = True
    hospital_basement_boss_defeated(player)


def hospital_basement_boss_defeated(player):
    print("you look around the room and see various alien experiments and equipment, but nothing useful.")
    print("there is also a cell in the corner with a prisoner inside.")
    while True:
        print("1) free the prisoner")
        print("2) ignore the prisoner")
        print("3) talk to the prisoner")
        print("4 go back upstairs")
        print("I) Open inventory")  
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("has_help_basement_prisoner", False):
                print("you free the prisoner from the cell, he thanks you and gives you map to a secret humain base.")
                player["inventory"].append("map_to_base")
                player["has_help_basement_prisoner"] = True
                return
            else:
                print("the prisoner is already free.")
                return
        elif choice == "2":
            print("you ignore the prisoner, who is begging for help.")
            return
        elif choice == "3":
            questione_prisoner(player)
        elif choice == "4":
            print("you go back upstairs")
            hospital_inside(player)
            return
        else:
            print("Invalid choice")
def questione_prisoner(player):
    while True:
        print("1) Ask about the alien metamorph")
        print("2) Ask about the alien cyborg scavenger")
        print("3) Ask about the alien scientist")
        print("4) Ask about what happened since the alien laser touchdown")
        print("5) Go back")
        print("I) Open inventory")
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            print(
                "The prisoner tells you that the alien metamorph is a dangerous creature "
                "that can mimic human forms and is highly aggressive. However, they do not "
                "mimic perfectly, and with enough perception, you can spot them.")
        elif choice == "2":
            print(
                "The prisoner explains that the alien cyborg scavenger was a friend of his "
                "who got captured by the alien scientist and experimented on, turning him "
                "into a cyborg against his will. The aliens have heavily experimented on "
                "humans since the invasion, both technologically and biologically."
            )

        elif choice == "3":
            print(
                "The prisoner reveals that the alien scientist was conducting experiments "
                "on humans to create hybrid creatures for the aliens. He thanks you for "
                "your assistance, saying he was next."
            )

        elif choice == "4":
            print(
                "The prisoner recounts that a few weeks after the laser scorched the Earth, "
                "a massive ship from space landed and started terraforming. The area around "
                "the landing site became unbreathable for humans without proper equipment. "
                "If you see their flora, turn around."
            )

        elif choice == "5":
            return
def hospital_first_floor(player):
    while True:
        print("you get up the stairs and see 2 room, a flower pot and a trash can")
        print("1)Go to the room and de left")
        print("2)Go to the room and the right")
        print("3)Inspect the flower pot")
        print("4)Inspect the trash can")
        print("I)Open inventory")
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            Hospital_first_floor_left_room(player)
            return
        elif choice == "2":
            Hospital_first_floor_right_room(player)
            return
        elif choice == "3":
            Hospital_flower_pot(player)
        elif choice == "4" :
            if player.get("hospital_trash_pot_check", False):
                print("You search through the trash and find some coins.")
                player["inventory"].extend(["coin", "coin", "coin"])
                player["hospital_trash_pot_check"] = True
        else:
            print("Invalid choice")
                          
def Hospital_flower_pot(player):

    while True:
        if player.get("hospital_flower_pot_checked", False):
            if skill_check(player, "perception", 30):
                print("Something feels off about a neat little flower pot in the middle of an alien-infested hospital.")
                print("3) Shoot the flower!")

        print("1) Check the flower pot")
        print("2) Go back")
        print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            print("You carefully examine the flower pot...")
            print("Suddenly, a tentacle lashes out!")
            alien = {"health": 3, "hit_chance": 70, "xp": 0}
            fight_enemy(player, alien)
            player["hospital_flower_pot_checked"] = True
            return

        elif choice == "3" and player.get("hospital_flower_pot_checked", False):
            print("You attack the flower pot before it can react. It dies instantly.")
            player["hospital_flower_pot_checked"] = True
            return

        elif choice == "2":
            return

        else:
            print("Invalid choice.")
def Hospital_first_floor_left_room(player):
    while True:
        print("You enter the room on the left. You see a desk with an old PC. It looks like it still works.")

        # PC NOT hacked yet
        if not player.get("hospital_pc_hacked", False):
            print("1) Try to hack the PC")
            print("2) Go back")
            print("I) Open inventory")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                if skill_check(player, "intelligence", 20):
                    player["hospital_pc_hacked"] = True
                    print("You successfully hack through the PC defenses.")
                else:
                    print("The PC defenses are too complex.")
            elif choice == "2":
                return
            else:
                print("Invalid choice")

        # PC hacked
        else:
            print("1) Read first message")
            print("2) Read second message")
            print("3) Unlock the desk safe")
            print("4) Go back")
            print("I) Open inventory")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "01/01/2000\n\n"
                    "Hey Millie, I hope you're doing well. The hospital is full of the usual "
                    "New Year missing fingers and drunk fools. I think I'll have to work all night."
                )

            elif choice == "2":
                print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "02/01/2000\n\n"
                    "God, Millie, what was that? A bright flash and most of everything wiped out. "
                    "The grid shut down, all patients on life support were lost. "
                    "I heard millions died. I hope you're alright. Please answer me."
                )

            elif choice == "3":
                if not player.get("has_taken_hospital_pc_safe", False):
                    print("You unlock the safe and find some ammo and a medkit.")
                    player["inventory"].append("revolver_ammo")
                    player["inventory"].append("medkit")
                    player["has_taken_hospital_pc_safe"] = True
                else:
                    print("The safe is empty.")

            elif choice == "4":
                return
            else:
                print("Invalid choice")
def Hospital_first_floor_right_room(player):
    while True:
        print("you enter the room on the right"
              "there nothig to see")
        print("1)Go back")
        print("I)Open inventory")
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            return 

        
