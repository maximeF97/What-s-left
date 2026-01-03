from unittest import result
from systems import gain_xp, handle_global_input, get_choice
from Player import skill_check
from combat import combats
import random
from inventory import use_item, add_item,remove_item
from enemis import get_enemy

def old_bunker(player):
    while True:
        print(
            "You are in an old bunker. You see a dusty table with the items\n"
            "of your fallen friend resting on it."
        )
        print("1) Inspect the table")
        print("2) Open the door")
        print("3) Go back")
        print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("bunker_items_taken", False):
                print("You find a rusty_knife and an old key.")
                add_item(player, "rusty_knife", 1)
                add_item(player, "old_key", 1)
                player["bunker_items_taken"] = True
                print("Items added to your inventory.")
            else:
                print("The table is empty.")

        elif choice == "2":
            if "old_key" in player["inventory"]:
                print(
                    "You use the old key to unlock the door and step outside\n"
                    "into the wasteland."
                )
                player["bunker_door_unlocked"] = True
                wasteland(player)
                return
            else:
                print("The door is locked. You need a key.")

        elif choice == "3":
            return

        else:
            print("Invalid choice.")


def new_func():
    choice = input("> ")
    return choice

def fight_enemy(player, enemy):
    result = combats(player, enemy)

    if result["result"] == "win":
        gain_xp(player, result["xp"])
        return "win"

    if result["result"] == "run":
        return "run"

    if result["result"] == "lose":
        print("Game over.")
        exit()


def wasteland(player):
    while True:
        print("You take your first steps into the wasteland.")
        print("Everything is desolate and quiet... when suddenly you hear a shivering noise behind you.")

        if not player.get("has_seen_alien", False):
            print("A small alien creature stands in the distance, watching you with curious eyes.")

        print("\nWhat do you want to do?")
        print("1) Approach the alien with your rusty knife  [Stealth / Luck]")
        print("2) Keep your distance and observe            [Perception]")
        print("3) Run away                                  [Stamina / Luck]")
        print("I) Open inventory")

        choice = get_choice()

        # Global inputs (I/S/L etc.)
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            # Must have a weapon
            if "rusty_knife" not in player["inventory"] and player.get("weapon") != "rusty_knife":
                print("You have nothing to fight with.")
                return

            alien = {"health": 6, "hit_chance": 60, "xp": 10}

            
            try:
                # If your systems.skill_check signature differs, adapt this call accordingly
                if skill_check(player, "stealth", 25):
                    print("You move silently. The alien doesn’t notice until it's too late — you strike first!")
                    alien["health"] = max(1, alien["health"] - 2)  
                else:
                    print("You step forward, but the alien spots you. No advantage.")
            except Exception:
                # Fallback if skill_check isn't available here
                pass

            outcome = fight_enemy(player, alien)

            if outcome == "win":
                # Reward and progression
                print("You defeated the alien and find some coins.")
                # A little luck can improve the haul
                extra = 0
                try:
                    if skill_check(player, "luck", difficulty=40):
                        extra = random.randint(1, 3)
                except Exception:
                    # fallback using raw luck value
                    extra = 1 if player.get("skills", {}).get("luck", 1) >= 3 and random.random() < 0.5 else 0

                add_item(player, "coin", 3 + extra)
                gain_xp(player, alien["xp"])
                player["has_seen_alien"] = True
                print("You continue forward...")
                wasteland_2(player)
                return

            elif outcome == "run":
                print("You escaped.")
                old_bunker(player)
                return

        elif choice == "2":
            # Perception check to learn more or avoid a fight
            try:
                if skill_check(player, "perception", 20):
                    print("You keep your distance and observe carefully. The creature seems harmless and eventually wanders away.")
                    print("it feel like it was studying you before leaving")
                else:
                    print("You watch from afar, but miss subtle details. The creature eventually leaves.")
            except Exception:
                print("You keep your distance and observe. The creature seems harmless and eventually walks away.")

            print("You survived for now...")
            player["has_seen_alien"] = True
            wasteland_2(player)
            return

        elif choice == "3":
            # Stamina/luck can help you get away cleanly
            clean_escape = False
            try:
                # Slightly easier check — running is a simpler task
                if skill_check(player, "stamina", difficulty=40) or skill_check(player, "luck", difficulty=35):
                    clean_escape = True
            except Exception:
                
                stam = player.get("skills", {}).get("stamina", 1)
                luck = player.get("skills", {}).get("luck", 1)
                clean_escape = (stam + luck + random.randint(0, 3)) >= 5

            if clean_escape:
                print("You run — fast and low. You get away without a scratch.")
            else:
                print("You run away, but trip over a broken slab and injure yourself, losing 1 health.")
                player["health"] = max(0, player["health"] - 1)
                print(f"Your health is now {player['health']}")

            print("You survived for now...")
            return

        else:
            print("Invalid choice")
