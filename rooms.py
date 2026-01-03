from unittest import result
from systems import gain_xp, handle_global_input, get_choice, randomized_bonus_loot
from Player import skill_check
from combat import combats, get_current_weapon, player_attack
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
    """
    Handles the result of combats(player, enemy).
    Supports two return shapes:
      - dict: {"result": "win"|"run"|"lose", "xp": <int>}
      - str:  "win"|"run"|"lose"  (no xp)
    """
    outcome = combats(player, enemy)

    # Normalize outcome to (result, xp)
    if isinstance(outcome, dict):
        result = outcome.get("result")
        xp = int(outcome.get("xp", 0)) if outcome.get("xp") is not None else 0
    else:
        result = outcome
        xp = 0

    if result == "win":
        # Ensure gain_xp accepts (player, xp)
        gain_xp(player, xp)
        return "win"

    if result == "run":
        return "run"

    if result == "lose":
        print("Game over.")
        # Prefer sys.exit over bare exit
        import sys
        sys.exit(0)

    # Unexpected result value
    raise ValueError(f"Unexpected combat outcome: {outcome!r}")

def wasteland(player):
    while True:
        if player.get("has_seen_alien", False):
            print("You are back in the desolate wasteland.you feel a bit safer now that you know what to expect.")
            wasteland_2(player) 
            return
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
                randomized_bonus_loot(player, {"medkit": (1,2), "healing_salve": (1,3), "bobby_pins": (2,5)})
                
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
            hospital_road(player)
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
    randomized_bonus_loot(player, {"revolver_ammo": (1,2), "healing_salve": (1,3), "coin": (2,5)})
    remove_item(player,"police_station_key", 1)
    print("the note reads:\n\n"
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
        if skill_check(player, "scavenging", 30):
            gain_xp(player, 10)
            print("you find a note under the rubble")
            add_item(player,"wasteland_note_small_1", 1)
            print("Saw one near the ruins.\n"
                    "Small. Fast. Curious.\n\n"
                    "It didn’t attack.\n"
                    "Just watched.\n"
                    "Like an animal.\n\n")

    else:
        print("nothing else of interest here")
    
def hospital_road(player):
    print("You've been walking for a while and started to feel watched.")

    player.setdefault("has_pass_hospital_road_count", 0)
    player.setdefault("medkit_encounter_done", False)

    while True:
        player["has_pass_hospital_road_count"] += 1

        if (
            player["has_pass_hospital_road_count"] >= 3
            and not player["medkit_encounter_done"]
        ):
            medkit_encounter(player)
            player["medkit_encounter_done"] = True

        print("1) keep walking to the hospital")
        print("2) look around")
        print("3) go back to the crossroad")
        print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            print("you arrive at the hospital")
            hospital(player)
            return

        elif choice == "2":
            if skill_check(player, "perception", 30):
                gain_xp(player, 10)
                player["has_seen_hospital_road_alien"] = True
                print(
                    "you see something staring at you from afar\n"
                    "it quickly vanishes behind some ruins"
                )
            else:
                print("you look around but see nothing unusual")

        elif choice == "3":
            wasteland_cross_road(player)
            return

        else:
            print("Invalid choice")

def medkit_encounter(player):
    print("You see a medkit lying on the ground.")

    if player.get("has_seen_hospital_road_alien", False):
        print("You recall seeing a strange figure watching you earlier.")

    while True:
        print("1) Pick up the medkit")
        print("2) Shoot it")
        print("3) Leave it")

        choice = get_choice()

        if choice == "1":
            print("As you reach for it, a tentacle lashes out!")
            alien = get_enemy("small_metamorph")
            result = fight_enemy(player, alien)

        elif choice == "2":
            weapon_name, weapon = get_current_weapon(player)

            if not weapon or weapon["type"] != "ranged":
                print("You have no ranged weapon.")
                continue

            

            print("You shoot the medkit. Dark blood sprays everywhere!")
            alien = get_enemy("small_metamorph")
            alien["health"] -= 2
            result = fight_enemy(player, alien)

        elif choice == "3":
            print("You leave it behind. Some things aren't worth the risk.")
            return

        else:
            print("Invalid choice.")
            continue

        # --- Combat resolution ---
        if result["result"] == "win":
            gain_xp(player, result["xp"])
            print("You defeated the creature and find some coins.")
            add_item(player, "coin", 5)

            if skill_check(player, "luck", 30):
                print("Luck is on your side — you find extra coins.")
                add_item(player, "coin", 3)

            return

        elif result["result"] == "lose":
            exit()



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
            hospital_road(player)
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
            weapon_name, weapon = get_current_weapon(player)

            if not weapon or weapon["type"] != "ranged":
                print("You have no ranged weapon.")
                continue
            

            if player.get("has_killed_cactus", False):
                print("The cactus is already dead. Truly dead.")
                continue
            print("You take aim at the cactus...")

            cactus = {
                "name": "innocent cactus",
                "health": 1
            }

            player_attack(player, cactus)  
                    
            print(
                
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
        if not player.get("hospital_scavenger_killed", False):
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
        print("5)Go back downstairs")
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
            if not player.get("hospital_trash_pot_check", False):
                print("You search through the trash and find some coins.")
                add_item(player, "coin",3)
                player["hospital_trash_pot_check"] = True
            else:
                print("The trash can is empty.")
        elif choice == "5":
            print("you go back downstairs")
            hospital_inside(player)
            return
        else:
            print("Invalid choice")
                          
def Hospital_flower_pot(player):

    while True:
        if not player.get("hospital_flower_pot_checked", False):
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
            print("4) Read third message")
            print("5) Go back")
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
                print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "03/01/2000\n\n"
                    "Millie, I don't know how much longer I can hold out. "
                    "The creatures are everywhere now. They change shape, "
                    "mimicking humans. I barely escaped an attack today. "
                    "If you get this, stay away from the hospital."
                )
            elif choice == "5":
                return
            else:
                print("Invalid choice")
def Hospital_first_floor_right_room(player):
    while True:
        print("You enter the room on the right.\n")
        if not player.get("Hospital_first_floor_right_room_note_taken", False):
            print(
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
        "A cold metallic echo carries from inside, like the house is breathing."
    )

    while True:
        print("\nWhat do you do?")
        print("1) Enter the house")
        print("2) Go back")

        if "map_to_base" in player.get("inventory", {}):
            print("3) Follow the map behind the house toward the mountain base")

        print("I) Open inventory")
        print("S) Save game")
        print("L) Load game")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("visited_old_farm_house"):
                print("The wind nudges the door open… then slams it.\n"
                      "You steady your breath and push forward.")
                player["visited_old_farm_house"] = True

            print("You step inside the farmhouse...")
            farm_house_inside(player)
            return

        elif choice == "2":
            return

        elif choice == "3" and "map_to_base" in player.get("inventory", {}):
            # Make sure this function exists; the name looks like a typo.
            try:
                survivor_montain_base(player)  # or survivor_mountain_base(player)
            except NameError:
                print("The path to the mountain base is blocked — you’ll need to find another route.")
            return

        else:
            print("Invalid choice.")

def farm_house_inside(player):
    print("You enter the old farmhouse. A dark living room yawns ahead; furniture slumps under a skin of dust.")
    if skill_check(player, "perception", 30):
        print("A low growl filters down from upstairs.Better be careful.")
    while True:
        print("\n1) Go upstairs")
        print("2) Go to the kitchen")
        print("3) Go to the living room")
        print("4) Go back outside")
        print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            print("You climb. The hallway is a black throat leading to the attic.")
            farm_house_upstairs(player)
        elif choice == "2":
            print("You step into the kitchen. Old appliances sit in silence.")
            farm_house_kitchen(player)
        elif choice == "3":
            if not player.get("farm_house_living_room_unlocked", False):
                print("You reach a locked door. Through the glass, a shotgun waits on the mantle.")
                if skill_check(player, "lockpicking", 40):
                    print("You tease the tumblers. The lock yields. The living room welcomes you with dust.")
                    player["farm_house_living_room_unlocked"] = True
                    farm_house_living_room(player)
                    return
                if player.get("inventory", {}).get("old_farm_house_living_room_key", 0) > 0:
                    print("You use the living room key. The door opens with a tired click.")
                    player["farm_house_living_room_unlocked"] = True
                    # Remove one key from inventory safely
                    remove_item(player, "old_farm_house_living_room_key", 1)
                    farm_house_living_room(player)
                    return
                print("The door is stubborn — it will not open.")
            else:
                print("You enter the living room.")
                farm_house_living_room(player)
        elif choice == "4":
            print("You step back out into the yard.")
            return
        else:
            print("Invalid choice")

def farm_house_living_room(player):
    while True:
        print("The living room is dark, the air thick with dust and a faint smell of metal.")
        print("1) Examine the room")
        print("2) Go back to the kitchen")
        print("3) Go back outside")
        print("I) Open inventory")
        print("S) Save game")
        print("L) Load game")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_living_room_searched", False):
                print("You lift the shotgun from the mantle. Underneath: shells and a pair of tactical gloves.")
                add_item(player, "shotgun", 1)
                add_item(player, "shotgun_shells", 5)  
                add_item(player, "tactical_gloves", 1)
                add_item(player, "third_hospital_safe_key", 1)
                player["farm_house_living_room_searched"] = True
            else:
                print("Whatever mattered here has already been taken.")
        elif choice == "2":
            print("You return to the kitchen.")
            return
        elif choice == "3":
            print("You step back outside.")
            return
        else:
            print("Invalid choice")

def farm_house_upstairs(player):
    while True:
        print("Upstairs lies mostly in ruins. A dried corpse rests against the wall. Stairs vanish into the attic.")
        print("1) Examine the corpse")
        print("2) Go to the attic")
        print("3) Go back downstairs")
        print("I) Open inventory")
        print("S) Save game")
        print("L) Load game")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_upstairs_corpse_searched", False):
                print("You search the corpse a massive claw mark rest on his chest \n"
                       "and find some coins and a folded note.")
                add_item(player, "coin", 10)
                add_item(player, "farmer_note", 1)
                print("\nThe note reads:\n")
                print(
                    "A small, bat‑shaped thing started haunting the farm.\n"
                    "It perches on the barn roof and watches. It doesn’t blink.\n\n"
                    "It’s growing. Every night, taller—now nearly twice my size,\n"
                    "bones shifting like a bad thought. The moon shines through its wings,\n"
                    "but the shadows bend the wrong way.\n\n"
                    "It isn’t aggressive, not yet. But it looks at me like it’s practicing.\n\n"
                    "Tonight I dropped the metal sheets. The noise made it scream without sound—\n"
                    "and the attic answered. It folded itself through the rafters like smoke.\n\n"
                    "For three nights, something moves above my room, counting the floorboards,\n"
                    "learning the house by heart.\n\n"
                    "I have to get rid of it before the farm forgets it ever belonged to me."
                )
                # If you have a helper like randomized_bonus_loot, you can use it; otherwise add items directly:
                add_item(player, "revolver_ammo", random.randint(1, 2))
                add_item(player, "shotgun_shells", random.randint(1, 2))
                add_item(player, "healing_salve", 1)
                player["farm_house_upstairs_corpse_searched"] = True
            else:
                print("The poor soul has nothing else of value.")
        elif choice == "2":
            print("You climb toward the attic. The air grows thin.")
            farm_house_attic(player)
        elif choice == "3":
            print("You go back downstairs to the living room.")
            return
        else:
            print("Invalid choice")

def farm_house_attic(player):
    def build_beast(hp_bonus=0):
      
        if callable(get_enemy):
            try:
                beast = get_enemy("hell_genetically_altered_bat")
            except Exception:
                beast = {"name": "hell_genetically_altered_bat", "health": 18, "hit_chance": 70, "xp": 100}
        else:
            beast = {"name": "hell_genetically_altered_bat", "health": 18, "hit_chance": 70, "xp": 100}
        beast["health"] = max(1, int(beast.get("health", 18)) + int(hp_bonus))
        beast.setdefault("hit_chance", 70)
        beast.setdefault("xp", 100)
        return beast

    def resolve_outcome(outcome, beast):
        """
        Normalize combats outcome and apply side effects (xp, flags).
        Returns True if room flow should continue, False to return downstairs/end.
        """
        if isinstance(outcome, dict):
            result = outcome.get("result")
            xp = int(outcome.get("xp", 0) or 0)
        else:
            result = outcome
            xp = 0

        if result == "win":
            player["beast_in_farm_house_defeated"] = True
            if xp > 0:
                gain_xp(player, xp)
            attic_beast_loot(player)
            # After winning, show the post-beast attic and exit
            print("The attic is finally quiet. The dust finally settles.")
            attic_after_beast_defeated(player)
            return False
        elif result == "run":
            print("You flee back down the ladder.")
            return False
        elif result == "lose":
            print("You have been defeated.")
            import sys
            sys.exit(0)
        else:
            # Unexpected result: continue loop safely
            print(f"Unexpected combat outcome: {outcome!r}")
            return True

    while True:
        print("You enter the attic. You see shadows dancing among the beams and a legion of eyes watching you.")

        # If the beast was woken earlier and not defeated yet, it attacks immediately with a challenge bump
        if player.get("beast_in_farm_house_woken_up", False) and not player.get("beast_in_farm_house_defeated", False):
            print("The beast is awake.\nIts anger shakes the rafters. It unfolds and charges!")
            beast = build_beast(hp_bonus=10)
            outcome = combats(player, beast)
            if not resolve_outcome(outcome, beast):
                return  # win/run/lose handled

        # If not woken and not defeated, present options
        if not player.get("beast_in_farm_house_defeated", False) and not player.get("beast_in_farm_house_woken_up", False):
            print("\n1) Prepare to fight the beast")
            print("2) Try to sneak attack the beast")
            print("3) Go back downstairs")
            print("I) Open inventory")

            choice = get_choice().strip().lower()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                player["beast_in_farm_house_woken_up"] = True
                print("You brace yourself for the beast's attack!")
                beast = build_beast()
                outcome = combats(player, beast)
                if not resolve_outcome(outcome, beast):
                    return

            elif choice == "2":
                print("You try to become the dark. The beast sees you with too many eyes.")
                try:
                    # Use a stealth check; success gives you a damage edge
                    if skill_check(player, "stealth", 50):
                        print("You catch it off guard and draw blood before it screams.")
                        beast = build_beast()
                        beast["health"] = max(1, beast["health"] - 5)
                    else:
                        print("You fail to disappear; its many eyes lock onto you.")
                        beast = build_beast()
                except Exception:
                    # Fallback if skill_check errors
                    beast = build_beast()

                outcome = combats(player, beast)
                if not resolve_outcome(outcome, beast):
                    return

            elif choice == "3":
                print("You back away, the attic swallowing your footprints.")
                return
            else:
                print("Invalid choice")
                continue

        # Already defeated: show post-beast state and exit
        elif player.get("beast_in_farm_house_defeated", False):
            print("The attic is finally quiet. The dust finally settles.")
            attic_after_beast_defeated(player)
            return

        # Any other state: go to post-beast flow as a safe fallback
        else:
            attic_after_beast_defeated(player)
            return

def attic_beast_loot(player):
    gain_xp(player, 100)
    print("You deliver the final blow. A scream threads the beams and then comes apart.")
    player["beast_in_farm_house_defeated"] = True
    add_item(player, "sharp_wing_claw", 1)
    attic_after_beast_defeated(player)
    return

def attic_after_beast_defeated(player):
    while True:
        print("The bat-thing lies still, but its many eyes feel like stains.")
        print("1) Search the attic")
        print("2) Go back downstairs")
        print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_attic_searched", False):
                print("You search the attic and find shells, a medkit, a key\n" 
                      "and some weary boots on the feet of one of the many corpses.")
                add_item(player, "shotgun_shells", 3)
                add_item(player, "medkit", 1)
                add_item(player, "weary_boots", 1)
                add_item(player, "old_farm_house_living_room_key", 1)
                player["farm_house_attic_searched"] = True
            else:
                print("Nothing else whispers to you here.")
        elif choice == "2":
            print("You go back downstairs.")
            return
        else:
            print("Invalid choice")

def farm_house_kitchen(player):
    while True:
        print("The kitchen smells like old metal and cold dust.")
        print("1) Search the fridge")
        print("2) Search the oven")
        print("3) Examine the counter")
        print("4) Go back to the living room")
        print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_fridge_searched", False):
                print("You search the fridge and find canned food and a strange fruit with creeping veins.")
                add_item(player, "canned_food", 2)
                add_item(player, "weird_fruit", 1)
                player["farm_house_fridge_searched"] = True
            else:
                print("The fridge is empty.")
        elif choice == "2":
            if not player.get("farm_house_oven_searched", False):
                print("You search the oven and find revolver rounds and shotgun shells.")
                add_item(player, "revolver_ammo", 2)
                add_item(player, "shotgun_shells", 2)
                if skill_check(player, "scavenging", 30):
                    print("Behind the oven’s back, a taped box, someone didn’t want this found.")
                    add_item(player, "coin", 15)
                player["farm_house_oven_searched"] = True
            else:
                print("The oven is empty.")
        elif choice == "3":
            if not player.get("farm_house_counter_searched", False):
                print("Two identical toasters sit side by side. One of them feels wrong.")
                toaster_check(player)
                return
            else:
                print("Nothing else to do here.")
        elif choice == "4":
            return
        else:
            print("Invalid choice")

def toaster_check(player):
    if skill_check(player, "perception", 25):
        print("On the right toaster: a faint smell of decay emanates.")
    print("1) Inspect the toaster on the right")
    print("2) Inspect the toaster on the left")
    print("3) Ignore it and go back")
    print("I) Open inventory")
    choice = get_choice()
    if handle_global_input(choice, player):
        return
    if choice == "1":
        right_toaster(player)
    elif choice == "2":
        left_toaster(player)
    elif choice == "3":
        return
    else:
        print("Invalid choice")

def right_toaster(player):
    print("You inspect the toaster on the right.")

    if player.get("toaster_metamorph_dead", False):
        print("The toaster is split open. Whatever nested inside is dead.")
        return

    while True:
        print("1) Stab the toaster")
        print("2) Shoot the toaster")
        print("3) Go back")
        print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            print("You plunge your knife in. Something bleeds.")
            # Use an inline enemy if get_enemy/fight_enemy aren’t available:
            alien = {"name": "small_metamorph", "health": 6, "hit_chance": 60, "xp": 50}
            combats(player, alien)
            if player["health"] > 0 and alien["health"] <= 0:
                player["toaster_metamorph_dead"] = True
                gain_xp(player, 50)
                add_item(player, "healing_salve", 1)
                return
            else:
                print("You collapse. The house swallows the scream.")
                return

        elif choice == "2":
            # Basic ranged check: do you have any gun and its ammo?
            possible_guns = [
                ("revolver", "revolver_ammo"),
                ("shotgun", "shotgun_shells"),
                ("alien_laser_rifle", "alien_energy_cell"),
            ]
            have_ranged = False
            for gun, ammo in possible_guns:
                if player.get("inventory", {}).get(gun, 0) and player.get("inventory", {}).get(ammo, 0):
                    have_ranged = True
                    break

            if not have_ranged:
                print("You have no loaded ranged weapon.")
                continue

            print("You fire. The toaster EXPLODES. Dark matter paints the walls.")
            if not player.get("beast_in_farm_house_defeated", False):
                print("A blood-chilling scream answers from the attic. Something woke up.")
                player["beast_in_farm_house_woken_up"] = True

            alien = {"name": "small_metamorph", "health": 6, "hit_chance": 60, "xp": 50}
            combats(player, alien)
            if player["health"] > 0 and alien["health"] <= 0:
                player["toaster_metamorph_dead"] = True
                gain_xp(player, 50)
                add_item(player, "healing_salve", 1)
                return
            else:
                print("You collapse. The house swallows the scream.")
                return

        elif choice == "3":
            return

        else:
            print("Invalid choice")
def left_toaster(player):
    print("You inspect the toaster on the left. It looks normal.")
    print("After a moment, you decide to leave it alone.")  
    return
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
                old_farm_house(player)
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
                old_farm_house(player)
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