def wasteland_2(player):
    print("you move forward and see a body on the ground what do you do")
    while True:
        print("1) inspect the body")
        print("2) move forward")
        print("3) go back")
        print("I) Open inventory")
        choice = get_choice()

        
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("wasteland_2_body_looted", False):
                if skill_check(player, "perception", 40):
                    print("\nYou notice claw marks around the body.")
                    gain_xp(player,10)

                print(" you inspect the body and find a note and a few coins")
                add_item(player,"coin", 3)
                add_item(player,"wasteland_2_note", 1)
                print(
                    "They’re everywhere.\n"
                    "I don’t know when it started.\n\n"
                    "They don’t always look alien.\n"
                    "Sometimes they look… familiar.\n\n"
                    "If you’re reading this,\n"
                    "don’t trust what you see.\n"
                    "Don’t sleep."
                )
                player["wasteland_2_body_looted"] = True
            else:
                print("you already took everything from him")
        elif choice == "2":
            wasteland_cross_road(player)
            return
        elif choice == "3": 
            wasteland(player)
            return
        else:
            print("incorect choice")
def wasteland_cross_road(player):
    print("you arrived at a a crossroad you see and old post with two signs.")
    while True:
        print("1) follow the sign to the left 'grove_town'")
        print("2) follow the sign to the right 'hospital'")
        print("3) you dont trust signs and walk straight ahead into the wasteland")
        print("4) go back ")
        print("I) Open inventory")
        print("S) Save game")
        print("L) Load game")

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
            wasteland_3(player)
            return
        elif choice == "4":
            return
        else:
            print("invalid choice")
def grove_town(player):
    print("you arrived at grove_town, nothing remains but the ruins of a police station and a few burned down houses.")
    while True:
        print("1) explore the police station")
        print("2) explore the burned down houses")
        print("3) go back to the crossroad")
        print("4) move forward")
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
        elif choice =="4":
            montain_tunel(player)
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
            print("You defeat the alien and find supplies and the key to the police station.")
            add_item(player,"revolver", 1)
            add_item(player,"revolver_ammo", 3)
            add_item(player,"police_station_key",1)
            gain_xp(player, 15)  # bonus XP

        elif result["result"] == "lose":
            exit()
    else:
        print("Just an empty desk and dead alien")


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
                print("You defeated the alien prisoner and find a weid looking key.")
                add_item(player,"hospital_safe_key", 1)
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
    print("your using the police station key to unlock the door")
    print("You find ammo and a medkit.")
    add_item(player,"revolver_ammo", 4)
    add_item(player,"medkit",1)
    add_item(player,"grovetown_note_2",1)
    print(
        "The humanoids don’t hunt like animals.\n"
        "They set traps.\n"
        "They wait.\n\n"
        "One of them watched me eat.\n"
        "Like it was studying how."
    )
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
        print("S) Save game")
        print("L) Load game")

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
        print("1) Sneak past the cactus")
        print("2) Shoot the cactus with your revolver")
        print("3) Go back to the hospital entrance")
        print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        # 🥷 Sneak
        if choice == "1":
            print(
                "The paranoia of the metamorph wasteland gets to you.\n"
                "You try to sneak past the suspicious cactus."
            )

            if skill_check(player, "stealth", 50):
                print("You slip past unnoticed.")
            else:
                print(
                    "Your heart races… but nothing happens.\n"
                    "It was just a cactus."
                )

            hospital_inside(player)
            return

        # 🔫 Shoot cactus
        elif choice == "2":
            if "revolver" not in player["inventory"]:
                print("You don't have a revolver.")
                continue

            if player.get("has_killed_cactus", False):
                print("The cactus is already dead. Truly dead.")
                continue

            if not remove_item(player, "revolver_ammo", 1):
                print("Click! You're out of ammo.")
                continue

            print(
                "You fire a shot.\n"
                "The cactus explodes into splinters.\n\n"
                "…It was just a plant."
            )

            player["has_killed_cactus"] = True
            hospital_inside(player)
            return

        # 🔙 Go back
        elif choice == "3":
            print("You step away from the side entrance.")
            hospital(player)
            return

        else:
            print("Invalid choice.")


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
                    add_item(player, "medkit",1)
                    add_item(player, "healing_salve",1)
                    add_item(player, "alien_laser_rifle",1)
                    add_item(player, "alien_energy_cell",1)
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
                add_item(player, "bobby_pins", 3)
                player["has_hospital_left_room_been_searched"] = True
                print("you pick up the bobby pins and add them to your inventory.")
                print("you take the stairs going down to the basement.")
                hospital_basement(player)
                return
            else:
                print("you take the stairs going down to the basement again.")
                hospital_basement(player)
        elif choice == "5":
            if not player.get("has_opened_hospital_back_door", False):
                if "hospital_back_door_key" in player["inventory"]:
                    print("You use the key and step out toward the wasteland.")
                    player["has_opened_hospital_back_door"] = True
                    wasteland_4(player)
                    return
                else:
                    print("The door is locked. You need a key.")
            else:
                print("The back door is already open.")

        elif choice == "6":
            print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            print("Invalid choice")
def scavenger_room(player):
    while True:
        if player.get("hospital_scavenger_killed", False):
            print("You enter the room again. The scavenger lies motionless. Whatever it was, it's dead.")
            return

        print(
            "You enter the room ahead to find the remains of a scavenger.\n"
            "You notice some pieces of his head have been altered with strange alien technology."
        )

        if skill_check(player, "perception", 20):
            print("You see a red light blinking on the scavenger's head, indicating active alien tech.")
        else:
            print("You don't notice anything unusual apart from the scavenger's head.")

        print("1) Search the body")
        print("2) Shoot the body with your revolver, just to be sure")
        print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # --- SEARCH BODY ---
        if choice == "1":
            print("The scavenger suddenly reanimates as a hostile alien cyborg!")

            cyborg = {
                "health": 11,
                "hit_chance": 70,
                "damage": 3,
                "xp": 80
            }

            result = combats(player, cyborg)
            if result["result"] == "win":
                gain_xp(player, cyborg["xp"])
                player["hospital_scavenger_killed"] = True
                add_item(player, "alien_implant", 1)
                print("You defeated the alien cyborg scavenger.")
                return
            else:
                exit()

        # --- SHOOT BODY ---
        elif choice == "2":
            if player.get("weapon") != "revolver":
                print("You don't have a revolver.")
                continue

            if not remove_item(player, "revolver_ammo", 1):
                print("Click! You're out of ammo.")
                continue

            if skill_check(player, "luck", 17):
                print(
                    "You fire a precise shot. The scavenger awakens badly damaged and attacks!"
                )
                cyborg = {
                    "health": 4,
                    "hit_chance": 70,
                    "damage": 3,
                    "xp": 80
                }
            else:
                print(
                    "You miss! The scavenger awakens fully and attacks!"
                )
                cyborg = {
                    "health": 11,
                    "hit_chance": 70,
                    "damage": 3,
                    "xp": 80
                }

            result = combats(player, cyborg)
            if result["result"] == "win":
                gain_xp(player, cyborg["xp"])
                player["hospital_scavenger_killed"] = True
                add_item(player, "alien_implant", 1)
                print("You defeated the alien cyborg scavenger.")
                return
            else:
                exit()

        else:
            print("Invalid choice.")

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
            if not remove_item(player, "revolver_ammo", 1):
                print("Click! You're out of ammo.")

            print("you sneak and shoot the chair for critical dammage whitch killed the alien metamorph")
            player["hospital_metamorph_killed"] = True
            add_item(player,"healing_salve", 1)

            gain_xp(player, 50)
            
            return
        elif choice == "2":
            print("you aproach the chair and the alien metamorph attacks you!")
            alien = {"health": 10, "hit_chance": 75, "xp": 70}
            result = combats(player, alien)

            if result["result"] == "win":
                gain_xp(player, result["xp"])
                add_item(player, "healing_salve", 1)
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
        print("S) Save game")
        print("L) Load game")


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

    
    add_item(player, "second_hospital_safe_key", 1)
    add_item(player, "alien_scientist_suit", 1)
    add_item(player, "hospital_back_door_key", 1)
    

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
                add_item(player, "map_to_base",1)
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
                add_item(player, "coin",3)
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
                    add_item(player, "revolver_ammo", 3)
                    add_item(player, "medkit", 1)
                    player["has_taken_hospital_pc_safe"] = True
                else:
                    print("The safe is empty.")

            elif choice == "4":
                return
            else:
                print("Invalid choice")
def Hospital_first_floor_right_room(player):
    while True:
        print("You enter the room on the right.\n"
            "There is a note lying on the floor.")
        print("1)read the note")
        print("2)Go back")
        print("I)Open inventory")
        print("S) Save game")
        print("L) Load game")

        choice = get_choice()  

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("Hospital_first_floor_right_room_note_taken", False):
                add_item(player, "hospital_note_doctor", 1)
                player["Hospital_first_floor_right_room_note_taken"] = True
                print("you pick up the note")
                print(
                    "The handwriting is shaky.\n\n"
                    "They can’t breathe our air.\n"
                    "That’s why they don’t stay long.\n\n"
                    "The small ones don’t mind.\n"
                    "They belong here now."
                        )           
            else:
                print("nothing else to do here")
        elif choice == "2":
            return 
def wasteland_3(player):
    print(
        "You arrive at an empty camp. You see a fire still hot\n"
        "and an old bedroll open on the floor."
    )

    while True:
        print("\nWhat do you do?")
        print("1) Look at the fire")
        print("2) Move forward")
        print("3) Look under the bedroll")
        print("4) Go back")
        print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            print(
                "You come near the fire. You see fresh footprints, they look human.\n"
                "Better not stay here too long."
            )
            continue

        elif choice == "2":
            print("You proceed forward.")
            wastland_stranger_encounter(player)
            return

        elif choice == "3":
            if player.get("looted_the_bedroll", False):
                print("You already took everything that was here.")
                continue

            if skill_check(player, "scavenging", 30):
                print(
                    "Your scavenging experience reminds you that people often bury valuables\n"
                    "under their bedroll."
                )
                print(
                    "You dig under the bedroll and find a sharpened kitchen knife\n"
                    "and some revolver ammo."
                )
                add_item(player, "sharp_kitchen_knife", 1)
                add_item(player, "revolver_ammo", 1)
                add_item(player, "bobby_pin", 1)
                player["looted_the_bedroll"] = True
            else:
                print("You search around but fail to find anything useful.")

        elif choice == "4":
            wasteland_cross_road(player)
            return

        else:
            print("Invalid choice.")
def wastland_stranger_encounter(player):

    
    print(
        "As you walk away from the camp, a silhouette appears on the horizon.\n"
        "A tall figure. Long coat.\n"
        "An absurdly perfect cowboy hat.\n"
        "It’s coming straight toward you."
    )

    while True:
        if not player.get("met_wasteland_stranger_near_farm", False):
            print("1) Walk toward the stranger")
            print("2) Shoot first")
            print("3) Go back")
            print("I) Open inventory")
            print("S) Save game")
            print("L) Load game")

            choice = get_choice()

            if handle_global_input(choice, player):
                continue

            if choice == "1":
                print(
                    "You step forward.\n"
                    "The stranger freezes.\n\n"
                    "His hand moves to his gun.\n"
                    "\"HOW DO I KNOW YOU’RE NOT ONE OF THEM?\""
                )
                player["met_wasteland_stranger_near_farm"] = True
                wasteland_stranger_encounter_dialogue(player)
                return

            elif choice == "2":
                player["met_wasteland_stranger_near_farm"] = True
                player["wasteland_stranger_near_farm_alive:"] = True
                if skill_check(player, "luck", 20):
                    print(
                        "You fire first.\n"
                        "The shot echoes across the wasteland.\n"
                        "The stranger got hit right in the chest."
                    )
                    cowboy = {
                        "health": 6,
                        "hit_chance": 80,
                        "damage": 4,
                        "xp": 10
                    }
                else:
                    print(
                        "Your shot goes wide.\n"
                        "The stranger smiles.\n"
                        "Then he draws."
                    )
                    cowboy = {
                        "health": 16,
                        "hit_chance": 80,
                        "damage": 4,
                        "xp": 10
                    }

                won = fight_enemy(player, cowboy)

                if won:
                    print(
                        "The gunfight ends.\n"
                        "The wasteland grows quiet again.\n\n"
                        "You take the cowboy hat.\n"
                        "Inside his coat, you find a note."
                    )
                    print("note:\n"
                        "There are two kinds.\n"
                        "I’m sure of it now.\n\n"
                        "The small ones mimic shapes.\n"
                        "Animals. Objects. Trash.\n\n"
                        "The tall ones mimic *us*."
                    )

                    add_item(player, "revolver_ammo", 6)
                    add_item(player, "cowboy_hat", 1)
                    add_item(player, "grovetown_note_1", 1)

                    old_farm_house(player)
                    return
                else:
                    print("You barely escape with your life.")
                    wasteland_3(player)
                    return

            elif choice == "3":
                
                print(
                    "You take a step back.\n"
                    "Then another.\n\n"
                    "The stranger doesn’t chase.\n\n"
                    "*BANG*\n\n"
                    "Pain explodes in your back.\n"
                    "You collapse into the dust.\n\n"
                    "Somewhere behind you, a voice mutters:\n"
                    "\"Cowards don’t live long in this part.\"\n\n"
                    "Your vision fades.\n"
                    "GAME OVER."
                )
                exit()


            else:
                print("Invalid choice.")

        else:
            print(
                "You turn away from the meeting place.\n"
                "The mountains loom ahead.\n"
                "Whatever that was… it’s behind you now."
            )
            old_farm_house(player)
            return

def old_farm_house(player):
    print(
        "You arrive at an old farmhouse.\n"
        "A chilling noise echoes from inside."
    )

    while True:
        print("\nWhat do you do?")
        print("1) Enter the house")
        print("2) Go back")

        if "map_to_base" in player.get("inventory", {}):
            print("3) Go behind the house to the mountain base marked on the map")

        print("I) Open inventory")
        print("S) Save game")
        print("L) Load game")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("visited_old_farm_house"):
                print("The wind pushes the door slightly open… then slams it shut.\n"
                      "you take a deep breath and")
                player["visited_old_farm_house"] = True

            print("You step inside the farmhouse...")
            farm_house_inside(player)
            return

        elif choice == "2":
            return

        elif choice == "3" and "map_to_base" in player.get("inventory", {}):
            survivor_montain_base(player)
            return

        else:
            print("Invalid choice.")
def farm_house_inside(player):
        
        

def wasteland_stranger_encounter_dialogue(player):
    print(
        "You stare down the stranger.\n"
        "Gun in hand, both of you trying to see humanity in the other's eyes."
    )

    while True:
        if player.get("met_wasteland_stranger_near_farm", False):
            print("The stranger has spoken before. His grip tightens on the gun.")

        print("\nWhat do you do?")
        print("1) Try to calm things down")
        print("2) Look for details that might prove he is an alien")
        print("3) Say all you really want is his hat (attack)")
        print("4) Go back")
        print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        # ---- OPTION 1 : CHARISMA ----
        if choice == "1":
            if skill_check(player, "charisma", 25):
                gain_xp(player, 10)

                print(
                    "After a long pause and many compliments about his hat, the stranger relaxes.\n"
                    "He tells you to turn back, nothing ahead but an old farmhouse full of mutated creatures.\n"
                    "Before leaving, he hands you a folded note.\n"
                    "“Keep your eyes on the horizon,” he says."
                )

                add_item(player, "grovetown_note_1", 1)

                print(
                    "\nNOTE:\n"
                    "There are two kinds.\n"
                    "I’m sure of it now.\n\n"
                    "The small ones mimic shapes.\n"
                    "Animals. Objects. Trash.\n\n"
                    "The tall ones mimic *us*."
                )

                player["met_wasteland_stranger_near_farm"] = True
                player["wasteland_stranger_near_farm_alive"] = True
                return

            else:
                print(
                    "Your words fail.\n"
                    "The stranger’s eyes narrow.\n"
                    "His finger tightens on the trigger."
                )

                player["met_wasteland_stranger_near_farm"] = True
                player["wasteland_stranger_near_farm_alive"] = True

                cowboy = get_enemy("wasteland_cowboy")
                won = fight_enemy(player, cowboy)

                if won:
                    loot_cowboy(player)
                return

        # ---- OPTION 2 : PERCEPTION ----
        elif choice == "2":
            if skill_check(player, "perception", 22):
                gain_xp(player, 10)
                print(
                    "You study him closely.\n"
                    "Nothing stands out.\n"
                    "If he’s something else… he hides it well."
                )
            else:
                print(
                    "You try to see beneath the layers of dust and clothing.\n"
                    "You can’t tell what he is.\n"
                    "And that’s the worst part."
                )
            return

        # ---- OPTION 3 : ATTACK ----
        elif choice == "3":
            print("The fight for the hat begins.")

            player["met_wasteland_stranger_near_farm"] = True
            player["wasteland_stranger_near_farm_alive"] = True

            cowboy = get_enemy("wasteland_cowboy")
            won = fight_enemy(player, cowboy)

            if won:
                loot_cowboy(player)
            return

        # ---- OPTION 4 : LEAVE ----
        elif choice == "4":
            return

        else:
            print("Invalid choice.")
def loot_cowboy(player):
    print(
        "The gunfight ends.\n"
        "The wasteland grows quiet again.\n\n"
        "You take the cowboy hat.\n"
        "Inside his coat, you find a note."
    )

    print(
        "\nNOTE:\n"
        "There are two kinds.\n"
        "I’m sure of it now.\n\n"
        "The small ones mimic shapes.\n"
        "Animals. Objects. Trash.\n\n"
        "The tall ones mimic *us*."
    )

    add_item(player, "revolver_ammo", 6)
    add_item(player, "cowboy_hat", 1)
    add_item(player, "grovetown_note_1", 1)




def wasteland_4(player):
    print("not donne yet")
    # to do
def montain_tunel(player):
    print("you arrive at the foot of a massive montain you find a locked tunel door")
    if("montain_tunel_key") in "inventory":
        print("you use the key and move forward")
    else:
        print("the doors are locked, you need a key")
        grove_town(player)
        return