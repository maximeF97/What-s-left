from unittest import result
from systems import gain_xp, handle_global_input, get_choice, randomized_bonus_loot
from Player import skill_check
from combat import combats, get_current_weapon, player_attack,shoot_and_remove_ranged_ammo
import random
from inventory import use_item, add_item,remove_item,ITEMS
from enemis import get_enemy
from text_effect import slow_print_char, suspense_print,slow_print_word
DEMO_MODE = True



#FUNCTIONS______________
def new_func():
    choice = input("> ")
    return choice
from save_system import load_game, save_game
def game_over():
    from main import start_game
    suspense_print(
        "\nYour body stops responding.\n"
        "Pain fades first.\n"
        "Then sound.\n"
        "Then thought.\n\n"
        "Somewhere in the dark,\n"
        "something continues moving.\n\n"
        "You are no longer part of it.\n\n"
        "— GAME OVER —\n"
    )

    while True:
        suspense_print("\nWhat do you do?")
        suspense_print("1) Restart")
        suspense_print("2) Load save")
        suspense_print("3) Quit")

        choice = input("> ").strip().lower()

        if choice == "1":
            suspense_print(
                "\nTime fractures.\n"
                "Memory collapses.\n"
                "You wake up again...\n"
            )
            start_game()   # your entry point
            return

        elif choice == "2":
            suspense_print(
                "\nSearching for intact memory fragments...\n"
            )
            load_game()    # your loader
            return

        elif choice == "3":
            suspense_print(
                "\nThe signal cuts out.\n"
                "Whatever happens next...\n"
                "happens without you.\n"
            )
            exit(0)

        else:
            suspense_print("Invalid choice.")
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
        game_over()
        return "lose"

    # Unexpected result value
    raise ValueError(f"Unexpected combat outcome: {outcome!r}")
def fight_multiple_enemies(player, enemies):
    """Fight multiple enemies in sequence."""
    for i, enemy in enumerate(enemies, 1):
        suspense_print(f"Enemy {i} of {len(enemies)} attacks!")
        result = fight_enemy(player, enemy)
        if result != "win":
            return False
        if player["health"] <= 0:
            return False
    return True

#ROADS_______
def old_bunker(player):
    # Increment visit counter
    count = player.get("bunker_visite_count", 0)
    player["bunker_visite_count"] = count + 1
    if count >=10  and count <15:
        suspense_print("you see a door in the back of the bunker you swore to never have seen it before\n"
                       "a strange feeling overcomes you as you approach it")
    elif count >= 5 and count <10:
        suspense_print("you're back again a strange feeling washes over you\n"
                       "you lived here for decades yet you cant remeber a single thing about it")
    while True:
        if player.get("old_bunker_first_visit", False):
            suspense_print("You are back in the old bunker.\n"
                        "you try to remember what happened here.\n"
                        "but your mind is blank.")
        elif player.get("has_left_the_bunker", False):
            suspense_print("You are back in the old bunker,you feel tired but have to move on.")
        else:
            suspense_print(
            "You are in an old bunker. You see a dusty table with the items\n"
            "of your fallen friend resting on it."
        )
        suspense_print("1) Inspect the table")
        suspense_print("2) Open the door")
        suspense_print("3) Go back")
        if count >=10 :
            suspense_print("4) pass through the door")
       
        suspense_print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("bunker_items_taken", False):
                suspense_print("You find a rusty_knife and an old key.")
                add_item(player, "rusty_knife", 1)
                add_item(player, "old_key", 1)
                player["bunker_items_taken"] = True
                suspense_print("Items added to your inventory.")
            else:
                suspense_print("The table is empty.")

        elif choice == "2":
            if player.get("bunker_door_unlocked", False):
                suspense_print("The door is already unlocked. You step outside into the wasteland.")
                player["has_left_the_bunker"] = True
                player["old_bunker_first_visit"] = True
                wasteland(player)
                return
            elif "old_key" in player["inventory"]:
                suspense_print(
                    "You use the old key to unlock the door and step outside\n"
                    "into the wasteland."
                )
                player["bunker_door_unlocked"] = True
                player["has_left_the_bunker"] = True
                remove_item(player, "old_key", 1)
                wasteland(player)
                return
            else:
                suspense_print("The door is locked. You need a key.")

        elif choice == "3":
            return
        elif choice == "4" and count >=10 :
            behind_the_door(player)
            
            return
        else:
            suspense_print("Invalid choice.")
        
def behind_the_door(player):
    if player.get("has_taken_artifact", False):
        suspense_print("juste an empty concrete room you have no idea what was here before")
        old_bunker(player)
    suspense_print("You pass through the door and find yourself in a small room full of blood\n"
                     "but no bodies. In the center of the room is a strange alien artifact pulsating with energy\n"
                     "it calls to you"
                    )
    while True:
        suspense_print("1) inspect the alien artifact")
        suspense_print("2) leave the room")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("as you approach the artifact it emits a bright light\n"
                           "you feel a surge of energy coursing through your body\n"
                           "your vision blurs and the artifact suddenly vanishes with the voices\n"
                           "your mind feels sharper your reflexes quicker\n"
                           "you have gained +1 intelligence and +1 stamina")
            player["skills"]["intelligence"] +=1
            player["skills"]["stamina"] +=1
            player["has_taken_artifact"] = True
            old_bunker(player)
            return
        elif choice == "2":
            suspense_print("you trye to leave but the voice gets louder\n"
                           "it says you cannot leave yet")
            continue
        else:
            suspense_print("Invalid choice.")
            
def wasteland(player):
    while True:
        if player.get("has_seen_alien", False):
            suspense_print("You are back in the desolate wasteland.you feel a bit safer now that you know what to expect.")
            wasteland_2(player) 
            return
        suspense_print("You take your first steps into the wasteland.")
        suspense_print("Everything is desolate and quiet... when suddenly you hear a shivering noise behind you.")

        if not player.get("has_seen_alien", False):
            suspense_print("A small alien creature stands in the distance, watching you with curious eyes.")

        suspense_print("\nWhat do you want to do?")
        suspense_print("1) Approach the alien with your rusty knife  [Stealth / Luck]")
        suspense_print("2) Keep your distance and observe            [Perception]")
        suspense_print("3) Run away                                  [Stamina / Luck]")
        suspense_print("I) Open inventory")

        choice = get_choice()

        # Global inputs (I/S/L etc.)
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            # Must have a weapon
            if "rusty_knife" not in player["inventory"] and player.get("weapon") != "rusty_knife":
                suspense_print("You have nothing to fight with.")
                return

            alien = {"health": 6, "hit_chance": 60, "xp": 10}

            
            try:
                # If your systems.skill_check signature differs, adapt this call accordingly
                if skill_check(player, "stealth", 25):
                    suspense_print("You move silently. The alien doesn’t notice until it's too late — you strike first!")
                    alien["health"] = max(1, alien["health"] - 2)  
                else:
                    suspense_print("You step forward, but the alien spots you. No advantage.")
            except Exception:
                # Fallback if skill_check isn't available here
                pass

            outcome = fight_enemy(player, alien)

            if outcome == "win":
                # Reward and progression
                suspense_print("You defeated the alien and find some coins.")
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
                suspense_print("You continue forward...")
                wasteland_2(player)
                return

            elif outcome == "run":
                suspense_print("You escaped.")
                old_bunker(player)
                return

        elif choice == "2":
            # Perception check to learn more or avoid a fight
            try:
                if skill_check(player, "perception", 20):
                    suspense_print("You keep your distance and observe carefully. The creature seems harmless and eventually wanders away.")
                    suspense_print("it feel like it was studying you before leaving")
                else:
                    suspense_print("You watch from afar, but miss subtle details. The creature eventually leaves.")
            except Exception:
                suspense_print("You keep your distance and observe. The creature seems harmless and eventually walks away.")

            suspense_print("You survived for now...")
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
                suspense_print("You run — fast and low. You get away without a scratch.")
            else:
                suspense_print("You run away, but trip over a broken slab and injure yourself, losing 1 health.")
                player["health"] = max(0, player["health"] - 1)
                suspense_print(f"Your health is now {player['health']}")

            suspense_print("You survived for now...")
            return

        else:
            suspense_print("Invalid choice")
def wasteland_2(player):
    # Increment counter at start
    count = player.get("has_passed_wasteland_2_count", 0)
    player["has_passed_wasteland_2_count"] = count + 1
    
    if player.get("wasteland_2_shroom_man_killed", False):
        suspense_print("You pass by the area where you encountered the shroom man, but it's eerily quiet now.")
    
    if count >= 10 and not player.get("wasteland_2_shroom_man_killed", False):
        shroom_man_encounter(player)
        return
    
    # ... rest of function, but REMOVE the increment lines at choices 2 and 3
    # Show progression messages based on visit count
    if count <= 2:
        # First visit
        suspense_print("you move forward and see a body on the ground what do you do")
    elif count >= 1 and count <= 6:
        if player.get("wasteland_2_body_looted", False):
            suspense_print("You passed near the body you found earlier, it seems unchanged.")
        else:
            suspense_print("you move forward and see a body on the ground what do you do")
    elif count >= 6 and count < 10:
        suspense_print("weird growths start to develop on the body you found earlier, you feel uneasy")
    
    # Main interaction loop
    while True:
        suspense_print("1) inspect the body")
        suspense_print("2) move forward")
        suspense_print("3) go back")
        suspense_print("I) Open inventory")
        choice = get_choice()

        if handle_global_input(choice, player):
            continue
            
        if choice == "1":
            if not player.get("wasteland_2_body_looted", False):
                if skill_check(player, "perception", 40):
                    suspense_print("\nYou notice claw marks around the body.")
                    gain_xp(player, 10)

                suspense_print("you inspect the body and find a note and a few coins")
                add_item(player, "coin", 3)
                add_item(player, "wasteland_2_note", 1)
                randomized_bonus_loot(player, {"medkit": (1,2), "healing_salve": (1,3), "bobby_pins": (2,5)})
                
                suspense_print(
                    "I lost my weapon in town\n"
                    "They were everywhere.\n"
                    "I don't know when it started.\n\n"
                    "They don't always look alien.\n"
                    "Sometimes they look… familiar.\n\n"
                    "If you're reading this,\n"
                    "don't trust what you see.\n"
                    "Don't sleep."

                )
                player["wasteland_2_body_looted"] = True
            else:
                suspense_print("you already took everything from him")
                
        elif choice == "2":
            
            wasteland_cross_road(player)
            return
            
        elif choice == "3": 
            
            wasteland(player)
            return
            
        else:
            suspense_print("incorrect choice")
def shroom_man_encounter(player):
    suspense_print("As you pass by the body again, you see it standing up staring at the sky,it has strange mushroom like growths all over its body.")
    while True:
        suspense_print("1) approach the shroom man")
        suspense_print("2) sneak passt it and move forward")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("you approach the shroom man weapon in arms")
            shroom_man = get_enemy("sporebound_slave")
            result = fight_enemy(player, shroom_man)
            if result == "win":
                suspense_print("you defeated the shroom man")
                gain_xp(player, 50)
                player["wasteland_2_shroom_man_killed"] = True
                return
            else:
                game_over()
            return
        elif choice == "2":
            if skill_check(player, "stealth", 40):
                suspense_print("you sneak past the shroom man unnoticed")
                return
            else:
                suspense_print("as you ty to sneek behind him his head snaps around and sees you\n"
                                "you have to fight him")
                shroom_man = get_enemy("sporebound_slave")
                result = fight_enemy(player, shroom_man)
                if result == "win":
                    suspense_print("you defeated the shroom man")
                    gain_xp(player, 50)
                    player["wasteland_2_shroom_man_killed"] = True
                    return
                else:
                    game_over()
                return
        else:
            suspense_print("invalid choice")  
def wasteland_cross_road(player):
    suspense_print("you arrived at a a crossroad you see and old post with two signs.")
    while True:
        suspense_print("1) follow the sign to the left 'grove_town'")
        suspense_print("2) follow the sign to the right 'hospital'")
        suspense_print("3) you dont trust signs and walk straight ahead into the wasteland")
        suspense_print("4) go back ")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")

        choice = get_choice()

        
        if handle_global_input(choice, player):
            continue
        
        if choice == "1":
            suspense_print("you follow the sign to grove_town")
            grove_town(player)
            return
        elif choice == "2":
            suspense_print("you follow the sign to the hospital")
            hospital_road(player)
            return
        elif choice == "3":
            suspense_print("you walk straight ahead into the wasteland")
            wasteland_3(player)
            return
        elif choice == "4":
            return
        else:
            suspense_print("invalid choice")

#GROVE_TOWN_ARC
def grove_town(player):
    suspense_print("you arrived at grove_town, nothing remains but the ruins of a police station and a few burned down houses.")
    while True:
        suspense_print("1) explore the police station")
        suspense_print("2) explore the burned down houses")
        suspense_print("3) go back to the crossroad")
        suspense_print("4) move forward")
        suspense_print("I) Open inventory")

        choice = get_choice()

        
        if handle_global_input(choice, player):
            continue
        
        if choice == "1":
            police_station(player)
        elif choice == "2":
            burned_houses(player)
        elif choice == "3":
            suspense_print("you go back to the crossroad")
            wasteland_cross_road(player)
            return
        elif choice =="4":
            mountain_tunnel(player)
            return
                
        else:
            suspense_print("Invalid choice")
def police_station(player):
    if not player.get("has_seen_police_station_alien", False):
        suspense_print("\nYou are inside the ruined police station you see something moving to a other room but when you go there you only see a mug on a desk.")
    else:
        suspense_print("\nYou are back inside the police station.")
    while True:

        suspense_print("1) Inspect the desk")
        suspense_print("2) Explore the cells")
        suspense_print("3) Enter the evidence room")
        suspense_print("4) Leave the police station")
        suspense_print("I) Open inventory")
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
            suspense_print("You leave the police station.")
            return

        else:
            suspense_print("Invalid choice.")
def inspect_desk(player):
    if not player.get("has_seen_police_station_alien", False):
        suspense_print("The mug suddenly transforms into a small alien!")

        alien = {"health": 4, "hit_chance": 65, "xp": 25}
        result = combats(player, alien)

        player["has_seen_police_station_alien"] = True

        if result["result"] == "win":
            gain_xp(player, result["xp"])
            suspense_print("You defeat the alien and find supplies and the key to the police station.")
            add_item(player,"revolver", 1)
            add_item(player,"revolver_ammo", 3)
            add_item(player,"police_station_key",1)
            gain_xp(player, 15)  # bonus XP

        elif result["result"] == "lose":
            exit()
    else:
        suspense_print("Just an empty desk and dead alien")
def explore_cells(player):
    while True:
        if player["has_freed_police_station_prisoner"]:
            suspense_print("The cells are empty.")
            return

        suspense_print("A man is locked in a cell. A note reads: 'Do not free him. He is an alien.'")
        suspense_print("1) Free him")
        suspense_print("2) Leave him")
        suspense_print("I) Open inventory")

        choice = get_choice()

            
        if handle_global_input(choice, player):
            continue



        if choice == "1":
            suspense_print("The prisoner transforms into a large hostile alien!")

            alien = {"health": 15, "hit_chance": 70, "xp": 100}
            result = combats(player, alien)

            if result["result"] == "win":
                gain_xp(player, result["xp"])
                suspense_print("You defeated the alien prisoner and find a weird looking key.")
                add_item(player,"hospital_safe_key", 1)
                gain_xp(player, 30)
                player["has_freed_police_station_prisoner"] = True

            elif result["result"] == "lose":
                exit()
        elif choice == "2":
            suspense_print("You leave the prisoner locked up.")
            return        
def evidence_room(player):
    if "police_station_key" not in player["inventory"]:
        suspense_print("The door is locked.")
        return

    if player["has_unlocked_police_station_evidence_room"]:
        suspense_print("The evidence room is empty.")
        return
    suspense_print("your using the police station key to unlock the door")
    suspense_print("You find ammo and a medkit.")
    add_item(player,"revolver_ammo", 4)
    add_item(player,"medkit",1)
    add_item(player,"grovetown_note_2",1)
    randomized_bonus_loot(player, {"revolver_ammo": (1,2), "healing_salve": (1,3), "coin": (2,5)})
    remove_item(player,"police_station_key", 1)
    suspense_print("the note reads:\n\n"
        "The humanoids don’t hunt like animals.\n"
        "They set traps.\n"
        "They wait.\n\n"
        "One of them watched me eat.\n"
        "Like it was studying how."
    )
    player["has_unlocked_police_station_evidence_room"] = True
def burned_houses(player):
    
    if not player.get("burned_houses_looted", False):
        suspense_print("you explore the burned down houses and find an leaking healing salve, you use it before it run out and recover 3 health points.")
        player["health"] += 3
        suspense_print(f"your health is now {player['health']}")
        player["burned_houses_looted"] = True
        if skill_check(player, "scavenging", 30):
            gain_xp(player, 10)
            suspense_print("you find a note under the rubble")
            add_item(player,"wasteland_note_small_1", 1)
            suspense_print("Saw one near the ruins.\n"
                    "Small. Fast. Curious.\n\n"
                    "It didn’t attack.\n"
                    "Just watched.\n"
                    "Like an animal.\n\n")

    else:
        suspense_print("nothing else of interest here")

#ROADS_________
def hospital_road(player):
    count = player.get("has_pass_hospital_road_count", 0)
    suspense_print("You've been walking for a while and started to feel watched.")
    if not player.get("found_hospital_road_hideout", False):
        if skill_check(player, "intelligence", 50, visible=False):
            gain_xp(player, 10)
            suspense_print("Your notice a faint chemical trail on the ground, possibly left by other survivors.\n"
                        "you follow to trail to an hidden trapdoor leading underground")
            player["found_hospital_road_hideout"] = True
            hospital_road_secret_hideout(player)
            return
    while True:
        
        if (
            count >= 3
            and not player.get("medkit_encounter_done", False)
        ):
            medkit_encounter(player)
            player["medkit_encounter_done"] = True

        suspense_print("1) keep walking to the hospital")
        suspense_print("2) look around")
        suspense_print("3) go back to the crossroad")
        suspense_print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            count += 1
            hospital(player)
            return

        elif choice == "2":
            if skill_check(player, "perception", 30):
                gain_xp(player, 10)
                player["has_seen_hospital_road_alien"] = True
                suspense_print(
                    "you see something staring at you from afar\n"
                    "it quickly vanishes behind some ruins"
                )
            else:
                suspense_print("you look around but see nothing unusual")

        elif choice == "3":
            count += 1
            wasteland_cross_road(player)
            return

        else:
            suspense_print("Invalid choice")
def hospital_road_secret_hideout(player):
    suspense_print("you enter the hidden trapdoor and find a small underground hideout.")
    suspense_print("inside you find some supplies and a note.")
    add_item(player,"medkit", 1)
    add_item(player,"healing_salve", 2)
    add_item(player,"weird_fruit", 1)
    add_item(player,"scavenging_notebook", 1)
    add_item(player,"wasteland_note_small_2", 1)
    suspense_print("the note reads:\n\n"
        "Found this place while escaping.\n"
        "Safe from the creatures above.\n\n"
        "Left some supplies here.\n"
        "Might come back later.\n\n"
        "If you find this,\n"
        "use them well."
    )
    return
def medkit_encounter(player):
    suspense_print("You see a medkit lying on the ground.")

    if player.get("has_seen_hospital_road_alien", False):
        suspense_print("You recall seeing a strange figure watching you earlier.")

    while True:
        suspense_print("1) Pick up the medkit")
        suspense_print("2) Shoot it")
        suspense_print("3) Leave it")

        choice = get_choice()

        if choice == "1":
            suspense_print("As you reach for it, a tentacle lashes out!")
            alien = get_enemy("small_metamorph")
            result = fight_enemy(player, alien)

        elif choice == "2":
            weapon_name, weapon = get_current_weapon(player)

            if not weapon or weapon["type"] != "ranged":
                suspense_print("You have no ranged weapon.")
                continue

            

            suspense_print("You shoot the medkit. Dark blood sprays everywhere!")
            alien = get_enemy("small_metamorph")
            alien["health"] -= 2
            result = fight_enemy(player, alien)

        elif choice == "3":
            suspense_print("You leave it behind. Some things aren't worth the risk.")
            return

        else:
            suspense_print("Invalid choice.")
            continue

        # --- Combat resolution ---
        if result["result"] == "win":
            gain_xp(player, result["xp"])
            suspense_print("You defeated the creature and find some coins.")
            add_item(player, "coin", 5)

            if skill_check(player, "luck", 30):
                suspense_print("Luck is on your side — you find extra coins.")
                add_item(player, "coin", 3)

            return

        elif result["result"] == "lose":
            exit()


#HOSPITAL_ARC
def hospital(player):
    suspense_print("you arrived at the hospital, the building is mostly intact but the front door is locked.")
    while True:
        suspense_print("1) try to lockpick the door open")
        suspense_print("2) look for another way in")
        suspense_print("3) look through the windows")
        suspense_print("4) go back to the crossroad")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")

        choice = get_choice()   

        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("has_oppened_hospital_lock", False):
                suspense_print("the door is already unlocked, you enter the hospital.")
                hospital_inside(player)
                return
            else:
                if "bobby_pins" in player["inventory"]:
                    if skill_check(player, "lockpicking", 20):
                        suspense_print("you successfully lockpick the door and enter the hospital.")
                        player["has_oppened_hospital_lock"] = True
                        hospital_inside(player)
                        return
                    else:
                        suspense_print("you failed to lockpick the door.")
                else:
                    suspense_print("you don't have any bobby pins.")
        elif choice == "2":
            suspense_print("you find a side entrance but there is a weird looking cactus.")
            hospital_side_entrance(player)
            return
        elif choice == "3":
            if player["has_pass_window_check"]:
                suspense_print("you already looked through the windows and saw the alien inside the hospital.")
                continue
            else:
                suspense_print("you try to look through the dirty windows and see moving shadows.")
                if skill_check(player, "perception", 20):
                    suspense_print("you clearly see an alien moving inside the hospital, better be careful.")
                    player["has_pass_window_check"] = True
                else:
                    suspense_print("you can't see much through the dirty windows.")

        elif choice == "4":
            suspense_print("you go back to the crossroad")
            hospital_road(player)
            return
        else:
            suspense_print("Invalid choice")
def hospital_side_entrance(player):
    if player.get("has_deal_with_cactus", False):
        suspense_print("You are back at the side entrance of the hospital. The cactus is no longer a threat.\n"
                        "You step inside the hospital.")
        hospital_inside(player)
        return
    while True:
        suspense_print("1) Sneak past the cactus")
        suspense_print("2) Shoot the cactus with your revolver")
        suspense_print("3) Go back to the hospital entrance")
        suspense_print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        # 🥷 Sneak
        if choice == "1":
            suspense_print(
                "The paranoia of the metamorph wasteland gets to you.\n"
                "You try to sneak past the suspicious cactus."
            )

            if skill_check(player, "stealth", 50):
                slow_print_word("You slip past unnoticed.")
            else:
                slow_print_word(
                    "Your heart races… but nothing happens.\n"
                    "It was just a cactus."

                )
            player["has_deal_with_cactus"] = True

            hospital_inside(player)
            return

        # 🔫 Shoot cactus
        elif choice == "2":
            weapon_name, weapon = get_current_weapon(player)

            if not weapon or weapon["type"] != "ranged":
                suspense_print("You have no ranged weapon.")
                continue
            

            if player.get("has_killed_cactus", False):
                suspense_print("The cactus is already dead. Truly dead.")
                continue
            suspense_print("You take aim at the cactus...")

            cactus = {
                "name": "innocent cactus",
                "health": 1
            }

            player_attack(player, cactus)  
                    
            suspense_print(
                
                "The cactus explodes into splinters.\n\n"
                "…It was just a plant."
            )

            
            player["has_deal_with_cactus"] = True
            hospital_inside(player)
            return

        # 🔙 Go back
        elif choice == "3":
            suspense_print("You step away from the side entrance.")
            hospital(player)
            return

        else:
            suspense_print("Invalid choice.")
def hospital_inside(player):
    while True:
        if not player.get("hospital_metamorph_killed", False):

            if player.get("has_pass_window_check", False):
                hospital_metamorph_encounter(player)
                continue

            suspense_print("You step inside the hospital and a hidden tentacle trips you!")
            player["health"] -= 2
            if player["health"] <= 0:
                game_over()
                return

            suspense_print(f"You lose 2 health points. Health: {player['health']}")
            fight_enemy(player, {"health": 10, "hit_chance": 75, "xp": 70})
            player["hospital_metamorph_killed"] = True
            suspense_print("You defeated the alien metamorph.")
            continue
        suspense_print("You are inside the hospital. The alien metamorph lies dead.")

        suspense_print("1) get up the stairs to the second floor")
        suspense_print("2) search the hospital right room")
        suspense_print("3) search the room ahead")
        suspense_print("4) search the left room")
        suspense_print("5) go to the back door")
        suspense_print("6) go back to the hospital entrance")
        suspense_print("I) Open inventory")  
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            hospital_first_floor(player)
        elif choice == "2":
            suspense_print("you search the room and find a safe with 3 keyholes.")
            if not player.get("has_opened_hospital_safe", False):

                if "hospital_safe_key" in player["inventory"] and "second_hospital_safe_key" in player["inventory"] and "third_hospital_safe_key" in player["inventory"]:
                    suspense_print("you use the hospital safe keys to open the safe, you see a dark slimy interior, you put your hand in a damp muckus and find some medical supplies, an alien laser rifle, and an alien energy cell.")
                    add_item(player, "medkit",1)
                    add_item(player, "healing_salve",1)
                    add_item(player, "alien_laser_rifle",1)
                    add_item(player, "alien_energy_cell",1)
                    if skill_check(player, "luck", 30):
                        suspense_print("your luck pays off and you find a strange elixir.")
                        add_item(player, "strange_elixir",1)
                    add_item(player, "alien_energy_cell",2)
                    remove_item(player, "hospital_safe_key", 1)
                    remove_item(player, "second_hospital_safe_key", 1)
                    remove_item(player, "third_hospital_safe_key", 1)
                    player["has_opened_hospital_safe"] = True
                    continue
                else:
                    suspense_print("you need some keys to open the safe.")
                    continue
            else:
                suspense_print("the safe is already opened.")
                continue
        elif choice == "3":
            scavenger_room(player)
        elif choice == "4":
            if not player.get("has_hospital_left_room_been_searched", False):
                suspense_print("you search the left there is an bobby pin on the floor and stairs going down to the basement.")
                add_item(player, "bobby_pins", 3)
                player["has_hospital_left_room_been_searched"] = True
                suspense_print("you pick up the bobby pins and add them to your inventory.")
                suspense_print("you take the stairs going down to the basement.")
                hospital_basement(player)
                return
            else:
                suspense_print("you take the stairs going down to the basement again.")
                hospital_basement(player)
        elif choice == "5":
            if not player.get("has_opened_hospital_back_door", False):
                if "hospital_back_door_key" in player["inventory"]:
                    suspense_print("You use the key and step out toward the wasteland.")
                    player["has_opened_hospital_back_door"] = True
                    wasteland_4(player)
                    return
                else:
                    suspense_print("The door is locked. You need a key.")
            else:
                suspense_print("The back door is already open.")
                wasteland_4(player)
                return
        elif choice == "6":
            suspense_print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            suspense_print("Invalid choice")
def scavenger_room(player):
    while True:
        if  player.get("hospital_scavenger_killed", False):
            suspense_print("You enter the room again. The scavenger lies motionless. Whatever it was, it's dead.")
            return

        suspense_print(
            "You enter the room ahead to find the remains of a scavenger.\n"
            "You notice some pieces of his head have been altered with strange alien technology."
        )

        if skill_check(player, "perception", 20):
            suspense_print("You see a red light blinking on the scavenger's head, indicating active alien tech.")
        else:
            suspense_print("You don't notice anything unusual apart from the scavenger's head.")

        suspense_print("1) Search the body")
        suspense_print("2) Shoot the body with your revolver, just to be sure")
        suspense_print("3) Go back ")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # --- SEARCH BODY ---
        if choice == "1":
            slow_print_word("The scavenger suddenly reanimates  as a hostile alien cyborg!")

            cyborg = get_enemy("cyborg_scavenger")

            result = combats(player, cyborg)
            if result["result"] == "win":
                gain_xp(player, cyborg["xp"])
                player["hospital_scavenger_killed"] = True
                add_item(player, "alien_implant", 1)
                suspense_print("You defeated the alien cyborg scavenger.")
                return
            else:
                exit()

        # --- SHOOT BODY ---
        elif choice == "2":
            if player.get("weapon") != "revolver":
                suspense_print("You don't have a revolver.")
                continue

            if not remove_item(player, "revolver_ammo", 1):
                suspense_print("Click! You're out of ammo.")
                continue

            if skill_check(player, "luck", 17):
                suspense_print(
                    "You fire a precise shot. The scavenger awakens badly damaged and attacks!"
                )
                cyborg = get_enemy("cyborg_scavenger")
                cyborg["health"] = cyborg["health"] // 2
            else:
                suspense_print(
                    "You miss! The scavenger awakens fully and attacks!"
                )
                cyborg = get_enemy("cyborg_scavenger")
                    

            result = combats(player, cyborg)
            if result["result"] == "win":
                gain_xp(player, cyborg["xp"])
                player["hospital_scavenger_killed"] = True
                add_item(player, "alien_implant", 1)
                suspense_print("You defeated the alien cyborg scavenger.")
                return
            
            else:
                exit()
        elif choice == "3":
            return
        else:
            suspense_print("Invalid choice.")
def hospital_metamorph_encounter(player):
    while True:
        suspense_print("You are inside the hospital. You remember seeing an alien through the window earlier but dont remember seeing that chair.")
        suspense_print("1) shoot the chair with your revolver")
        suspense_print("2) aproach the chair")
        suspense_print("3) go back to the hospital entrance")
        suspense_print("I) Open inventory")
    
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if "revolver" not in player["inventory"]:
                suspense_print("You don't have a revolver.")
                continue
            if not remove_item(player, "revolver_ammo", 1):
                suspense_print("Click! You're out of ammo.")

            suspense_print("you sneak and shoot the chair for critical dammage whitch killed the alien metamorph")
            player["hospital_metamorph_killed"] = True
            add_item(player,"healing_salve", 1)

            gain_xp(player, 50)
            
            return
        elif choice == "2":
            suspense_print("you aproach the chair and the alien metamorph attacks you!")
            alien = {"health": 10, "hit_chance": 75, "xp": 70}
            result = combats(player, alien)

            if result["result"] == "win":
                gain_xp(player, result["xp"])
                add_item(player, "healing_salve", 1)
                suspense_print("You defeated the alien metamorph.")
                player["hospital_metamorph_killed"] = True  
                return

            elif result["result"] == "lose":
                exit()
        elif choice == "3":
            suspense_print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            suspense_print("Invalid choice")  
def hospital_basement(player):
    
    suspense_print(
        "You enter the basement. As you descend the stairs, you hear pained moans coming from below.\n"
        "At the bottom, a large alien stands before you — humanoid, wearing a white lab coat."
    )

    while True:
        suspense_print("\n1) Try to sneak attack the alien")
        suspense_print("2) Charge at the alien with your weapon drawn")
        suspense_print("3) Look around the room")
        suspense_print("4) Go back upstairs")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")


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

            suspense_print("You attempt to sneak closer...")
            if skill_check(player, "stealth", 40):
                slow_print_word("You catch the alien off guard!")
                alien = {"health": 15, "hit_chance": 70, "xp": 150}
            else:
                slow_print_word("You fail to sneak — the alien turns toward you!")
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

            suspense_print("You charge at the alien!")
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
                suspense_print("you see a jailed man but the alien blocks your path — you’ll need to deal with it first.")
            else:
                hospital_basement_boss_defeated(player)
                return

        # ───────────────────────────────
        # Leave
        # ───────────────────────────────
        elif choice == "4":
            suspense_print("You retreat back upstairs.")
            hospital_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
def finish_hospital_boss(player, xp):
    gain_xp(player, xp)
    suspense_print("You defeated the alien scientist.")

    
    add_item(player, "second_hospital_safe_key", 1)
    add_item(player, "alien_scientist_suit", 1)
    add_item(player, "hospital_back_door_key", 1)
    

    player["has_defeated_hospital_boss"] = True
    hospital_basement_boss_defeated(player)
def hospital_basement_boss_defeated(player):
    suspense_print("you look around the room and see various alien experiments and equipment, but nothing useful.")
    suspense_print("there is also a cell in the corner with a prisoner inside.")
    while True:
        suspense_print("1) free the prisoner")
        suspense_print("2) ignore the prisoner")
        suspense_print("3) talk to the prisoner")
        suspense_print("4 go back upstairs")
        suspense_print("I) Open inventory")  
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("has_help_basement_prisoner", False):
                suspense_print("you free the prisoner from the cell, he thanks you and gives you map to a secret humain base.\n" \
                "when you arrive tell them that john sent you.\n")
                add_item(player, "map_to_base",1)
                player["has_help_basement_prisoner"] = True
                return
            else:
                suspense_print("the prisoner is already free.")
                return
        elif choice == "2":
            suspense_print("you ignore the prisoner, who is begging for help.")
            return
        elif choice == "3":
            questione_prisoner(player)
        elif choice == "4":
            suspense_print("you go back upstairs")
            hospital_inside(player)
            return
        else:
            suspense_print("Invalid choice")
def questione_prisoner(player):
    while True:
        suspense_print("1) Ask about the alien metamorph")
        suspense_print("2) Ask about the alien cyborg scavenger")
        suspense_print("3) Ask about the alien scientist")
        suspense_print("4) Ask about what happened since the alien laser touchdown")
        suspense_print("5) Go back")
        suspense_print("I) Open inventory")
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "The prisoner tells you that the alien metamorph is a dangerous creature "
                "that can mimic human forms and is highly aggressive. However, they do not "
                "mimic perfectly, and with enough perception, you can spot them.")
        elif choice == "2":
            suspense_print(
                "The prisoner explains that the alien cyborg scavenger was a friend of his "
                "who got captured by the alien scientist and experimented on, turning him "
                "into a cyborg against his will. The aliens have heavily experimented on "
                "humans since the invasion, both technologically and biologically."
            )

        elif choice == "3":
            suspense_print(
                "The prisoner reveals that the alien scientist was conducting experiments "
                "on humans to create hybrid creatures for the aliens. He thanks you for "
                "your assistance, saying he was next."
            )

        elif choice == "4":
            suspense_print(
                "The prisoner recounts that a few weeks after the laser scorched the Earth, "
                "a massive ship from space landed and started terraforming. The area around "
                "the landing site became unbreathable for humans without proper equipment. "
                "If you see their flora, turn around."
            )

        elif choice == "5":
            return
def hospital_first_floor(player):
    while True:
        suspense_print("you get up the stairs and see 2 room, a flower pot and a trash can")
        suspense_print("1)Go to the room and de left")
        suspense_print("2)Go to the room and the right")
        suspense_print("3)Inspect the flower pot")
        suspense_print("4)Inspect the trash can")
        suspense_print("5)Go back downstairs")
        suspense_print("I)Open inventory")
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
                suspense_print("You search through the trash and find some coins.")
                add_item(player, "coin",3)
                player["hospital_trash_pot_check"] = True
            else:
                suspense_print("The trash can is empty.")
        elif choice == "5":
            suspense_print("you go back downstairs")
            hospital_inside(player)
            return
        else:
            suspense_print("Invalid choice")                         
def Hospital_flower_pot(player):

    while True:
        if not player.get("hospital_flower_pot_checked", False):
            suspense_print("1) Check the flower pot")
            suspense_print("2) Go back")
            if skill_check(player, "perception", 30):
                suspense_print("Something feels off about a neat little flower pot in the middle of an alien-infested hospital.")
                suspense_print("3) Shoot the flower!")

        
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print("You carefully examine the flower pot...")
            suspense_print("Suddenly, a tentacle lashes out!")
            alien = {"health": 3, "hit_chance": 70, "xp": 0}
            fight_enemy(player, alien)
            player["hospital_flower_pot_checked"] = True
            return

        elif choice == "3" and player.get("hospital_flower_pot_checked", False):
            suspense_print("You attack the flower pot before it can react. It dies instantly.")
            player["hospital_flower_pot_checked"] = True
            return

        elif choice == "2":
            return

        else:
            suspense_print("Invalid choice.")
def Hospital_first_floor_left_room(player):
    while True:
        suspense_print("You enter the room on the left. You see a desk with an old PC. It looks like it still works.")

        # PC NOT hacked yet
        if not player.get("hospital_pc_hacked", False):
            suspense_print("1) Try to hack the PC")
            suspense_print("2) Go back")
            suspense_print("I) Open inventory")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                if skill_check(player, "intelligence", 20):
                    player["hospital_pc_hacked"] = True
                    suspense_print("You successfully hack through the PC defenses.")
                else:
                    suspense_print("The PC defenses are too complex.")
            elif choice == "2":
                return
            else:
                suspense_print("Invalid choice")

        # PC hacked
        else:
            suspense_print("1) Read first message")
            suspense_print("2) Read second message")
            suspense_print("3) Unlock the desk safe")
            suspense_print("4) Read third message")
            suspense_print("5) Go back")
            suspense_print("I) Open inventory")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                suspense_print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "01/01/2000\n\n"
                    "Hey Millie, I hope you're doing well. The hospital is full of the usual "
                    "New Year missing fingers and drunk fools. I think I'll have to work all night."
                )

            elif choice == "2":
                suspense_print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "02/01/2000\n\n"
                    "God, Millie, what was that? A bright flash and most of everything wiped out. "
                    "The grid shut down, all patients on life support were lost. "
                    "I heard millions died. I hope you're alright. Please answer me."
                )

            elif choice == "3":
                if not player.get("has_taken_hospital_pc_safe", False):
                    suspense_print("You unlock the safe and find some ammo and a medkit.")
                    add_item(player, "revolver_ammo", 3)
                    add_item(player, "medkit", 1)
                    player["has_taken_hospital_pc_safe"] = True
                else:
                    suspense_print("The safe is empty.")
            elif choice == "4":
                suspense_print(
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
                suspense_print("Invalid choice")
def Hospital_first_floor_right_room(player):
    while True:
        suspense_print("You enter the room on the right.\n")
        if not player.get("Hospital_first_floor_right_room_note_taken", False):
            suspense_print(
            "There is a note lying on the floor.")
        suspense_print("1)read the note")
        suspense_print("2)Go back")
        suspense_print("I)Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")

        choice = get_choice()  

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("Hospital_first_floor_right_room_note_taken", False):
                add_item(player, "hospital_note_doctor", 1)
                player["Hospital_first_floor_right_room_note_taken"] = True
                suspense_print("you pick up the note")
                suspense_print(
                    "The handwriting is shaky.\n\n"
                    "They can’t breathe our air.\n"
                    "That’s why they don’t stay long.\n\n"
                    "The small ones don’t mind.\n"
                    "They belong here now."
                        )           
            else:
                suspense_print("nothing else to do here")
        elif choice == "2":
            return 
        else:
            suspense_print("Invalid choice")

#road to old farm
def wasteland_3(player):
    suspense_print(
        "You arrive at an empty camp. You see a fire still hot\n"
        "and an old bedroll open on the floor."
    )
    if skill_check(player, "luck", 30, visible=False):
        gain_xp(player, 10)
        suspense_print(
            "As you approach, you notice something shiny near the fire.\n"
            "It's a small pouch of coins left behind by the previous occupant."
        )
        add_item(player, "coin", 5)
    while True:
        suspense_print("\nWhat do you do?")
        suspense_print("1) Look at the fire")
        suspense_print("2) Move forward")
        suspense_print("3) Look under the bedroll")
        suspense_print("4) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "You come near the fire. You see fresh footsuspense_prints, they look human.\n"
                "Better not stay here too long."
            )
            continue

        elif choice == "2":
            suspense_print("You proceed forward.")
            wastland_stranger_encounter(player)
            return

        elif choice == "3":
            if player.get("looted_the_bedroll", False):
                suspense_print("You already took everything that was here.")
                continue

            if skill_check(player, "scavenging", 30):
                suspense_print(
                    "Your scavenging experience reminds you that people often bury valuables\n"
                    "under their bedroll."
                )
                suspense_print(
                    "You dig under the bedroll and find a sharpened kitchen knife\n"
                    "and some revolver ammo."
                )
                add_item(player, "sharp_kitchen_knife", 1)
                add_item(player, "revolver_ammo", 1)
                add_item(player, "bobby_pin", 1)
                player["looted_the_bedroll"] = True
            else:
                suspense_print("You search around but fail to find anything useful.")

        elif choice == "4":
            wasteland_cross_road(player)
            return

        else:
            suspense_print("Invalid choice.")
def wasteland_stranger_encounter(player):
    count =player.get("wasteland_stranger_encounter_count", 0)
    player["wasteland_stranger_encounter_count"] = count + 1
    if count >=5:
        suspense_print(
            "As you walk, you feel a strange presence behind you.\n"
            "You quicken your pace, but the feeling persists.\n"
            "Suddenly, you hear the sound of footsteps matching your own.\n"
            "before you can react, a blunt pain erupts in the back of your head.\n"
            "You collapse to the ground, unconscious.\n\n"
        )
        alien_cell(player)
        return
            
    while True:
        if not player.get("met_wasteland_stranger_near_farm", False):
            suspense_print(
            "As you walk away from the camp, a silhouette appears on the horizon.\n"
            "A tall figure. Long coat.\n"
            "An absurdly perfect cowboy hat.\n"
            "It’s coming straight toward you."
    )
            suspense_print("1) Walk toward the stranger")
            suspense_print("2) Shoot first")
            suspense_print("3) Go back")
            suspense_print("I) Open inventory")
            suspense_print("S) Save game")
            suspense_print("L) Load game")

            choice = get_choice()

            if handle_global_input(choice, player):
                continue

            if choice == "1":
                suspense_print(
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
                    slow_print_word(
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
                    suspense_print(
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
                    suspense_print(
                        "The gunfight ends.\n"
                        "The wasteland grows quiet again.\n\n"
                        "You take the cowboy hat.\n"
                        "Inside his coat, you find a note."
                    )
                    suspense_print("note:\n"
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
                    suspense_print("You barely escape with your life.")
                    wasteland_3(player)
                    return

            elif choice == "3":
                
                suspense_print(
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
                suspense_print("Invalid choice.")

        else:
            if player.get("wasteland_stranger_near_farm_alive", True):
                suspense_print(
                    "you keep walking remembering the encounter with the stranger.\n"
                    "you can't forget that cowboy hat."
                )
            else:
                suspense_print(
                    "you keep walking remembering the encounter with the stranger.\n"
                    "You're still haunted by his face."
                )
            old_farm_house(player)
            return
def wasteland_stranger_encounter_dialogue(player):
    suspense_print(
        "You stare down the stranger.\n"
        "Gun in hand, both of you trying to see humanity in the other's eyes."
    )

    while True:
        if player.get("met_wasteland_stranger_near_farm", False):
            suspense_print("The stranger has spoken before. His grip tightens on the gun.")

        suspense_print("\nWhat do you do?")
        suspense_print("1) Try to calm things down")
        suspense_print("2) Look for details that might prove he is an alien")
        suspense_print("3) Say all you really want is his hat (attack)")
        suspense_print("4) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        # ---- OPTION 1 : CHARISMA ----
        if choice == "1":
            if skill_check(player, "charisma", 25):
                gain_xp(player, 10)

                suspense_print(
                    "After a long pause and many compliments about his hat, the stranger relaxes.\n"
                    "He tells you to turn back, nothing ahead but an old farmhouse full of mutated creatures.\n"
                    "Before leaving, he hands you a folded note.\n"
                    "“Keep your eyes on the horizon,” he says."
                )

                add_item(player, "grovetown_note_1", 1)

                suspense_print(
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
                suspense_print(
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
                suspense_print(
                    "You study him closely.\n"
                    "Nothing stands out.\n"
                    "If he’s something else… he hides it well."
                )
            else:
                suspense_print(
                    "You try to read him.\n"
                    "Your instincts whisper that something is wrong.\n"
                    "But you can’t prove it."
                )
            return

        # ---- OPTION 3 : ATTACK ----
        elif choice == "3":
            suspense_print("The fight for the hat begins.")

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
            suspense_print("Invalid choice.")
def loot_cowboy(player):
    suspense_print(
        "The gunfight ends.\n"
        "The wasteland grows quiet again.\n\n"
        "You take the cowboy hat.\n"
        "Inside his coat, you find a note."
    )

    suspense_print(
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
def alien_cell(player):
    suspense_print(
        "You awaken in a slimy damp cell.\n"
        "Strange symbols glow faintly on the walls.\n"
        "You hear distant wet clicking sounds echoing through the corridors.")
    while True:
            suspense_print("1) Look around the cell")
            suspense_print("2) Try to open the cell door")
            if player.get("understand_alien_language", False):  
                suspense_print("3) Speak in the alien language")
            suspense_print("I) Open inventory")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print(
                    "You examine the cell.\n"
                    "The walls are covered in strange alien symbols that seem to pulse with energy.\n"
                    "The floor is damp and slippery."
                )
            elif choice == "2":
                if skill_check(player, "lockpicking", 25):
                    suspense_print(
                        "You manage to pick the lock and open the cell door quietly.\n"
                        "You slip out into the dimly lit corridor.\n"
                        "you hear something calling to you from a crate nearby.\n"
                        "as your oppen it something grabs your hand from inside the crate\n."
                        "you feel it going intro your body and you lose consciousness."
                    )
                    suspense_print("You woke up in the old bunker.\n"
                                    "something is atached to your hand it look like a weapon.\n" \
                    )
                    add_item(player, "symbiotic_blood_pistol", 1)
                    old_bunker(player)
                    
                    return
                else:
                    suspense_print("You fail to pick the lock.\n"
                        "The clicking sounds grow louder."
                        "after a moment, a creature appears outside your cell."
                        "it releasesa gaz in the cell that makes you unconscious."
                    )
                    suspense_print("You woke up in the old bunker.\n" \
                    "you feel like something is missing from you but you feel more aware.")
                    player["health"] -=10
                    player["perception"] +=2
                    old_bunker(player)
            elif choice == "3" and player.get("understand_alien_language", False):
                suspense_print(
                    "You attempt to communicate using the alien language you learned.\n"
                    "The clicking sounds stop.\n"
                    "A figure approaches your cell."
                )
                suspense_print(
                    "it tells you that you will be freed when he finish what he must do to you.\n"
                    "you smell a strange scent and feel dizzy.\n"
                    "you lose consciousness."
                )
                suspense_print("You woke up in the old bunker.\n" \
                    "you feel like something is missing from you but you feel more aware.")
                player["health"] -=10
                player["perception"] +=2
                old_bunker(player)        
            else:
                suspense_print("Invalid choice.")         

#survivor_base
def old_farm_house(player):
    suspense_print(
        "You arrive at an old farmhouse.\n"
        "A cold metallic echo carries from inside, like the house is breathing."
    )

    while True:
        suspense_print("\nWhat do you do?")
        suspense_print("1) Enter the house")
        suspense_print("2) Go to the wasteland crossroad")

        if "map_to_base" in player.get("inventory", {}):
            suspense_print("3) Follow the map behind the house toward the mountain base")

        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("visited_old_farm_house"):
                suspense_print("The wind nudges the door open… then slams it.\n"
                      "You steady your breath and push forward.")
                player["visited_old_farm_house"] = True

            suspense_print("You step inside the farmhouse...")
            farm_house_inside(player)
            return

        elif choice == "2":
            wasteland_3(player)

        elif choice == "3" and "map_to_base" in player.get("inventory", {}):
            # Make sure this function exists; the name looks like a typo.
            try:
                survivor_montain_base(player)  # or survivor_mountain_base(player)
            except NameError:
                suspense_print("The path to the mountain base is blocked — you’ll need to find another route.")
            return

        else:
            suspense_print("Invalid choice.")
def survivor_montain_base(player):
    if "survivor_base_access_card" in player.get("inventory", {}):
        suspense_print("You use the access card to enter the base, you feel watched\")")
        survivor_mountain_base_inside(player)
        return
    suspense_print(
        "You follow the map behind the farmhouse.\n"
        "After a long trek, you arrive at a hidden mountain base.\n"
        "at the front of the door waits a gard weapon in hand."
    )
    suspense_print("1) talk to the guard ")
    suspense_print("2) go back to the farm house")
    suspense_print("I) Open inventory")
    if  player.get("has_received_survivor_base_access_card", False):
        suspense_print("You use the access card to enter the base as the guard steps aside.")
        survivor_mountain_base_inside(player)
        return
        
    while True:
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "The guard eyes you warily.\n"
                "\"State your business,\" he demands.\n\n"
                "You explain that john gave you the map when you saved him from the alien prison and are seeking refuge.\n"
                "He nods slowly, then steps aside to let you in.\n\n"
                "Inside, you find a community of survivors."
            )
            add_item(player, "survivor_base_access_card", 1)
            survivor_mountain_base_inside(player)
            return
        elif choice == "2":
            suspense_print("You head back to the farmhouse.")
            old_farm_house(player)
            return
        else:
            suspense_print("Invalid choice.")
def survivor_mountain_base_inside(player):
    """
    Mountain base interior.
    It feels safer than the outside.
    That doesn’t mean it feels safe.
    """
    player["scene"] = "MountainBaseInside"

    count = player.get("has_visited_mountain_base_count", 0) + 1
    player["has_visited_mountain_base_count"] = count

    # --- 3rd visit: John ---
    if count == 3 and not player.get("has_met_john_prisoner", False):
        suspense_print(
            "You step into the mountain base.\n"
            "The heavy gates grind shut behind you.\n\n"
            "For a moment, no one speaks.\n\n"
            "Then you see John, the prisoner you saved.\n"
            "He stands against the stone wall, thinner than before.\n"
            "His eyes lock onto yours.\n\n"
            "He raises a hand slowly.\n\n"
            "\"I was hoping it was really you,\" he says.\n"
            "\"I wasn’t sure anymore.\""
        )
        john_prisoner_dialogue(player)
        return

    # --- 7th visit: survivor incident ---
    if count >= 7 and  player.get("has_completed_leader_quest", False) and not player.get("has_accepted_leader_second_quest", False):
        suspense_print(
            "Shouting echoes through the tunnels as you enter.\n\n"
            "Two survivors face each other in a narrow corridor.\n"
            "Both are armed.\n"
            "Both are shaking.\n\n"
            "\"He changed,\" one screams. \"I SAW HIS EYES.\"\n"
            "\"You're wrong,\" the other pleads. \"Please—\"\n\n"
            "The gunshot is deafening.\n\n"
            "The body collapses.\n"
            "Blood spreads across the concrete.\n\n"
            "Nothing transforms.\n"
            "The blood runs red.\n\n"
            "Just a dead man.\n\n"
            "The base goes silent.\n"
            "The leader slowly turns to look at you."
        )
        leader_second_quest(player)
        return

    # --- Default description ---
    suspense_print(
        "You enter the mountain base.\n\n"
        "The air is cold and stale.\n"
        "The stone walls swallow sound, twisting every voice.\n\n"
        "Survivors move quickly, avoiding eye contact.\n"
        "No one stays still for long.\n\n"
        "This place is safer than the outside.\n"
        "That doesn’t mean it feels safe."
    )

    while True:
        suspense_print("\nWhat do you do?")
        suspense_print("1) Speak to the leader")
        suspense_print("2) Walk through the base")
        suspense_print("3) Visit the merchant")
        suspense_print("4) Leave the base")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
    # Check if player has the actual item FIRST
            if "radio_device" in player.get("inventory", {}):
                suspense_print(
                    "You approach the leader.\n"
                    "She looks at you with hope in her eyes.\n\n"
                    "\"You have the radio device!\" she exclaims.\n"
                    "\"This will save us all!\"\n\n"
                    "You hand over the radio device.\n"
                    "now we can stop metamorph transformation in our base.\""
                )
                player["has_completed_leader_quest"] = True
                remove_item(player, "radio_device", 1)
                gain_xp(player, 200)
                add_item(player, "shielded_jacket", 1)
                add_item(player, "coin", 20)
                add_item(player, "healing_salve", 2)
                add_item(player, "shotgun_shells", 4)
                continue
            elif "energy_core" in player.get("inventory", {}):
                suspense_print(
                    "You approach the leader.\n"
                    "She looks at you with weary eyes.\n\n"
                    "\"You have the energy core,\" she says.\n"
                    "\"This will help power the base's defenses.\"\n\n"
                    "You hand over the energy core.\n"
                    "Thank you. she says with a faint glimmer of hope."
                )
                if player.get("thomas_allied", False):
                    suspense_print(
                        "ho and thomas has returned it has something to discuss with you.\n"
                        "you should go find him."
                    )
                    player["can_accept_thomas_quest"] = True
                remove_item(player, "energy_core", 1)
                gain_xp(player, 100)
                add_item(player, "coin", 50)
                add_item(player, "rifle",1)
                add_item(player, "rifle_ammo", 10)
                add_item(player, "weird_fruit", 1)
                continue
            # NOW check quest flags
            elif player.get("leader_radio_quest_accepted", False) and not player.get("has_completed_leader_quest", False):
                suspense_print(
                    "You approach the leader.\n"
                    "She nods at you.\n\n"
                    "\"Have you retrieved the radio device yet?\" she asks."
                )
                continue
            elif player.get("has_accepted_leader_second_quest", False) and not player.get("has_completed_leader_second_quest", False):
                suspense_print(
                    "You approach the leader.\n"
                    "She looks at you with weary eyes.\n\n"
                    "\"Have you brought the energy core?\" she asks."
                )
                continue
            elif player.get("has_completed_leader_quest", False):
                suspense_print(
                    "You approach the leader.\n"
                    "She smiles warmly.\n\n"
                    "\"Thank you for retrieving the radio device,\" she says.\n"
                    "\"With this we have a chance to stop the metamorph infiltration.\"\n\n"
                    "\"You've done a great service for all of us.\""
                )
                continue
            # Default: offer first quest
            else:
                suspense_print(
                    "You approach the leader.\n"
                    "She studies you carefully before speaking.\n\n"
                    "\"I heard what you did for John,\" she says.\n"
                    "\"You're not like the others,\" she says quietly.\n"
                    "\"You've seen what's out there… and what it does to people.\"\n\n"
                    "\"We may need your help.\""
                )
                leader_quest(player)
                continue

        elif choice == "2":
            if player.get("can_accept_thomas_quest", False):
                suspense_print(
                    "As you walk through the base, Thomas approaches you.\n"
                    "\"I heard you brought the energy core,\" he says.\n"
                    "\"i can finaly finish my work now.\"\n\n"
                    "He looks at you expectantly.\n"
                    "\"Will you help me with one last task?\""
                    )
                thomas_quest(player)
                
                player["can_accept_thomas_quest"] = False
                return
            suspense_print(
                "You wander through the base.\n\n"
                "A child stares at you from behind a barricade.\n"
                "Someone sobs softly behind a closed door.\n"
                "You hear a scream — then laughter.\n\n"
                "No one explains anything."
            )

        elif choice == "3":
            suspense_print(
                "The merchant greets you with a tired smile.\n"
                "\"Ammo's getting scarce,\" he mutters.\n"
                "\"So are people.\""
            )
            survivor_base_merchant(player)

        elif choice == "4":
            suspense_print(
                "You leave the base.\n"
                "The gates close behind you.\n\n"
                "For a moment, you feel relieved to be outside."
            )
            old_farm_house(player)
            return

        else:
            suspense_print("Invalid choice.")
def survivor_base_merchant(player):
    while True:
        suspense_print("\nThe merchant watches you carefully.")
        suspense_print("1) Buy items")
        suspense_print("2) Sell items")
        suspense_print("3) Leave")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # --- SELL ---
        if choice == "2":
            sellable = [
                item for item in player["inventory"]
                if item in ITEMS and ITEMS[item].get("sell")
            ]

            if not sellable:
                suspense_print("You have nothing worth trading.")
                continue

            suspense_print("\nWhat will you sell?")
            for i, item in enumerate(sellable, start=1):
                value = ITEMS[item]["sell"]
                name = ITEMS[item]["name"]
                suspense_print(f"{i}) {name} - {value} coins")

            suspense_print(f"{len(sellable)+1}) Leave")

            sell_choice = get_choice()

            if sell_choice.isdigit():
                idx = int(sell_choice) - 1
                if 0 <= idx < len(sellable):
                    item = sellable[idx]
                    if remove_item(player, item, 1):
                        add_item(player, "coin", ITEMS[item]["sell"])
                        suspense_print(f"You sell the {ITEMS[item]['name']}.")
            continue
        # --- BUY ---
        elif choice == "1":
            shop_items = {
                "medkit": 15,
                "revolver_ammo": 5,
                "shotgun_shells": 10,
                "rifle_ammo": 8,
                "healing_salve": 12,
                "magnum": 300,
                "magnum_ammo": 5

            }  
            suspense_print("\nWhat will you buy?")
            for i, (item, price) in enumerate(shop_items.items(), start=1):
                name = ITEMS[item]["name"]
                suspense_print(f"{i}) {name} - {price} coins")
            suspense_print(f"{len(shop_items)+1}) Leave")
            buy_choice = get_choice()
            if buy_choice.isdigit():
                idx = int(buy_choice) - 1
                if 0 <= idx < len(shop_items):
                    item = list(shop_items.keys())[idx]
                    price = shop_items[item]
                    if player["inventory"].get("coin", 0) >= price:
                        remove_item(player, "coin", price)
                        add_item(player, item, 1)
                        suspense_print(f"You buy the {ITEMS[item]['name']}.")
                    else:
                        suspense_print("You don't have enough coins.")
            continue
        elif choice == "3":
            return
def john_prisoner_dialogue(player):
    suspense_print(
        "John keeps his voice low.\n\n"
        "\"Thank you… for getting me out,\" he says.\n"
        "\"But listen to me carefully.\"\n\n"
        "\"People here aren’t the same as when I arrived.\"\n"
        "\"They watch each other.\"\n"
        "\"They listen at doors.\"\n\n"
        "\"I saw one of the guards change.\"\n"
        "\"Or maybe I just *thought* I did.\"\n\n"
        "He presses something cold into your hand.\n"
        "\"Take this. If things go bad… you’ll need it.\""
    )

    add_item(player, "third_hospital_safe_key", 1)
    suspense_print("You received: Hospital Safe Key III.")
    player["has_met_john_prisoner"] = True
    survivor_mountain_base_inside(player)
    return             
def leader_quest(player):
    suspense_print(
        "The leader studies you in silence.\n\n"
        "\"We lost an outpost,\" she finally says.\n"
        "\"No warning. No survivors we could trust.\"\n\n"
        "\"There was a high-frequency radio device there.\"\n"
        "\"We believe it interferes with metamorph behavior.\"\n\n"
        "\"If we don’t recover it… this place won’t last.\""
    )

    while True:
        suspense_print("1) Accept the quest")
        suspense_print("2) Decline")
        suspense_print("3) Ask for more information")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "You agree to help the leader.\n"
                "she give you the key to the outpost.\n"
                "\"Thank you,\" she says. \"Be careful out there.\""
            )
            player["leader_radio_quest_accepted"] = True
            add_item(player, "mountain_tunnel_key", 1)
            return
        elif choice == "2":
            suspense_print(
                "You decline the quest.\n"
                "\"I understand,\" the leader says. \"But we could really use your help.\""
            )
            return
        elif choice == "3":
            suspense_print(
                "The leader explains that the outpost was attact during the night by alien creatures many died.\n"
                "they had tu run away fast leaving many important items behind.\n\n"
                "before seteling here.\n"
                "The radio device is hight power shield that block metamorph transformation.\n"
                "\"It's located in a dangerous area after the montain tunelnear grove town,\" she warns. \"But if anyone can get it, it's you.\""
            )
        else:
            suspense_print("Invalid choice.")
def leader_second_quest(player):
    suspense_print(
        "The leader’s voice is quiet.\n\n"
        "\"This wasn’t the first incident,\" she admits.\n"
        "\"We tried activating the radio device… but it needs power.\"\n\n"
        "\"A energy core is required to run it.\"\n\n"
        "\"The only known source is beyond the hospital.\n"
        "In the old military research base.\"\n\n"
        "pass the terraformed zone, in alien land..\" \n\n"
        "She hesitates.\n\n"
        "\"No one we sent there came back the same.\""
    )
    while True:
        suspense_print("1) Accept the quest")
        suspense_print("2) Decline")
        suspense_print("3) Ask for more information")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "You agree to help the leader.\n"
                "\"Thank you,\" she says. \"Be careful out there.\""
            )
            player["has_accepted_leader_second_quest"] = True
            survivor_mountain_base_inside(player)
            return
        elif choice == "2":
            suspense_print(
                "You decline the quest.\n"
                "\"I understand,\" the leader says. \"But we could really use your help.\""

            )
            survivor_mountain_base_inside(player)
            return
        elif choice == "3":
            suspense_print(
                "The leader explains that the energy core is a rare near limitless power source used in military technology.\n"
                "it can be found in the old military research base located near the hospital.\n"
                "she warns you that the base is heavily infested with metamorphs and other alien creatures.\n"
                "only a few have ever returned from there."
            )
            continue
        else:
            suspense_print("Invalid choice.")
def thomas_quest(player):   
    suspense_print(
        "Thomas looks at you with hopeful eyes.\n\n"
        "\"I need your help,\" he says.\n"
        "\"i finaly unlock the door to the secret lab.\"\n\n"
        "\"But the security system is still active.\"\n"
        "\"many security bots are patrolling the area.\"\n\n"
        "\"If you can disable them, I can finish my work there.\"\n\n"
    )
    while True:
        suspense_print("1) Accept the quest")
        suspense_print("2) Decline")
        suspense_print("3) Ask for more information")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "You agree to help Thomas.\n"
                "\"Thank you,\" he says. \"Be careful out there.\nHere's the key to the lab.\""
            )
            player["thomas_quest_accepted"] = True
            add_item(player, "mountain_base_secret_lab_key", 1)
            survivor_mountain_base_inside(player)
            return
        elif choice == "2":
            suspense_print(
                "You decline the quest.\n"
                "\"I understand,\" Thomas says. \"But I could really use your help.\""
            )
            survivor_mountain_base_inside(player)
            return
        elif choice == "3":
            suspense_print(
                "Thomas explains that the secret lab is a hidden facility within the mountain base.\n"
                "it contains advanced technology that could help humanity fight back against the alien threat.\n"
                "it was a weapon research lab before the invasion.\n"
                "he warns you that the security bots are heavily armed and dangerous.\n"
                "they will attack anyone who enters the lab without authorization.\n"
                "you can keep any useful weapons or items you find there.\n"
                "i only need them disabled so i can finish my work."
            )
            continue
            
        else:
            suspense_print("Invalid choice.")    

# Farm House Rooms
def farm_house_inside(player):
    suspense_print("You enter the old farmhouse. A dark living room yawns ahead; furniture slumps under a skin of dust.")
    if skill_check(player, "perception", 30):
        suspense_print("A low growl filters down from upstairs.Better be careful.")
    while True:
        suspense_print("\n1) Go upstairs")
        suspense_print("2) Go to the kitchen")
        suspense_print("3) Go to the living room")
        suspense_print("4) Go back outside")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("You climb. The hallway is a black throat leading to the attic.")
            farm_house_upstairs(player)
        elif choice == "2":
            suspense_print("You step into the kitchen. Old appliances sit in silence.")
            farm_house_kitchen(player)
        elif choice == "3":
            if not player.get("farm_house_living_room_unlocked", False):
                suspense_print("You reach a locked door. Through the glass, a shotgun waits on the mantle.")
                if skill_check(player, "lockpicking", 40):
                    suspense_print("You tease the tumblers. The lock yields. The living room welcomes you with dust.")
                    player["farm_house_living_room_unlocked"] = True
                    farm_house_living_room(player)
                    return
                if player.get("inventory", {}).get("old_farm_house_living_room_key", 0) > 0:
                    suspense_print("You use the living room key. The door opens with a tired click.")
                    player["farm_house_living_room_unlocked"] = True
                    # Remove one key from inventory safely
                    remove_item(player, "old_farm_house_living_room_key", 1)
                    farm_house_living_room(player)
                    return
                suspense_print("The door is stubborn — it will not open.")
            else:
                suspense_print("You enter the living room.")
                farm_house_living_room(player)
        elif choice == "4":
            suspense_print("You step back out into the yard.")
            old_farm_house(player)
            return
        else:
            suspense_print("Invalid choice")
def farm_house_living_room(player):
    while True:
        suspense_print("The living room is dark, the air thick with dust and a faint smell of metal.")
        suspense_print("1) Examine the room")
        suspense_print("2) Go back ")
        suspense_print("3) Go back ")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_living_room_searched", False):
                suspense_print("You lift the shotgun from the mantle. Underneath: shells and a pair of tactical gloves.")
                add_item(player, "shotgun", 1)
                add_item(player, "shotgun_shells", 5)  
                add_item(player, "tactical_gloves", 1)
                player["farm_house_living_room_searched"] = True
            else:
                suspense_print("Whatever mattered here has already been taken.")
        elif choice == "2":
            suspense_print("You return to the kitchen.")
            return
        elif choice == "3":
            suspense_print("You step back.")
            return
        else:
            suspense_print("Invalid choice")
def farm_house_upstairs(player):
    while True:
        suspense_print("Upstairs lies mostly in ruins. A dried corpse rests against the wall. Stairs vanish into the attic.")
        suspense_print("1) Examine the corpse")
        suspense_print("2) Go to the attic")
        suspense_print("3) Go back downstairs")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_upstairs_corpse_searched", False):
                suspense_print("You search the corpse a massive claw mark rest on his chest \n"
                       "and find some coins and a folded note.")
                add_item(player, "coin", 10)
                add_item(player, "farmer_note", 1)
                suspense_print("\nThe note reads:\n")
                suspense_print(
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
                suspense_print("The poor soul has nothing else of value.")
        elif choice == "2":
            suspense_print("You climb up to the attic. The air grows thin.")
            farm_house_attic(player)
        elif choice == "3":
            suspense_print("You go back downstairs to the living room.")
            return
        else:
            suspense_print("Invalid choice")
def update_bat_phase(beast):
    """Mutate the bat based on remaining health."""
    max_hp = beast.get("max_health", beast["health"])
    current_hp = beast["health"]
    hp_pct = current_hp / max_hp

    # Phase 2: Frenzied
    if hp_pct <= 0.6 and not beast.get("phase_2", False):
        beast["phase_2"] = True
        beast["damage"] += 2
        beast["special_attack_chance"] = 0.25
        beast["attack_messages"].extend([
            "The bat howls in pain and attacks wildly!",
            "Blood sprays as it dives again and again!"
        ])
        suspense_print(
            "The bat screams something breaks inside it.\n"
            "Its movements become faster. Angrier."
        )

    # Phase 3: Death Spiral
    if hp_pct <= 0.25 and not beast.get("phase_3", False):
        beast["phase_3"] = True
        beast["damage"] += 3
        beast["special_attack_chance"] = 0.4
        beast["special_attack_multiplier"] = 2.5
        beast["attack_messages"].extend([
            "The bat throws itself at you in a suicidal frenzy!",
            "Its wings tear as it slams into you!"
        ])
        suspense_print(
            "The creature should be dead.\n"
            "It isn’t.\n"
            "It comes anyway."
        )
def farm_house_attic(player):
    def build_beast(hp_bonus=0):
        if callable(get_enemy):
            try:
                beast = get_enemy("hell_genetically_altered_bat")
            except Exception:
                beast = {"name": "hell_genetically_altered_bat", "health": 18, "hit_chance": 70, "xp": 100}
        else:
            beast = {"name": "hell_genetically_altered_bat", "health": 18, "hit_chance": 70, "xp": 100}

        base_health = int(beast.get("health", 18))

        beast["max_health"] = max(1, base_health + hp_bonus)
        beast["health"] = beast["max_health"]

        beast.setdefault("hit_chance", 70)
        beast.setdefault("xp", 100)

        update_bat_phase(beast)
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
            suspense_print("The attic is finally quiet. The dust finally settles.")
            attic_after_beast_defeated(player)
            return False
        elif result == "run":
            suspense_print("You flee back down the ladder.")
            return False
        elif result == "lose":
            suspense_print("You have been defeated.")
            import sys
            sys.exit(0)
        else:
            # Unexpected result: continue loop safely
            suspense_print(f"Unexpected combat outcome: {outcome!r}")
            return True

    while True:
        suspense_print("You enter the attic. You see shadows dancing among the beams and a legion of eyes watching you.")

        # If the beast was woken earlier and not defeated yet, it attacks immediately with a challenge bump
        if player.get("beast_in_farm_house_woken_up", False) and not player.get("beast_in_farm_house_defeated", False):
            suspense_print("The beast is awake.\nIts anger shakes the rafters. It unfolds and charges!")
            beast = build_beast(hp_bonus=10)
            outcome = combats(player, beast)
            if not resolve_outcome(outcome, beast):
                return  # win/run/lose handled

        # If not woken and not defeated, present options
        if not player.get("beast_in_farm_house_defeated", False) and not player.get("beast_in_farm_house_woken_up", False):
            suspense_print("\n1) Prepare to fight the beast")
            suspense_print("2) Try to sneak attack the beast")
            suspense_print("3) Go back downstairs")
            suspense_print("I) Open inventory")

            choice = get_choice().strip().lower()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                player["beast_in_farm_house_woken_up"] = True
                suspense_print("You brace yourself for the beast's attack!")
                beast = build_beast()
                outcome = combats(player, beast)
                if not resolve_outcome(outcome, beast):
                    return

            elif choice == "2":
                suspense_print("You try to become the dark. The beast sees you with too many eyes.")
                try:
                    # Use a stealth check; success gives you a damage edge
                    if skill_check(player, "stealth", 50):
                        suspense_print("You catch it off guard and draw blood before it screams.")
                        beast = build_beast()
                        beast["health"] = max(1, beast["health"] - 5)
                    else:
                        suspense_print("You fail to disappear; its many eyes lock onto you.")
                        beast = build_beast()
                except Exception:
                    # Fallback if skill_check errors
                    beast = build_beast()

                outcome = combats(player, beast)
                if not resolve_outcome(outcome, beast):
                    return

            elif choice == "3":
                suspense_print("You back away, the attic swallowing your footsuspense_prints.")
                return
            else:
                suspense_print("Invalid choice")
                continue

        # Already defeated: show post-beast state and exit
        elif player.get("beast_in_farm_house_defeated", False):
            suspense_print("The attic is finally quiet. The dust finally settles.")
            attic_after_beast_defeated(player)
            return

        # Any other state: go to post-beast flow as a safe fallback
        else:
            attic_after_beast_defeated(player)
            return
def attic_beast_loot(player):
    gain_xp(player, 100)
    suspense_print("You deliver the final blow. A scream threads the beams and then comes apart.")
    player["beast_in_farm_house_defeated"] = True
    add_item(player, "sharp_wing_claw", 1)
    attic_after_beast_defeated(player)
    return
def attic_after_beast_defeated(player):
    while True:
        suspense_print("The bat-thing lies still, but its many eyes feel like stains.")
        suspense_print("1) Search the attic")
        suspense_print("2) Go back downstairs")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_attic_searched", False):
                suspense_print("You search the attic and find shells, a medkit, a key\n" 
                      "and some weary boots on the feet of one of the many corpses.")
                add_item(player, "shotgun_shells", 3)
                add_item(player, "medkit", 1)
                add_item(player, "weary_boots", 1)
                add_item(player, "old_farm_house_living_room_key", 1)
                player["farm_house_attic_searched"] = True
            else:
                suspense_print("Nothing else whispers to you here.")
        elif choice == "2":
            suspense_print("You go back downstairs.")
            farm_house_inside(player)
            return
        else:
            suspense_print("Invalid choice")
def farm_house_kitchen(player):
    while True:
        suspense_print("The kitchen smells like old metal and cold dust.")
        suspense_print("1) Search the fridge")
        suspense_print("2) Search the oven")
        suspense_print("3) Examine the counter")
        suspense_print("4) Go back")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("farm_house_fridge_searched", False):
                suspense_print("You search the fridge and find canned food and a strange fruit with creeping veins.")
                add_item(player, "canned_food", 2)
                add_item(player, "weird_fruit", 1)
                player["farm_house_fridge_searched"] = True
            else:
                suspense_print("The fridge is empty.")
        elif choice == "2":
            if not player.get("farm_house_oven_searched", False):
                suspense_print("You search the oven and find revolver rounds and shotgun shells.")
                add_item(player, "revolver_ammo", 2)
                add_item(player, "shotgun_shells", 2)
                if skill_check(player, "scavenging", 30):
                    suspense_print("Behind the oven’s back, a taped box, someone didn’t want this found.")
                    add_item(player, "coin", 15)
                player["farm_house_oven_searched"] = True
            else:
                suspense_print("The oven is empty.")
        elif choice == "3":
            if not player.get("farm_house_counter_searched", False):
                suspense_print("Two identical toasters sit side by side. One of them feels wrong.")
                toaster_check(player)
                return
            else:
                suspense_print("Nothing else to do here.")
        elif choice == "4":
            farm_house_inside(player)
            return
        else:
            suspense_print("Invalid choice")
def toaster_check(player):
    if skill_check(player, "perception", 25):
        suspense_print("On the right toaster: a faint smell of decay emanates.")
    suspense_print("1) Inspect the toaster on the right")
    suspense_print("2) Inspect the toaster on the left")
    suspense_print("3) Ignore it and go back")
    suspense_print("I) Open inventory")
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
        suspense_print("Invalid choice")
def right_toaster(player):
    suspense_print("You inspect the toaster on the right.")

    if player.get("toaster_metamorph_dead", False):
        suspense_print("The toaster is split open. Whatever nested inside is dead.")
        return

    while True:
        suspense_print("1) Stab the toaster")
        suspense_print("2) Shoot the toaster")
        suspense_print("3) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print("You plunge your knife in. Something bleeds.")
            # Use an inline enemy if get_enemy/fight_enemy aren’t available:
            alien = {"name": "small_metamorph", "health": 6, "hit_chance": 60, "xp": 50}
            combats(player, alien)
            if player["health"] > 0 and alien["health"] <= 0:
                player["toaster_metamorph_dead"] = True
                gain_xp(player, 50)
                add_item(player, "healing_salve", 1)
                return
            else:
                suspense_print("You collapse. The house swallows the scream.")
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
                suspense_print("You have no loaded ranged weapon.")
                continue

            suspense_print("You fire. The toaster EXPLODES. Dark matter paints the walls.")
            if not player.get("beast_in_farm_house_defeated", False):
                suspense_print("A blood-chilling scream answers from the attic. Something woke up.")
                player["beast_in_farm_house_woken_up"] = True

            alien = {"name": "small_metamorph", "health": 6, "hit_chance": 60, "xp": 50}
            combats(player, alien)
            if player["health"] > 0 and alien["health"] <= 0:
                player["toaster_metamorph_dead"] = True
                gain_xp(player, 50)
                add_item(player, "healing_salve", 1)
                return
            else:
                suspense_print("You collapse. The house swallows the scream.")
                return

        elif choice == "3":
            return

        else:
            suspense_print("Invalid choice")
def left_toaster(player):
    suspense_print("You inspect the toaster on the left. It looks normal.")
    suspense_print("After a moment, you decide to leave it alone.")  
    return

#OLD SURVIVOR_BASE

def mountain_tunnel(player):
    player["scene"] = "mountain_tunnel"
    
    # If door is already open, just enter
    if player.get("mountain_door_opened", False):
        suspense_print("the door is unlocked")
        suspense_print("1) Go inside the tunnel")
        suspense_print("2) Go to grove town")
        choice = get_choice()
        if choice == "1":
            mountain_tunnel_inside(player)
            return
        else:
            grove_town(player)
        return
    
    # Door is locked - check if player has key
    if player.get("inventory", {}).get("mountain_tunnel_key", 0) > 0:
        suspense_print("You use the mountain tunnel key. The lock clicks open.")
        player["mountain_door_opened"] = True
        remove_item(player, "mountain_tunnel_key", 1)
        mountain_tunnel_inside(player)
        return
    
    # No key - can't enter
    suspense_print("You arrive at the foot of a massive mountain. A locked tunnel door blocks the way.")
    suspense_print("The door won't budge. You need a key. You go back.")
    grove_town(player)
    return
def mountain_tunnel_inside(player):
  
    if (
        player.get("inventory", {}).get("radio_device", 0) > 0
        and not player.get("thomas_encountered", False)
    ):
        suspense_print(
            "As you turn to leave the tunnel, a figure steps into your path.\n"
            "“STOP RIGHT THERE!”\n"
            "“You have something that belongs to me.”\n\n"
            "A faded name tag hangs from his engineer jacket:\n"
            "THOMAS\n\n"
            "“Give me back the radio device and I *might* let you go.”"
        )

        player["thomas_encountered"] = True
        thomas_encounter(player)
        return

    suspense_print(
        "You enter the tunnel. Cold air crawls across your skin.\n"
        "Scratching noises echo from inside the walls.\n\n"
        "Ahead, the tunnel splits.\n"
        "Left: deep footprints pressed into the dirt.\n"
        "Right: a sloping tunnel descending into darkness."
    )

    while True:
        suspense_print("1) Go left")
        suspense_print("2) Go right")
        suspense_print("3) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            abandoned_outpost(player)
        elif choice == "2":
            underground_complex_entrance(player)
        elif choice == "3":
            mountain_tunnel(player)
            return
        else:
            suspense_print("Invalid choice.")
def thomas_encounter(player):
    suspense_print("Thomas watches you carefully, finger near the trigger.")

    while True:
        suspense_print("\n1) Explain that the leader sent you")
        suspense_print("2) Study Thomas closely")
        suspense_print("3) Attack Thomas")
        suspense_print("I) Open inventory")
        
        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # ---- TALK ----
        if choice == "1":
            suspense_print(
                "You explain that the leader sent you for the radio device.\n"
                "Thomas freezes.\n\n"
                "'They survived…?' he mutters.\n"
                "His weapon lowers slightly.\n\n"
                "'I almost finished it when they attacked the outpost.\n"
                "I thought everyone was dead.\n"
                "There were too many aliens… I couldn't check.'\n\n"
                "He exhales slowly.\n"
                "'If you really work for her, then keep it.\n"
                "Tell her I nearly opened the way to the complex under the outpost.\n"
                "I'll find her once I'm done.'"
            )
            player["thomas_allied"] = True
            player["thomas_encountered"] = True  # Mark as completed
            mountain_tunnel(player)  # Stay in tunnel instead of going to grove_town
            return

        # ---- PERCEPTION CHECK ----
        elif choice == "2":
            if player.get("thomas_seems_human", False) or player.get("thomas_suspicious", False):
                suspense_print(
                    "You've already studied Thomas.\n"
                    "Staring longer won't reveal anything new.\n"
                    "He notices."
                )
                continue

            if skill_check(player, "perception", 30):
                suspense_print(
                    "You study Thomas closely.\n"
                    "Nothing stands out.\n"
                    "If he's something else… he hides it well."
                )
                player["thomas_seems_human"] = True
                # Remove the continue here - let it fall through to show menu again
            else:
                suspense_print(
                    "You try to read him.\n"
                    "Your instincts whisper that something is wrong.\n"
                    "But you can't prove it."
                )
                player["thomas_suspicious"] = True
            # No continue - player should see the options again after examining

        # ---- COMBAT ----
        elif choice == "3":
            suspense_print("The silence shatters. The fight begins.")
            thomas = get_enemy("thomas")
            won = fight_enemy(player, thomas)

            if won:
                suspense_print(
                    "Thomas collapses, blood soaking the concrete.\n"
                    "His eyes stay open.\n\n"
                    "You feel a stab of guilt.\n"
                    "But the mission matters more."
                )
                player["thomas_killed"] = True
                player["thomas_encountered"] = True  # Mark as completed
            mountain_tunnel_inside(player)  # Return to tunnel after combat
            return

        else:
            suspense_print("Invalid choice.")           
def abandoned_outpost(player):
    suspense_print(
        "From afar, you spot an abandoned outpost.\n"
        "A torn tent. A strange device at the center.\n"
        "Bodies scattered across the ground."
    )

    if skill_check(player, "perception", 30):
        suspense_print("Some of the bodies appear to be breathing. Very slowly.")

    while True:
        suspense_print("1) Approach the tent")
        suspense_print("2) Examine the device")
        suspense_print("3) Search the bodies")
        suspense_print("4) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("abandoned_outpost_tent_searched"):
                suspense_print(
                    "Inside the tent, you find a journal, scattered supplies and a respirator."
                )
                add_item(player, "abandoned_outpost_journal", 1)
                add_item(player, "revolver_ammo", 4)
                add_item(player, "medkit", 1)
                add_item(player, "respirator", 1)

                suspense_print(
                    "Journal:\n"
                    "Another shooting happened.\n"
                    "A mother shot her son. Said his eyes moved wrong.\n\n"
                    "Nobody trusts anyone anymore.\n"
                    "Thomas is building a device to interfere with their morphing.\n"
                    "I hope it works."
                )

                player["abandoned_outpost_tent_searched"] = True
            else:
                suspense_print("The tent is empty now.")

        elif choice == "2":

            # Case 1: device already safe to loot
            if not player.get("abandoned_outpost_device_examined") and player.get("abandoned_outpost_center_body_searched", False):
                suspense_print(
                    "The device looks like a high-frequency radio emitter.\n"
                    "It’s dead. Burned out."
                )
                add_item(player, "radio_device", 1)
                player["abandoned_outpost_device_examined"] = True
                continue

            # Case 2: trap + ambush
            if not player.get("abandoned_outpost_device_examined") and not player.get("abandoned_outpost_center_body_searched", False):
                suspense_print(
                    "The device looks like a high-frequency radio emitter.\n"
                    "It hums faintly, but seems inactive.\n"
                    "As you step closer, a nearby corpse jerks violently.\n"
                    "Something grabs your feet and drags you backward!"
                )

                enemies = [
                    get_enemy("small_metamorph"),
                    get_enemy("small_metamorph"),
                    get_enemy("small_metamorph"),
                ]

                won = fight_multiple_enemies(player, enemies)

                if not won:
                    suspense_print("You barely escape, your heart hammering in your chest.")
                    return

                suspense_print(
                    "The creatures lie still.\n"
                    "Silence returns — thick and unnatural.\n"
                    "You force yourself to approach the device again."
                )

                suspense_print(
                    "The device looks like a high-frequency radio emitter.\n"
                    "It’s dead. Burned out."
                )

                add_item(player, "radio_device", 1)
                randomized_bonus_loot(
                    player,
                    {
                        "coin": (10, 15),
                        "alien_power_cell": (1, 2),
                        "revolver_ammo": (2, 5),
                    }
                )
                player["abandoned_outpost_center_body_searched"] = True
                player["abandoned_outpost_device_examined"] = True
                continue



        elif choice == "3":
            body_search(player)

        elif choice == "4":
            mountain_tunnel_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
def body_search(player):
    player["scene"] = "abandoned_outpost_body_search"
    if skill_check(player, "perception", 30) and not player.get("abandoned_outpost_right_body_seen_moving"):
        suspense_print("One of the bodies on the right twitches.")
        player["abandoned_outpost_right_body_seen_moving"] = True

    while True:
        suspense_print("1) Search body on the left")
        suspense_print("2) Search body on the right")
        suspense_print("3) Search bodies near the device")
        suspense_print("4) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            left_body_search(player)

        elif choice == "2":
            right_body_search(player)

        elif choice == "3":
            center_body_search(player)

        elif choice == "4":
            abandoned_outpost(player)
            return

        else:
            suspense_print("Invalid choice.")    
def left_body_search(player):
    if  player.get("abandoned_outpost_left_body_searched", False):
        suspense_print("You already searched this body.")
        body_search(player)
        return

    while True:
        suspense_print("1) Examine closely")
        suspense_print("2) Sneak in and stab the body")
        suspense_print("3) Shoot the body")
        suspense_print("4) search the body")
        suspense_print("5) Ignore and go back")
        suspense_print("I) Open inventory")
        
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("You examine the body closely.\n"
                           "it looks long dead, but you notice a small pouch tied to its belt.\n"
                           "and weird fungus growths on its skin.")
            continue  # Add this
        elif choice == "2":
            if skill_check(player, "stealth", 30):
                suspense_print("You sneak up and stab the body.\n"
                               "It doesn't react, you quickly search the pouch.")
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(player, {"coin": (5, 10), "revolver_ammo": (1, 3)})
                add_item(player,"abandoned_outpost_left_body_note",1) 
                suspense_print("thomas still havent find a way to get the the complex under the outpost\n"
                "he say there is someting important down there\n"
                "i just hope he is right and we can get out of this hell\n"   
                "apparently it was an old secret military base before the blast")
                player["abandoned_outpost_left_body_searched"] = True
                return
            else:
                suspense_print("As you approach, you stumble on a rock.\n"
                               "nothing happens, its already dead.\n")
                continue  # Changed from return to allow retry
        elif choice == "3":
            suspense_print("You shoot the body.\n"
                           "The body remains still, you search the pouch.")
            add_item(player, "healing_salve", 2)
            randomized_bonus_loot(player, {"coin": (5, 10), "revolver_ammo": (1, 3)})
            add_item(player,"abandoned_outpost_left_body_note",1)  # Remove duplicate
            suspense_print("thomas still havent find a way to get the the complex under the outpost\n"
            "he say there is someting important down there\n"
            "i just hope he is right and we can get out of this hell\n"   
            "apparently it was an old secret military base before the blast")
            player["abandoned_outpost_left_body_searched"] = True
            return
             
        elif choice == "4":
            suspense_print("You search the left body carefully.")
            add_item(player, "revolver_ammo", 3)
            add_item(player, "coin", 10)
            add_item(player,"abandoned_outpost_left_body_note",1) 
            suspense_print("thomas still havent find a way to get the the complex under the outpost\n"
            "he say there is someting important down there\n"
            "i just hope he is right and we can get out of this hell\n"   
            "apparently it was an old secret military base before the blast")     
            player["abandoned_outpost_left_body_searched"] = True
            return
        elif choice == "5":
            body_search(player)
            return
        else:
            suspense_print("Invalid choice.")
def right_body_search(player):
    if player.get("abandoned_outpost_right_body_searched", False):
        suspense_print("You already searched this body.")
        body_search(player)
        return

    if player.get("abandoned_outpost_right_body_seen_moving", False):
        suspense_print("You remember seeing this body move slightly.")

    while True:
        suspense_print("1) Examine closely")
        suspense_print("2) Sneak in and stab the body")
        suspense_print("3) Shoot the body")
        suspense_print("4) Ignore and go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "You examine the body closely.\n"
                "Its chest rises and falls — very slowly."
            )

        elif choice == "2":
            if skill_check(player, "stealth", 40):
                suspense_print(
                    "You creep forward, blade raised.\n"
                    "One precise strike.\n"
                    "The body goes completely still."
                )
                player["abandoned_outpost_right_body_searched"] = True
                add_item(player, "healing_salve", 1)
                randomized_bonus_loot(player, {"coin": (10, 15), "revolver_ammo": (2, 5)})
                return
            else:
                suspense_print(
                    "You step on loose debris.\n"
                    "The body’s eyes snap open."
                )
                small_metamorph = get_enemy("small_metamorph")
                won = fight_enemy(player, small_metamorph)
                if won:
                    suspense_print("The creature collapses. You search the remains.")
                    player["abandoned_outpost_right_body_searched"] = True
                    add_item(player, "healing_salve", 1)
                    randomized_bonus_loot(
                        player,
                        {"coin": (10, 15), "revolver_ammo": (2, 5), "shotgun_shells": (2, 5)}
                    )
                    return
                else:
                    suspense_print("Everything goes dark.")
                    exit(0)

        elif choice == "3":
            suspense_print(
                "You fire a shot.\n"
                "The body shrieks and twists unnaturally."
            )
            remove_item(player, "revolver_ammo", 1)
            small_metamorph = get_enemy("small_metamorph")
            small_metamorph["health"] -= 4
            won = fight_enemy(player, small_metamorph)
            if won:
                suspense_print("The thing finally stops moving.")
                player["abandoned_outpost_right_body_searched"] = True
                add_item(player, "healing_salve", 1)
                randomized_bonus_loot(
                    player,
                    {"coin": (10, 15), "revolver_ammo": (2, 5), "shotgun_shells": (2, 5)}
                )
                return
            else:
                suspense_print("Everything goes dark.")
                exit(0)

        elif choice == "4":
            body_search(player)
            return

        else:
            suspense_print("Invalid choice.")
def center_body_search(player):
    if player.get("abandoned_outpost_center_body_searched", False):
        suspense_print("You already searched these bodies.")
        body_search(player)
        return

    if skill_check(player, "perception", 40):
        suspense_print("You notice the bodies are subtly moving.")

    while True:
        suspense_print("1) Examine closely")
        suspense_print("2) Sneak in and stab the bodies")
        suspense_print("3) Shoot the bodies")
        suspense_print("4) Ignore and go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "Their breathing is slow.\n"
                "Too synchronized."
            )

        elif choice == "2":
            suspense_print("You steady your breathing and move in.")

            first_success = skill_check(player, "stealth", 30)
            second_success = skill_check(player, "stealth", 40)

            if first_success and second_success:
                suspense_print(
                    "Your blade flashes.\n"
                    "One body falls.\n"
                    "Then another.\n"
                    "No sound. No movement."
                )
                player["abandoned_outpost_center_body_searched"] = True
                add_item(player, "healing_salve", 3)
                randomized_bonus_loot(
                    player,
                    {"coin": (20, 30), "revolver_ammo": (4, 7)}
                )
                gain_xp(player, 50)
                return

            suspense_print(
                "You strike — but something goes wrong.\n"
                "A body twitches.\n"
                "Then moves."
            )

            enemies = []

            if not first_success:
                enemies.append(get_enemy("small_metamorph"))

            if not second_success:
                enemies.append(get_enemy("small_metamorph"))

            suspense_print(f"{len(enemies)} creature{'s' if len(enemies) > 1 else ''} rise to attack!")

            won = fight_multiple_enemies(player, enemies)
            if won:
                suspense_print("The last twitch fades into silence.")
                player["abandoned_outpost_center_body_searched"] = True
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(
                    player,
                    {"coin": (15, 20), "revolver_ammo": (3, 6), "shotgun_shells": (3, 6)}
                )
                return
            else:
                suspense_print("Everything goes dark.")
                exit(0)


        elif choice == "3":
            suspense_print("Gunfire echoes violently.")
            remove_item(player, "revolver_ammo", 1)
            enemies = [
                get_enemy("small_metamorph"),
                get_enemy("small_metamorph"),
            ]
            enemies[0]["health"] -= 4
            won = fight_multiple_enemies(player, enemies)
            if won:
                suspense_print("The echoes fade.")
                player["abandoned_outpost_center_body_searched"] = True
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(
                    player,
                    {"coin": (15, 20), "revolver_ammo": (3, 6), "shotgun_shells": (3, 6)}
                )
                return
            else:
                suspense_print("Everything goes dark.")
                exit(0)

        elif choice == "4":
            body_search(player)
            return

        else:
            suspense_print("Invalid choice.")

 #       


#SECRET UNDERGROUND COMPLEX
def underground_complex_entrance(player):
    suspense_print(
        "You descend into the darkness.\n"
        "The air grows colder.\n"
        "Faint lights flicker ahead.\n\n"
        "You arrive at a massive steel door, half-buried in rock.\n"
        
    )

    while True:
        suspense_print("1) Try to open the door")
        suspense_print("2) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if "mountain_base_secret_lab_key" in player.get("inventory", {}):
                suspense_print(
                    "You use the secret lab key.\n"
                    "The lock clicks open."
                    "You push against the door.\n"
                "It resists, then slowly grinds open.\n\n"
                )
                underground_complex_inside(player)
                return
            suspense_print(
                "The door is sealed tight.\n"
                "You need a special key to open it."
            )
            continue
           

        elif choice == "2":
            mountain_tunnel_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
    #___check___zone
def underground_complex_inside(player):
    suspense_print(
        "You step into the underground complex.\n"
        "Dim lights flicker on the walls.\n"
        "Strange machinery hums softly.\n\n"
        "The air is thick with the scent of oil and metal.\n"
        "You feel a strange energy pulsing through the place."
    )

    while True:
        suspense_print("1) Advance through the corridors")
        suspense_print("2) Carefully check the corridors")
        suspense_print("3) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            _handle_corridor_advance(player)
            return

        elif choice == "2":
            _handle_corridor_check(player)

        elif choice == "3":
            underground_complex_entrance(player)
            return

        else:
            suspense_print("Invalid choice.")
def _handle_corridor_advance(player):
    if player.get("has_seen_blinking_red_light", False):
        corridors_with_blinking_red_light(player)
        return

    suspense_print(
        "You advance through the corridors when suddenly an alarm blares!\n"
        "Two automated turrets emerge from the walls, locking onto you!"
    )

    enemies = [get_enemy("turret"), get_enemy("turret")]
    won = fight_enemy(player, *enemies)

    if won:
        suspense_print("The turrets collapse into heaps of twisted metal.")
        gain_xp(player, 100)
        add_item(player, "rifle_ammo", 10)
        randomized_bonus_loot(
            player,
            {"coin": (20, 30), "alien_power_cell": (1, 2)}
        )
        underground_complex_main_hall(player)
    else:
        suspense_print("Everything goes dark.")
        exit(0)
def _handle_corridor_check(player):
    if skill_check(player, "perception", 30):
        suspense_print(
            "Your eyes catch a faint blinking red light hidden in the wall."
        )
        player["has_seen_blinking_red_light"] = True

    elif skill_check(player, "intelligence", 50):
        suspense_print(
            "You recognize the layout—this corridor hides an automated defense system."
        )
        player["has_seen_blinking_red_light"] = True

    else:
        suspense_print("You find nothing unusual.")
def corridors_with_blinking_red_light(player):
    suspense_print(
        "You focus on the blinking red light.\n"
        "It’s part of a concealed turret system.\n"
        "A damaged control panel hums beside it."
    )

    while True:
        suspense_print("1) Shoot the control panel")
        suspense_print("2) Throw something to bait the turrets")
        suspense_print("3) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "You fire at the control panel.\n"
                "Sparks erupt as the turret system shuts down."
            )
            gain_xp(player, 50)
            add_item(player, "rifle_ammo", 10)
            randomized_bonus_loot(
                player,
                {"coin": (20, 30), "alien_power_cell": (1, 2)}
            )
            underground_complex_main_hall(player)
            return

        elif choice == "2":
            suspense_print(
                "You toss debris down the corridor.\n"
                "A turret emerges—targeting the noise."
            )

            won = fight_enemy(player, get_enemy("turret"))
            if won:
                suspense_print("The turret crashes to the ground, lifeless.")
                add_item(player, "rifle_ammo", 10)
                randomized_bonus_loot(
                    player,
                    {"coin": (20, 30), "alien_power_cell": (1, 2)}
                )
                underground_complex_main_hall(player)
                return
            else:
                suspense_print("Everything goes dark.")
                exit(0)

        elif choice == "3":
            underground_complex_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
def underground_complex_main_hall(player):
    suspense_print("you arived in a big hall,before you stand two rusted bots the look inactive"
                   "you also see a stairs going up,some going down,you also see a room going to the right ")
    #finish later
 #

#need to finish underground complex main hall
#road to bastion
def wasteland_4(player):
    if player.get(("wasteland_4_count"), 0) >= 5:   
        suspense_print(
            "You feel a strange familiarity with this part of the wasteland.\n"
            "It's as if you've been here many times before."
        )

    count = player.get("wasteland_4_count", 0) + 1

    if (
        count > 1
        and player.get("found_invisible_alien", False)
        and not player.get("invisible_alien_encountered", False)
    ):
        suspense_print(
            "As you walk, the alien you saw before appears where you last noticed it.\n"
            "It hasn’t seen you yet.\n"
            "What do you do?"
        )
        invisible_alien_encounter(player)
        return

    suspense_print(
        "You're finally out of the hospital.\n"
        "You take a breath of fresh air.\n"
        "The air tastes of rust and sulfur.\n\n"
        "A path leads toward a steaming city in the distance.\n"
        "You start walking toward it."
    )

    while True:
        suspense_print("1) Continue toward the city")
        suspense_print("2) Look around")
        suspense_print("3) Go  to the hospital")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):

            continue

        if choice == "1":
            count += 1
            way_toward_bastion(player)
            
            return

        elif choice == "2":
            if not player.get("found_invisible_alien", False) and skill_check(player, "perception", 30):
                suspense_print(
                    "You notice a strange distortion in the air.\n"
                    "Something invisible shifts… then vanishes.\n"
                    "A chill runs down your spine."
                )
                player["found_invisible_alien"] = True
            else:
                suspense_print("You scan the wasteland, but see nothing unusual.")

        elif choice == "3":
            count += 1
            hospital_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
def invisible_alien_encounter(player):
    player["invisible_alien_encountered"] = True

    suspense_print("The invisible alien notices you and starts moving toward you.")

    while True:
        if player.get("has_eaten_10_fruits", False):
            suspense_print(
                "The alien tilts its head.\n"
                "It seems to recognize you.\n\n"
                "Slowly, it relaxes.\n"
                "It places something at your feet before pointing toward the horizon.\n"
                "Then it fades from sight."
            )
            player["invisible_alien_ally"] = True
            add_item(player, "alien_power_cell", 1)
            add_item(player, "revolver_ammo", 6)
            gain_xp(player, 40)
            return

        suspense_print("1) Try to communicate")
        suspense_print("2) Attack it")
        suspense_print("3) Run away")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if skill_check(player, "charisma", 40):
                suspense_print(
                    "You speak calmly.\n"
                    "The alien hesitates… then vanishes into the wasteland."
                )
                gain_xp(player, 20)
                return
            else:
                suspense_print("The alien recoils violently and attacks!")
                alien_metamorph = get_enemy("alien_metamorph")
                won = fight_enemy(player, alien_metamorph)
                if won:
                    suspense_print("The creature collapses, its outline finally visible.")
                    add_item(player, "alien_energy_cell", 1)
                    randomized_bonus_loot(
                        player,
                        {"coin": (10, 20), "alien_power_cell": (1, 2)}
                    )
                    return
                exit(0)

        elif choice == "2":
            suspense_print("You strike first.")
            alien_metamorph = get_enemy("alien_metamorph")
            won = fight_enemy(player, alien_metamorph)
            if won:
                suspense_print("The alien dissolves into shimmering fragments.")
                add_item(player, "alien_energy_cell", 1)
                randomized_bonus_loot(
                    player,
                    {"coin": (10, 20), "alien_power_cell": (1, 2)}
                )
                return
            exit(0)

        elif choice == "3":
            suspense_print("You retreat, heart pounding.")
            return

        else:
            suspense_print("Invalid choice.")
def way_toward_bastion(player):
    if player.get("beast_in_way_to_bastion_defeated", False):
        way_toward_bastion_after_beast(player)
        return

    suspense_print(
        "You continue walking toward the town.\n"
        "The taste of rust and sulfur grows stronger.\n"
        "Dark spores drift through the air.\n"
        "The town looms closer…\n\n"
        "Then you hear a growl behind you."
    )

    while True:
        suspense_print("1) Turn around and face the threat")
        suspense_print("2) Keep running toward the town")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "You turn around.\n"
                "A cyborg stands before you — metal fused with flesh.\n"
                "Its face is wet with tears.\n"
                "There is still a man inside."
            )

            cyborg = get_enemy("weeping_cyborg")
            won = fight_enemy(player, cyborg)

            if won:
                suspense_print(
                    "The cyborg collapses.\n"
                    "As the metal stills, all you see is a broken man beneath it."
                )
                gain_xp(player, 100)
                player["beast_in_way_to_bastion_defeated"] = True
                add_item(player, "alien_implant", 1)
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(player, {"coin": (20, 30)})

                way_toward_bastion_after_beast(player)
                return

            suspense_print("Everything goes dark.")
            game_over(player)
            return

        elif choice == "2":
            suspense_print(
                "You try to ignore the growl and keep walking.\n"
                "It gets closer.\n"
                "Closer.\n\n"
                "A sharp pain pierces your back.\n"
            )
            player["health"] -= 10
            if player["health"] <= 0:
                suspense_print("You collapse, darkness swallowing you whole.")
                game_over()
                return
            cyborg = get_enemy("weeping_cyborg")
            won = fight_enemy(player, cyborg)
            if won:
                suspense_print(
                    "The cyborg collapses.\n"
                    "As the metal stills, all you see is a broken man beneath it."
                )
                gain_xp(player, 100)
                player["beast_in_way_to_bastion_defeated"] = True
                add_item(player, "alien_implant", 1)
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(player, {"coin": (20, 30)})

                way_toward_bastion_after_beast(player)
                return

            suspense_print("Everything goes dark.")
            game_over()
            return


                
            

        else:
            suspense_print("Invalid choice.")
def way_toward_bastion_after_beast(player):
    player["way_toward_bastion_after_beast_count"] = player.get("way_toward_bastion_after_beast_count", 0) + 1
    if skill_check(player, "luck", 30, visible=False) and not player.get("way_toward_bastion_after_beast_luck_check_passed", False):
        suspense_print(
            "As you walk, you notice a glint in the dirt.\n"
            "You bend down and find a small pouch of coins."
        )
        add_item(player, "coin", 25)
        gain_xp(player, 20)
        player["way_toward_bastion_after_beast_luck_check_passed"] = True
    if player.get("way_toward_bastion_after_beast_count", 0) >= 3 and not player.get("wonded_woman_rescued", False):
        suspense_print(
            "as you walk you feel see a wonded woman sitting against a rock\n"
            "she looks at you with hope in her eyes"
            "\"please help me...\" she says\n"
            "you approach her carefully"
        )
        wonded_woman_encounter(player)
        return

    suspense_print(
        "With the threat gone, you continue toward the town.\n"
        "you arrived at the gates of Bastion.\n"
        "under a massive wall, guarded by armed sentries.\n"
        "You have arrived at Bastion."
    )

    bastion_entrance(player)
def wonded_woman_encounter(player):

    if skill_check(player, "perception", 40, visible=False):
        suspense_print(
            "You notice something moving under her skin.\n"
            "I don't think she is one of us"
        )
    
    while True:
        suspense_print("1) Help her")
        suspense_print("2) Ignore her and continue to Bastion")
        suspense_print("3) Shoot her")
        
        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "you try to save her when suddenly she morphs into a alien creature\n"
            )
            alien_metamorph = get_enemy("alien_metamorph")
            won = fight_enemy(player, alien_metamorph)
            if won:
                suspense_print("The creature collapses, its outline finally visible.")
                add_item(player, "alien_energy_cell", 1)
                add_item(player, "tactical_boots",1)
                randomized_bonus_loot(
                    player,
                    {"coin": (10, 20), "alien_power_cell": (1, 2)}
                )
                player["wonded_woman_rescued"] = True
                way_toward_bastion_after_beast(player)
                return
            else:
                game_over()
                return

        elif choice == "2":
            suspense_print("you ignore her and continue to bastion")
            player["wonded_woman_rescued"] = True

            bastion_entrance(player)
            return
            
        elif choice == "3":
            alien_metamorph = get_enemy("alien_metamorph")

            if player_attack(player, alien_metamorph):
                suspense_print("Your shot hits before it can react!")

            suspense_print(
                "You shoot her and she falls to the ground.\n"
                "Her body twists and morphs into an alien creature that lunges at you!"
            )

            alien_metamorph["health"] = max(0, alien_metamorph["health"] - 6)

            won = fight_enemy(player, alien_metamorph)
            if won:
                suspense_print("The creature collapses, its outline finally visible.")
                add_item(player, "alien_energy_cell", 1)
                add_item(player, "tactical_boots",1)
                randomized_bonus_loot(
                    player,
                    {"coin": (10, 20), "alien_power_cell": (1, 2)}
                )
                player["wonded_woman_rescued"] = True
                way_toward_bastion_after_beast(player)
                return
            else:
                game_over()
                return

        else:
            suspense_print("Invalid choice.")
          

#BASTION CITY
def bastion_entrance(player):
    if player.get("has_rescued_bastion_scout", False) and not player.get("bastion_badge_awarded", False):
        suspense_print(
            "The guards recognize you immediately.\n"
            "\"Welcome back,\" one says.\n"
            "\"The scout made it through thanks to you.\""
        )

        suspense_print(
            "The guard hands you a small metal badge.\n"
            "\"This grants you limited access beneath Bastion.\""
        )

        add_item(player, "bastion_access_badge", 1)
        gain_xp(player, 150)
        player["bastion_badge_awarded"] = True

        suspense_print(
            "\"Follow us,\" the guard says.\n"
            "You are escorted beneath the massive walls."
        )

        bastion_inside(player)
        return
    # Track visits
    player["bastion_entrance_count"] = player.get("bastion_entrance_count", 0) + 1

    # --- Authorized entry ---
    if "bastion_access_badge" in player.get("inventory", {}):
        suspense_print(
            "The guards scan your badge.\n"
            "A green light flashes.\n\n"
            "\"Access granted,\" one of them says.\n"
            "The massive gates open fully.\n\n"
            "You are allowed into Bastion."
        )
        while True:
        
            suspense_print("1) Enter")
            suspense_print("2) go toward hospital")
            suspense_print("3) Go toward old factory")
            suspense_print("4) Go in alien land")
            if "bastion_map" in player.get("inventory", {}):
                suspense_print("5) go toward twisted forest")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                bastion_inside(player)
                return
            elif choice =="2":
                wasteland_4(player)
                return
            elif choice=="3":
                old_factory_way(player)
                return
            elif choice == "4":
                alien_land_1(player)
                return
            elif choice == "5":
                twisted_forest(player)
                return
            else:
                suspense_print("incorect choice")

    # --- Repeat visit → job offer ---
    if player.get("bastion_entrance_visited", False) and player["bastion_entrance_count"] >= 4:
        suspense_print(
            "As you approach the gates again, a guard recognizes you.\n"
            "\"Still alive?\"\n"
            "\"If you want real work, talk to us.\""
        )
        Bastion_inside_job_offer(player)
        return

    # --- First visit ---
    if not player.get("bastion_entrance_visited", False):
        suspense_print(
            "As you approach the gates of Bastion, a guard steps forward.\n"
            "“Halt! State your business.”"
        )

    while True:
        
        suspense_print("1) Explain you need to pass through")
        suspense_print("2) Ask where you are")
        if player.get("bastion_scout_quest_accepted", False):
            suspense_print("4) go east toward the old factory")
        suspense_print("3) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            
            suspense_print(
                "“We can’t let just anyone in,” the guard says.\n"
                "“Only military personnel are allowed.”\n\n"
                "“For a fee… we can escort you through.”"
            )

            while True:
                suspense_print("1) Pay 50 coins")
                suspense_print("2) Refuse and go back")

                sub_choice = get_choice()
                if handle_global_input(sub_choice, player):
                    continue

                if sub_choice == "1":
                    if not player.get("bastion_gard_paid", False):
                        if skill_check(player, "charisma", 40):
                            suspense_print("You convince the gard to let you pass for free.")
                            player["bastion_gard_paid"] = True
                            player["bastion_entrance_visited"] = True
                            alien_land_1(player)
                            return
                        if player.get("inventory", {}).get("coin", 0) >= 50:
                            remove_item(player, "coin", 50)
                            suspense_print(
                                "The guard nods.\n\n"
                                "You are escorted through a narrow corridor beneath Bastion’s walls.\n"
                                "The city itself remains sealed off above you.\n"
                                "Armed guards watch your every step."
                            )
                            player["bastion_entrance_visited"] = True
                            player["bastion_gard_paid"] = True
                            alien_land_1(player)
                            return
                        
                        else:
                            suspense_print("You don’t have enough coins.")
                            continue
                    else:
                        suspense_print("the guard says youre clear to pass")
                        alien_land_1(player)
                        return
                elif sub_choice == "2":
                    way_toward_bastion(player)
                    return
                else:
                    suspense_print("Invalid choice.")

        elif choice == "2":
            suspense_print(
                "“This is Bastion,” the guard says.\n"
                "“The last stronghold before alien territory.”\n"
                "“And you’re not cleared to enter it.”"
            )
            continue

        elif choice == "3":
            wasteland_4(player)
            return
        elif choice == "4" and player.get("bastion_scout_quest_accepted", False):
            old_factory_way(player)
            return
        else:
            suspense_print("Invalid choice.")  
def Bastion_inside_job_offer(player):
    # Prevent re-offering the same quest
    if player.get("bastion_scout_quest_accepted", False):
        suspense_print(
            "The guards are already waiting for news about the missing scout.\n"
            "\"Find him,\" the leader says. \"Dead or alive.\""
        )
        return

    suspense_print(
        "The leader of the guards approaches you.\n\n"
        "\"You’ve been hanging around our walls long enough,\" he says.\n"
        "\"Most of our men are tied up holding back alien advances.\"\n\n"
        "\"One of our scouts went missing near the old factory east of Bastion.\"\n"
        "\"Find him, and we’ll pay you 100 coins.\""
    )

    while True:
        suspense_print("1) Accept the job")
        suspense_print("2) Refuse and go back")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "The guard nods.\n\n"
                "\"The scout was last seen near the old factory east of Bastion.\"\n"
                "\"Be careful — the area is crawling with aliens.\"\n\n"
                "You head toward the factory."
            )

            player["bastion_scout_quest_accepted"] = True
            player["bastion_entrance_count"] = 0  # reset nag counter safely

            old_factory_way(player)
            return

        elif choice == "2":
            suspense_print(
                "\"Suit yourself,\" the guard says.\n"
                "\"But don’t expect the gates to open for free.\""
            )
            wasteland_4(player)
            return

        else:
            suspense_print("Invalid choice.")
def bastion_inside(player):
    player["scene"] = "bastion_inside"
    if player.get("has_rescued_bastion_scout", False) and not player.get("complited_bastion_scout_quest", False):
        suspense_print(
            "You return to Bastion with the rescued scout.\n"
            "The guards rush to meet you."
        )

        suspense_print(
            "\"You found him!\" the leader exclaims.\n"
            "\"Thank you. Here’s your reward.\n"
            "there is also an old exoskeleton model that i think you can use\""
        )
        add_item(player, "coin", 100)
        add_item(player, "old_exoskeleton_model", 1)
        gain_xp(player, 200)
        player["complited_bastion_scout_quest"] = True

        
        suspense_print(
        "You step into Bastion.\n"
        "The air is thick with the scent of metal and oil.\n"
        "Guards patrol the streets, eyeing you warily.\n\n"
        "You see soldiers training in a courtyard.\n"
        "heavy machinery clanks in the distance.\n"
        "and stairs leading down to underground levels."
    )
    while True:
        suspense_print("1) Explore the courtyard")
        suspense_print("2) Check out the heavy machinery")
        suspense_print("3) Go down to the underground levels")
        suspense_print("4) Go outside")
        
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "You walk into the courtyard.\n"
                "Soldiers stop their training and watch you closely.\n"
                "A sergeant approaches you."
            ) 
            sergeant_dialogue(player)


        elif choice == "2":
            suspense_print(
                "You approach the heavy machinery.\n"
                "It’s a mix of alien tech and human engineering.\n"
                "A technician notices you and waves you over."
            )
            engineer_dialogue(player)
        elif choice == "3":
            
                if  not player.get("bastion_full_clearance", False):
                    suspense_print(
                        "A guard stops you.\n"
                        "\"That badge only grants access to the lower levels.\""
                    )
                else:
                    suspense_print(
                        "You head up to the main chambers of Bastion.\n"
                        "The air grows cooler and the hum of machinery louder.\n"
                        "you see a comand center with several guards and a lab area"
                    )
                    Bastion_main(player)
                    # Implement underground Bastion levels here
        elif choice == "4":
            bastion_entrance(player)
            return
        else:
            suspense_print("Invalid choice.")    
def Bastion_main(player):

    #todo
    pass  
#FINISH BASTION MAIN
def sergeant_dialogue(player):
    
    if not player.get("became_bastion_scout", False):
        sergeant_recruitment(player)
    elif player.get("bastion_active_quest") == "scout_outpost":
        sergeant_scout_outpost(player)
    else:
        sergeant_idle(player)
def sergeant_recruitment(player):
    suspense_print(
        "\"Welcome to Bastion,\" the sergeant says.\n"
        "\"We could use someone with your skills.\"\n\n"
        "\"You’ve already proven yourself.\n"
        "I’d like to offer you a position as a scout.\"\n\n"
        "\"Scouts are vital to our survival.\n"
        "We send them beyond the walls to track alien movement and resources.\""
    )
    while True:  
        suspense_print("1) Accept the position as a scout")
        suspense_print("2) Decline the position")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "\"Excellent,\" the sergeant says.\n"
                "\"i already have a mission for you.\"\n"
                "i need you to go into alien territory and scout an old abandoned military outpost\n"
                "report back any findings and try to gather any useful resources you can find there\n\""
                "and i got something for you if you manage to clear the outpost"
            )
            player["became_bastion_scout"] = True
            player["bastion_active_quest"] = "scout_outpost"
            player["bastion_rank"] = 1
            gain_xp(player, 100)
            return

        elif choice == "2":
            suspense_print(
                "\"Very well,\" the sergeant says.\n"
                "\"Feel free to explore Bastion.\""
            )
            return

        else:
            suspense_print("Invalid choice.") 
def sergeant_scout_outpost(player):
    

    # FULL CLEAR PATH (violent)
    if player.get("enemy_in_outpost_killed_count", 0) >= 10:
        suspense_print(
            "\"You did it!\" the sergeant exclaims.\n"
            "\"The outpost is secure thanks to you.\"\n"
            "\"Bastion won’t forget this.\""
        )
        add_item(player, "combat_knife", 1)
        add_item(player, "coin", 200)
        gain_xp(player, 200)

        player["scout_outpost_completed"] = True
        player["bastion_active_quest"] = "private_mission"
        player["bastion_rank"] += 1
        return

    # DATA EXTRACTION PATH (stealth / smart)
    elif player.get("outpost_data_count", 0) >= 3:
        suspense_print(
            "\"You’re back — and alive,\" he says.\n"
            "\"This data will save lives.\""
        )
        add_item(player, "coin", 150)
        gain_xp(player, 150)

        player["scout_outpost_completed"] = True
        player["bastion_active_quest"] = "private_mission"
        player["bastion_rank"] += 1
        return

    # NOT DONE YET
    else:
        suspense_print(
            "\"The outpost is still out there,\" the sergeant says.\n"
            "\"Bring back anything you find.\""
        )
        return

def sergeant_private_mission(player):
    pass

#todo



def sergeant_idle(player):
    suspense_print(
        "\"Keep your eyes open out there,\" the sergeant says.\n"
        "\"The aliens are always watching.\""
    )
  #chech
def engineer_dialogue(player):
    given = player.get("has_given_alien_tech_to_engineer", 0)

    # --- Milestone dialogue ---
    if given >= 10 and not player.get("engineer_reward_10_given", False):
        suspense_print(
            "The engineer looks up from a half-disassembled turret.\n"
            "His eyes widen as he sees the pile of alien tech you brought.\n\n"
            "\"By the rusted gears of Bastion…\"\n"
            "\"With parts like these, I’ve reinforced the walls, upgraded the guns,\n"
            "and patched weaknesses we didn’t even know we had.\"\n\n"
            "He wipes grease from his hands and nods at you.\n"
            "\"You’ve done more than most soldiers ever will.\"\n"
            "\"I don’t have the special gear finished yet… but when I do, it’s yours.\""
        )
        gain_xp(player, 150)
        player["engineer_reward_10_given"] = True

    elif given >= 5 and not player.get("engineer_reward_5_given", False):
        suspense_print(
            "The engineer tightens a bolt as you approach.\n"
            "\"Yeah… these parts are good. Real good.\"\n"
            "\"I’ve already reinforced the outer turrets thanks to you.\"\n\n"
            "He tosses you a small crate.\n"
            "\"Take this. Keeps you alive out there — which means more tech for me.\""
        )
        add_item(player, "coin", 100)
        add_item(player, "shotgun_shells", 4)
        add_item(player, "magnum_ammo", 1)
        gain_xp(player, 100)
        player["engineer_reward_5_given"] = True

    elif given >= 3 and not player.get("engineer_reward_3_given", False):
        suspense_print(
            "\"Thanks for the parts,\" the engineer says.\n"
            "\"With these and the files our scout brought back I’ve made real progress.\"\n\n"
            "He gestures you closer.\n"
            "\"This neural implant should help you decipher their language.\"\n"
            "\"Try not to fry your brain.\""
        )
        add_item(player, "neural_implant", 1)
        player["understand_alien_language"] = True
        add_item(player, "coin", 50)
        add_item(player, "shotgun_shells", 3)
        gain_xp(player, 50)
        player["engineer_reward_3_given"] = True

    else:
        suspense_print(
            "The engineer barely looks up from his work.\n"
            "\"Alien tech keeps this place standing.\"\n"
            "\"If you find any out there, bring it to me.\""
        )

    # --- Menu loop ---
    while True:
        suspense_print("1) Ask about the machinery")
        suspense_print("2) Give alien tech parts")
        suspense_print("3) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "The engineer taps a humming console.\n"
                "\"Half of this city shouldn’t even work anymore.\"\n"
                "\"Human steel, alien cores… held together by luck and bad decisions.\"\n"
                "\"But as long as it runs, Bastion stands.\""
            )
            return

        elif choice == "2":
            inventory = player.get("inventory", {})
            if inventory.get("alien_tech_part", 0) > 0:
                remove_item(player, "alien_tech_part", 1)
                player["has_given_alien_tech_to_engineer"] = given + 1

                suspense_print(
                    "You hand over the alien tech.\n"
                    "The engineer examines it closely, nodding.\n"
                    "\"Yeah… this’ll keep a few more people alive.\""
                )
                return  # clean re-entry for milestone check

            else:
                suspense_print(
                    "The engineer shakes his head.\n"
                    "\"No alien tech, no miracles.\""
                )

        elif choice == "3":
            return

        else:
            suspense_print("Invalid choice.")


#OLD FACTORY AREA
def old_factory_way(player):
    if not player.get("has_found_secret_path_near_factory", False):
        suspense_print(
            "You head east, toward the old factory.\n"
            "The road is cracked and half-swallowed by ash.\n"
            "Twisted streetlights hum faintly, still drawing power from somewhere.\n"
            "Every sound echoes too long.\n"
            "You feel like something is listening."
        )

    while True:
        suspense_print("1) Continue toward the factory")
        suspense_print("2) Look around")
        suspense_print("3) Go back to Bastion")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            near_old_factory(player)
            return

        elif choice == "2":
            if (
                not player.get("has_found_secret_path_near_factory", False)
                and skill_check(player, "perception", 40, visible=False)
            ):
                suspense_print(
                    "Something feels wrong.\n"
                    "You notice disturbed dust — footprints.\n"
                    "Human.\n"
                    "They vanish behind a collapsed structure."
                )
                near_old_factory_secret(player)
                return

            elif skill_check(player, "luck", 30, visible=False) and not player.get("found_lucky_loot_near_factory", False):
                player["found_lucky_loot_near_factory"] = True
                suspense_print(
                    "you got lucky searching the area.\n"
                    "You pry open a half-buried container.\n"
                    "Whatever hid it didn’t come back for it."
                )
                add_item(player, "coin", 15)
                add_item(player, "healing_salve", 1)

            elif skill_check(player, "scavenging", 50, visible=False) and not player.get("found_scavenged_loot_near_factory", False):
                player["found_scavenged_loot_near_factory"] = True
                suspense_print(
                    "Among the debris, you recover usable parts.\n"
                    "Scavenged. Not abandoned."
                )
                add_item(player, "shotgun_shells", 3)
                randomized_bonus_loot(
                    player,
                    {"alien_power_cell": (1, 2), "revolver_ammo": (2, 4)}
                )

            else:
                suspense_print(
                    "You scan the ruins.\n"
                    "Nothing moves.\n"
                    "That almost makes it worse."
                )

        elif choice == "3":
            bastion_entrance(player)
            return
        else:
            suspense_print("Invalid choice.")
def near_old_factory_secret(player):
    suspense_print(
        "Behind the ruins, the air smells of burned flesh and oil.\n"
        "Two small alien bodies lie twisted on the ground.\n"
        "Nearby, a human corpse slumps against broken concrete.\n"
        "They didn’t survive each other."
    )

    while True:
        suspense_print("1) Inspect the alien bodies")
        suspense_print("2) Inspect the human body")
        suspense_print("3) Go back")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "The aliens are riddled with bullet holes.\n"
                "Precise.\n"
                "Whoever fought them knew where to aim."
            )

        elif choice == "2":
            if not player.get("has_looted_secret_stranger", False):
                suspense_print(
                    "The man bled out slowly.\n"
                    "His weapon lies empty beside him.\n"
                    "Clutched in his hand — spent casings.\n"
                    "He didn’t run."
                )
                add_item(player, "coin", 70)
                add_item(player, "revolver_ammo", 5)
                player["has_looted_secret_stranger"] = True
                player["has_found_secret_path_near_factory"] = True
            else:
                suspense_print(
                    "There’s nothing left.\n"
                    "Only the silence he died in."
                )

        elif choice == "3":
            old_factory_way(player)
            return
        else:
            suspense_print("Invalid choice.")
def near_old_factory(player):
    suspense_print("you see the old factory in the distance, youre not far\n"
                   "you see faint tracks that go behind a large rock\n"
                   "what do you do ?")
    while True:
        suspense_print("1) Move toward the factory")
        suspense_print("2) Go inspect the camp")
        suspense_print("3) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            old_factory_entrance(player)
            return
        elif choice == "2":
            hidden_camp(player)
            return
        elif choice == "3":
            old_factory_way(player)
            return
        else:
            ("invalid choice")
def hidden_camp(player):
    if not player.get("has_rescued_bastion_scout", False):
        suspense_print(
            "You see a scout camp overlooking the old factory.\n"
            "Tracks go down but none come back."
        )

        while True:
            suspense_print("1) Look in the tent")
            suspense_print("2) Inspect the fire")
            suspense_print("3) Go back")
            suspense_print("I) Open inventory")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                if not player.get("looted_scout_tent", False):
                    suspense_print("You find a note and a few shells.")
                    add_item(player, "shotgun_shells", 2)
                    add_item(player, "scout_note", 1)
                    add_item(player,"tactical_helmet",1)
                    suspense_print(
                        "The note reads:\n\n"
                        "The factory was supposed to be abandoned, but I just saw an alien\n"
                        "in serious gear leaving. He came back with bugs in a jar...\n"
                        "A ship landed. They loaded vats inside.\n"
                        "Something big is happening.\n"
                        "I need to g—"
                    )

                    player["looted_scout_tent"] = True
                else:
                    suspense_print("You already searched the tent.")

            elif choice == "2":
                suspense_print(
                    "The fire is long cold. You see alien footprints — but no blood."
                )

            elif choice == "3":
                
                near_old_factory(player)
                return

            else:
                suspense_print("Invalid choice.")
    else:
        suspense_print("The scout camp is abandoned. Nothing left to do here.")

#factory_inside
def old_factory_entrance(player):
    player["scene"] = "old_factory_entrance"
    if not player.get("old_factory_centipede_killed", False):
        suspense_print(
            "The old factory looms ahead.\n"
            "A monolith of rusted steel and cracked concrete,\n"
            "its walls scarred by time and something far worse.\n\n"
            "A massive sealed door blocks the entrance.\n"
            "The ground around it is unnaturally still."
        )

        if (
            skill_check(player, "perception", 40, visible=False)
            and not player.get("old_factory_entrance_skill_check_passed", False)
        ):
            suspense_print(
                "For just a moment…\n"
                "the sand near the entrance shifts.\n"
                "Something large moves beneath the surface."
            )
            player["old_factory_entrance_skill_check_passed"] = True

        while True:
            suspense_print("1) Approach the factory door")
            suspense_print("2) Go back to the camp")
            suspense_print("I) Open inventory")
            if player.get("old_factory_entrance_skill_check_passed", False):
                suspense_print("3) Investigate the disturbed sand")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            # --- Direct approach ---
            if choice == "1":
                suspense_print(
                    "You step closer to the door.\n"
                    "The metal beneath your feet vibrates.\n\n"
                    "A wet hissing sound erupts from below —\n"
                    "and the ground EXPLODES upward."
                )

                giant_centipede = get_enemy("giant_centipede")
                won = fight_enemy(player, giant_centipede)

                if won:
                    suspense_print(
                        "The centipede thrashes violently before collapsing.\n"
                        "Its segmented body twitches long after it should be dead."
                    )
                    gain_xp(player, 100)
                    add_item(player, "centipede_chitin", 2)
                    player["old_factory_centipede_killed"] = True
                    old_factory_inside(player)
                    return

                game_over()
                return

            # --- Retreat ---
            elif choice == "2":
                near_old_factory(player)
                return

            # --- Investigate movement ---
            elif choice == "3" and player.get("old_factory_entrance_skill_check_passed", False):
                suspense_print(
                    "You move slowly, every step deliberate.\n"
                    "The sand trembles faintly beneath your boots."
                )

                giant_centipede = get_enemy("giant_centipede")

                if skill_check(player, "stealth", 40, visible=False):
                    suspense_print(
                        "Beneath the sand, you spot it.\n"
                        "A massive centipede, coiled and dormant.\n"
                        "Its chitin rises and falls with each breath.\n\n"
                        "You strike before it can react."
                    )
                    giant_centipede["health"] -= 10
                else:
                    suspense_print(
                        "The ground collapses beneath you.\n"
                        "The centipede erupts from the sand, mandibles snapping."
                    )

                won = fight_enemy(player, giant_centipede)

                if won:
                    suspense_print(
                        "The creature lets out a shrill, metallic screech\n"
                        "before collapsing into the sand."
                    )
                    gain_xp(player, 100)
                    add_item(player, "centipede_chitin", 2)
                    player["old_factory_centipede_killed"] = True
                    old_factory_inside(player)
                    return

                game_over()
                return

            else:
                suspense_print("Invalid choice.")

    else:
        suspense_print(
            "The entrance lies silent.\n"
            "Dark stains mark where the creature fell.\n"
            "Nothing moves now… at least, not outside."
        )
        old_factory_inside(player)
        return
def old_factory_inside(player):
    suspense_print(
        "You're in the old factory.\n"
        "The air is thick with dust and the scent of rust.\n"
        "Dim light filters through cracked windows, casting eerie shadows.\n"
        "You hear faint scuttling sounds deeper inside.\n"
        "What do you do?")
    suspense_print("1) Explore upstairs")
    suspense_print("2) Explore the main floor")
    suspense_print("3) Go down to the basement")
    suspense_print("4) Go outside")
    while True:
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            factory_first_floor(player)
            return
        elif choice == "2":
            factory_main_floor(player)
            return
        elif choice == "3":
            factory_basement(player)
            return
        elif choice == "4":
            near_old_factory(player)
            return
        else:
            suspense_print("Invalid choice.")
def factory_first_floor(player):
    if not player.get("factory_first_alien_killed", False):
        suspense_print("you arrive up the stairs and hear faint noises coming from behind a door\n"
                    "what do you do ?")
        while True:
            suspense_print("1) open the door")
            suspense_print("2) go back downstairs")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                alien_fight(player)
                return
            elif choice == "2":
                old_factory_inside(player)
                return
            else:
                suspense_print("Invalid choice.")
    else:
        suspense_print("you arrive up the stairs but the area is eerily silent\n")
        while True:
            suspense_print("1) advance to the next room")
            suspense_print("2) check the crates")
            suspense_print("3) go back downstairs")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                factory_first_floor_next_room(player)
                return
            elif choice == "2":
                if not player.get("factory_first_floor_crates_looted", False):
                    suspense_print(
                        "you check the crates and find some useful items\n"
                        "there is also some slimy alien armor, a shame no man can fit it\n"
                    )
                    add_item(player, "weird_fruit", 1)
                    add_item(player, "alien_energy_cell", 3)
                    add_item(player, "advance_medkit", 2)
                    player["factory_first_floor_crates_looted"] = True
                else:
                    suspense_print("The crates are empty. Whatever was useful is gone.")

            elif choice == "3":
                old_factory_inside(player)
                return
            else:
                suspense_print("Invalid choice.")
def factory_first_floor_next_room(player):
    if player.get("has_help_bastion_scout", False) and "scout_files"in player.get("inventory", {}):
        scout_second_talk(player)
    elif not player.get("has_help_bastion_scout", False):
        scout_first_talk(player)
    else:
        suspense_print(
            "The scout sits weakly against the table.\n"
            "\"Please… the files are in the basement lab.\"\n"
            "\"I can’t leave without them.\""
        )
        factory_first_floor(player)
        return

def scout_first_talk(player):
    suspense_print("you enter the next room and see a man staped to a table\n"
                   "he seems weak and injured\n"
                   "he looks at you with pleading eyes,he feats the scout description\n")
    while True:
        suspense_print("1) help him")
        suspense_print("2) ask him who he is")
        suspense_print("3) go back")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("you carefully untap him from the table\n"
                           "he winces in pain but thanks you\n"
                           "\"thank you stranger i thought i was done for\"\n"
                            "\"i was sent here to scout this factory but i got captured by aliens\"\n"
                            "\"they were experimenting on me and others there is a lab in the basement where they keep files\"\n"
                            "\"i cant leave without those files\"\n"
                            "\"if you can get those files it would help bastion a lot\"\n")
            player["has_help_bastion_scout"] = True
            factory_first_floor(player)
            return
        elif choice == "2":
            if skill_check(player, "perception", 40) and not player.get("has_verified_scout_identity", False):
                player["has_verified_scout_identity"] = True
                suspense_print("you look closely at him, nothing about him seems off\n")
                gain_xp(player, 20)
                player["has_verified_scout_identity"]= True
            else:
                suspense_print("he looks too weak to be lying about anything\n")
            suspense_print("please i need your help\n"
                           "free me from these bonds\n")
        elif choice == "3":
            factory_first_floor(player)
            return
        else:
            suspense_print("Invalid choice.")
def scout_second_talk(player): 
    suspense_print("you enter the next room and see the scout binding his wounds\n"
                   "he looks at you with gratitude\n"
                     "\"I can't believe you got those files\"\n" 
                        "\"this will help bastion a lot thank you\"\n")
    while True:
        suspense_print("1) ask about the computer downstairs")
        suspense_print("2) go back")
        if "scout_files" in player.get("inventory", {}):
            suspense_print("3) Give him the files")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "3" and not  "scout_files" in player.get("inventory", {}):
            suspense_print("you dont have the files to give him")
        elif choice == "3" and "scout_files" in player.get("inventory", {}):
            if player.get("has_rescued_bastion_scout", False):
                suspense_print("The scout has already secured the files and thanks you again.")
                continue
            suspense_print("thank you so much stranger\n"
                           "with these files bastion will be able to plan better defenses against the aliens\n"
                            "there is a lot of info about alien tech i think the engineer at bastion will be very interested in this\n")    
            gain_xp(player, 50)
            add_item(player, "coin", 100)
            remove_item(player, "scout_files", 1)
            player["has_rescued_bastion_scout"] = True
            suspense_print(
                "The scout gathers his strength.\n"
                "\"I’ll head back to Bastion as soon as I can walk.\"\n"
                "\"You should return too. They’ll want to hear from you.\""
)       
            old_factory_inside(player)

            return
        elif choice == "1":
            suspense_print("\"the computer downstairs ?\"\n"
                           "\"i saw some aliens using it to log data about their experiments\"\n"
                           "\"but there is no way to use it without deciphering their language\"\n")
            
        elif choice == "2":
            factory_first_floor(player)
            return
        else:
            suspense_print("Invalid choice.")
def alien_fight(player):
    suspense_print("you open the door and see a alien creature rummaging through some crates\n"
                   "it does not seem to have noticed you yet")
    suspense_print("what do you do ?")
    while True:
        suspense_print("1) sneak attack")
        suspense_print("2) shoot it")
        suspense_print("3) analyze it")
        suspense_print("4) go back")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if skill_check(player, "stealth", 40):
                suspense_print("you successfully sneak attack the alien")
                alien = get_enemy("alien_soldier")
                alien["health"] -= 10
                won = fight_enemy(player, alien)
                if won:
                    suspense_print("you have defeated the alien")
                    add_item(player, "weird_fruit", 1)
                    add_item(player, "alien_energy_cell", 2)
                    player["factory_first_alien_killed"] = True
                    return
                else:
                    game_over()
                    return
            else:
                suspense_print("the alien notices you as you try to sneak attack it")
                alien = get_enemy("alien_soldier")
                won = fight_enemy(player, alien)
                alien["health"] += 5
                if won:
                    suspense_print("you have defeated the alien")
                    gain_xp(player, 100)
                    add_item(player, "weird_fruit", 1)
                    add_item(player, "alien_energy_cell", 2)
                    player["factory_first_alien_killed"] = True
                    return
                else:
                    game_over()
                    return
        elif choice == "2":
            damage = shoot_and_remove_ranged_ammo(player)
            if damage <= 0:
                return  # no shot fired

            suspense_print("The alien screeches in pain!")
            alien = get_enemy("alien_soldier")
            alien["health"] -= damage

            won = fight_enemy(player, alien)
            if won:
                suspense_print("you have defeated the alien")
                gain_xp(player, 100)
                add_item(player, "weird_fruit", 1)
                add_item(player, "alien_energy_cell", 2)
                player["factory_first_alien_killed"] = True
                return
            else:
                game_over()
                return
        elif choice == "3":
            if skill_check(player, "intelligence", 40):
                suspense_print("you analyze the alien and find its weak spots\n" \
                "it can't breathe our air well, if we shoot his scafender it will be easier to fight\n"
                               "you feel more confident fighting it")
                gain_xp(player, 20)
            else:
                suspense_print("you try to analyze the alien but fail to find anything useful\n")
        elif choice == "4":
            factory_first_floor(player)
            return
        else:
            suspense_print("Invalid choice.")
def factory_main_floor(player):
    suspense_print("you enter the main hall you hear machinery humming faintly\n"
                   "but before you there is only a long empty corridor leading deeper into the factory\n")
    if skill_check(player, "perception", 40, visible=False):
        suspense_print("you see red laser tripwires across the corridor\n")
        player["has_seen_laser_tripwires"] = True
    suspense_print("what do you do ?")
    while True:
        suspense_print("1) go down the corridor")
        suspense_print("2) look around the hall")   
        suspense_print("3) go back") 
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("has_seen_laser_tripwires", False):
                suspense_print("you carefully avoid the laser tripwires and move down the corridor safely\n")
                factory_machine_room(player)
                return
            else:
                player["factory_main_turret_destroyed"] = True
                suspense_print("as you move down the corridor you suddenly hear a beep\n"
                               "you triggered a laser tripwire\n"
                               "suddenly turrets emerge from the walls and open fire on you\n")
                turret = get_enemy("turret")
                won = fight_enemy(player, turret)
                if won:
                    player["factory_main_turret_destroyed"] = True
                    suspense_print("you have destroyed the turret and can now proceed down the corridor safely,the laser tripwires turn off\n")
                    factory_machine_room(player)
                    return
                else:
                    game_over()
                    return
        elif choice == "2":
            suspense_print("you look around the hall but find nothing of interest\n")
        elif choice == "3":
            old_factory_inside(player)
            return
        else:
            suspense_print("Invalid choice.")
def factory_machine_room(player):
    if not player.get("factory_machine_room_cleared", False):
        suspense_print("you arrive in a large room filled with machinery\n"
                   "barely funtioning generators and conveyor belts creak and hum\n"
                   "you see a man against a wall it look hurt but alive\n")
        while True:
            suspense_print("1) talk to the man")
            suspense_print("2) look around the room")
            suspense_print("3) help the man")
            suspense_print("4) shoot the man")
            suspense_print("5) go back")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print(
                    "please i need your help\n"
                    "they captured me and experimented on me\n"
                    "im a scout for bastion please help me get out of here\n"
                )

                # Player already helped a Bastion scout earlier
                if player.get("has_help_bastion_scout", False):
                    suspense_print(
                        "Something doesn't sit right.\n"
                        "You already helped a Bastion scout upstairs.\n"
                    )

                    # Perception check – physical tells
                    if skill_check(player, "perception", 40):
                        suspense_print(
                            "You notice his breathing is irregular.\n"
                            "His shadow flickers unnaturally against the machinery.\n"
                            "This man is hiding something.\n")
                        if player.get("suspect_metamorph", False):
                            gain_xp(player, 10)
                        player["suspect_metamorph"] = True
                        continue
                    # Intelligence check – logical contradiction
                    elif skill_check(player, "intelligence", 40):
                        suspense_print(
                            "His story doesn't add up.\n"
                            "a scout would have left not gone deeper.\n"
                            "You suspect deception.\n"
                        )
                        if player.get("suspect_metamorph", False):
                                gain_xp(player, 10)
                        player["suspect_metamorph"] = True
                        continue
                    else:
                        suspense_print(
                            "Despite your doubts, you can't find solid proof.\n"
                            "Maybe you're just being paranoid.\n"
                        )
                        continue
                else:
                    suspense_print(
                        "He looks terrified and exhausted.\n"
                        "If he's lying, he's very convincing.\n"
                    )
                    continue
            elif choice == "2":
                
                if skill_check(player, "intelligence", 40) and not player.get("machine_room_looted", False):

                    suspense_print("you look around the room and find a gear that dosent seem to belong here\n"
                                   "upon closer inspection you find a hidden compartment with some useful items\n")
                    gain_xp(player, 20)
                    add_item(player, "alien_energy_cell", 1)
                    add_item(player, "rifled_ammo", 2)
                    add_item(player, "coin", 50)
                    player["machine_room_looted"] = True
                    return

                else:
                    suspense_print("you look around nothings seams out of place\n")
            elif choice == "3":
                
                if player.get("suspect_metamorph", False):
                    suspense_print(
                        "You keep your distance as you approach.\n"
                        "The moment he moves, you are ready.\n"
                        "The disguise melts away — an alien metamorph!\n"
                    )
                    alien_metamorph = get_enemy("alien_metamorph")
                    alien_metamorph["health"] -= 8  # advantage for being cautious
                else:
                    suspense_print(
                        "You come closer to help the man.\n"
                        "Suddenly he launches a spike at you!\n"
                        "The flesh twists and reforms — an alien metamorph!\n"
                    )
                    player["health"] -= 6
                    alien_metamorph = get_enemy("alien_metamorph")

                won = fight_enemy(player, alien_metamorph)

                if won:
                    suspense_print("you have defeated the alien metamorph\n")
                    gain_xp(player, 100)
                    add_item(player, "alien_biomass", 2)
                    add_item(player, "bubbling_goo", 1)
                    randomized_bonus_loot(
                        player,
                        {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["factory_machine_room_cleared"] = True
                    player["suspect_metamorph"] = False
                    return
                else:
                    game_over()
                    return
            elif choice == "4":
                damage = shoot_and_remove_ranged_ammo(player)
                if damage <= 0:
                    return  # no shot fired
                
                suspense_print("you shoot the man,it turns back to you with glowing eyes\n"
                               "change forms and lunches at you\n")
                alien_metamorph = get_enemy("alien_metamorph")
                if player.get("suspect_metamorph", False):
                    alien_metamorph["health"] -= damage + 5
                else:
                    alien_metamorph["health"] -= damage
                won = fight_enemy(player, alien_metamorph)
                if won:
                    suspense_print("you have defeated the alien metamorph\n")
                    gain_xp(player, 100)
                    add_item(player, "alien_biomass", 2)
                    add_item(player, "bubbling_goo", 1)
                    randomized_bonus_loot(
                        player,
                        {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["factory_machine_room_cleared"] = True
                    player["suspect_metamorph"] = False
                    return
                else:
                    game_over()
                    return
            elif choice == "5":
                factory_main_floor(player)
                return
            else:
                suspense_print("Invalid choice.")
    else:
        suspense_print("the room is eerily silent now that the alien threat has been eliminated\n"
                       "there is nothing more to do here\n")
        old_factory_inside(player)  
    
def factory_basement(player):
    suspense_print("you head down to the basement\n"
                   "the air is damp and musty\n"
                   "you hear crawling sounds coming from the shadows\n")
    while True:
        if not player.get("kill_the_centipedes", False):
            suspense_print("1) explore the basement")
            suspense_print("2) go back")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print("as you go down you see glowing eyes in the darkness\n"
                            "the sound of claping mandibles grows louder\n" \
                            "you see moving shadows all around you\n"
                                "suddenly armored giant centipede jump at you from the shadows\n")
                enemies = [get_enemy("armored_giant_centipede") for _ in range(2)]
                won = fight_multiple_enemies(player, enemies)   
                if won:
                    suspense_print("you have defeated the armored giant centipedes\n")
                    gain_xp(player, 150)
                    add_item(player, "centipede_chitin", 4)
                    randomized_bonus_loot(
                        player,
                        {"alien_power_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["kill_the_centipedes"] = True
                    suspense_print("you find a healing station in the corner and heal youself to max health")
                    player["health"] = player["max_health"]
                    alien_lab_basement(player)
                    return
                else:
                    game_over()
                    return
            elif choice == "2":
                old_factory_inside(player)
                return
            else:
                suspense_print("Invalid choice.")
        else:
            suspense_print("the basement is eerily silent now that the centipede threat has been eliminated\n"
                           "there is nothing more to do here\n")
            while True: 
                suspense_print("1) go in the lab")
                suspense_print("2) go back")
                choice = get_choice()
                if handle_global_input(choice, player):
                    continue
                if choice == "1":
                    alien_lab_basement(player)
                    return
                elif choice == "2":
                    old_factory_inside(player)
                    return
                else:
                    suspense_print("Invalid choice.")
def update_kapibara_phase(beast):
    """Mutate the boss based on remaining health."""
    max_hp = beast.get("max_health", beast["health"])
    current_hp = beast["health"]
    hp_pct = current_hp / max_hp

    # Phase 2: Aberrant Frenzy
    if hp_pct <= 0.6 and not beast.get("phase_2", False):
        beast["phase_2"] = True
        beast["damage"] += 2
        beast["special_attack_chance"] = 0.35

        beast["attack_messages"].extend([
            "Its spine splits with a wet crack as it lunges!",
            "Jagged bone tears through its hide as it slams into you!",
            "It moves wrong — joints bending where they shouldn't!"
        ])

        beast.setdefault("miss_messages", []).extend([
            "It crashes into the ground, spraying blood and dirt everywhere."
        ])

        suspense_print(
            "The creature SCREAMS — not in rage, but in agony.\n"
            "Bones push outward beneath its skin, tearing through fur and flesh.\n"
            "It staggers… then steadies itself.\n"
            "Whatever it was, it isn't anymore."
        )

    # Phase 3: Terminal Mutation
    if hp_pct <= 0.25 and not beast.get("phase_3", False):
        beast["phase_3"] = True
        beast["damage"] += 3
        beast["special_attack_chance"] = 0.5
        beast["special_attack_multiplier"] = 3.0

        beast["attack_messages"].extend([
            "Its jaw unhinges with a sickening snap as it charges!",
            "Acidic fluid pours from its mouth as it throws itself at you!",
            "It collapses — then drags itself forward on broken limbs!"
        ])

        beast.setdefault("special_attack_messages", []).extend([
            "Its chest bursts open as it hurls itself at you in a final, screaming charge!"
        ])

        suspense_print(
            "The creature should be dead.\n"
            "Its body is failing — organs exposed, movements erratic.\n"
            "Yet it keeps coming, driven by something that refuses to let it die.\n"
            "This is no longer a fight for survival.\n"
            "It is a corpse lashing out."
        )
#boss fight functions
def mutated_capibara_intro_attack(player, boss):
    suspense_print(
        "\nThe container explodes open!\n"
        "The mutated capibara slams its fists into the ground,\n"
        "releasing a psychic shockwave!\n"
    )

    damage = 6 + boss.get("level", 1) * 2
    player["health"] -= damage

    suspense_print(f"You take {damage} damage before the fight even begins!\n")

    if player["health"] <= 0:
        game_over()
        return False

    boss["intro_used"] = True
    return True
def mutated_capibara_death(boss):
    suspense_print(
        "\nThe mutated capibara lets out a final distorted scream.\n"
        "Its body begins to convulse as the alien mutations destabilize.\n"
        "Glowing veins rupture, releasing a blinding flash of energy!\n"
        "With a thunderous crash, the creature collapses — finally still.\n"
    )
def alien_lab_basement(player):
    def build_mutated_capibara():
        capibara = get_enemy("mutated_capibara")
        capibara["max_health"] = capibara["health"]
        capibara["phase_2"] = False
        capibara["phase_3"] = False
        update_kapibara_phase(capibara)
        return capibara
    if not player.get("old_factory_boss_killed", False):
        suspense_print(
            "You enter a lab filled with alien equipment.\n"
            "Strange lights pulse across glass tanks and metal restraints.\n\n"
            "An alien scientist works frantically at a console.\n"
            "It freezes when it sees you.\n\n"
            "Without a word, it slams a control panel.\n"
            "A reinforced container unlocks with a heavy CLANG.\n\n"
            "Something inside MOVES.\n"
            "A deep, wet growl reverberates through the lab.\n\n"
            "The alien recoils in terror then vanishes through a hidden door."
        )

        Boss = build_mutated_capibara()
        mutated_capibara_intro_attack(player, Boss)
        won = fight_enemy(player, Boss)
        
        if won:
            mutated_capibara_death(Boss)
            suspense_print("you have defeated the mutated capibara\n"
                           "the alien scientist must have fled through the hidden door\n"
                           "you search the lab and find some useful items\n")
            gain_xp(player, 200)
            add_item(player, "alien_tech_part", 1)
            add_item(player, "healing_salve", 2)
            add_item(player, "mutation_serum", 1)
            randomized_bonus_loot(
                player,
                {"alien_power_cell": (1, 2), "rifled_ammo": (2, 4)}
            )
            player["old_factory_boss_killed"] = True
            alien_lab_basement_after_boss(player)
            return
        else:
            game_over()
            return
    else:
        alien_lab_basement_after_boss(player)

def alien_lab_basement_after_boss(player):
    suspense_print("the lab is now silent after the battle\n"
                   "the pustuled remains of the mutated capibara lie on the floor\n"
                   "there is nothing more to do here\n")
    while True:
        suspense_print("1) go back upstairs")
        suspense_print("2) open the door the alien scientist fled through")
        suspense_print("3) look around the lab")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
                old_factory_inside(player)
                return   
        elif choice == "2":
            if not player.get("dealt_with_alien_scientist", False):
                suspense_print("you pry open the hidden door and enter a small room\n")
                factory_alien_scientist_encounter(player)
                return
            else:
                suspense_print("you enter the secret room again")
                secret_factory_room(player)
                return
        elif choice == "3":
            suspense_print("you look around the lab there is many twistedand amorphous creatures in vats\n"
                           "some seem to be alien experiments others look like mutated animals\n"
                           "you find some useful items among the lab equipment\n")
            add_item(player, "pulsing_vial", 1)
            add_item(player, "alien_energy_cell", 1)
        else:
            suspense_print("Invalid choice.")
def factory_alien_scientist_encounter(player):
    suspense_print(
        "The alien scientist hunches over a flickering console.\n"
        "Its elongated fingers tremble as they dance across alien symbols.\n\n"
        "Slowly… it turns toward you.\n"
        "Its eyes are too large. Too wet.\n"
        "For a moment, neither of you moves.\n"
    )

    def resolve_scientist_fight(alien_scientist):
        won = fight_enemy(player, alien_scientist)
        if won:
            suspense_print(
                "The alien collapses in a heap of twitching limbs.\n"
                "Its weapon clatters to the floor, still humming softly.\n\n"
                "You search the room, ignoring the smell of burned flesh.\n"
            )
            gain_xp(player, 150)
            add_item(player, "scout_note", 1)
            add_item(player, "healing_salve", 1)
            randomized_bonus_loot(
                player,
                {"alien_power_cell": (1, 2), "rifled_ammo": (2, 4)}
            )
            player["dealt_with_alien_scientist"] = True
            secret_factory_room(player)
        else:
            game_over()

    while True:
        suspense_print("1) ask why it is experimenting on creatures")
        suspense_print("2) demand it surrender")
        suspense_print("3) shoot it")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        alien_scientist = get_enemy("alien_scientist")

        if choice == "1":
            suspense_print(
                "The alien tilts its head at an impossible angle.\n"
                "It chatters rapidly in a wet, clicking language.\n\n"
                "You feel like it's explaining something.\n"
                "Something terrible.\n\n"
                "Suddenly, its hand snaps toward a weapon.\n"
            )
            resolve_scientist_fight(alien_scientist)
            return

        elif choice == "2":
            suspense_print(
                "The alien recoils, pressing itself against the console.\n"
                "A thin, shrill sound escapes its throat.\n\n"
                "Then fear turns to desperation.\n"
                "It raises its weapon and fires.\n"
            )
            resolve_scientist_fight(alien_scientist)
            return

        elif choice == "3":
            shot = shoot_and_remove_ranged_ammo(player)
            if shot:
                suspense_print(
                    "You fire.\n"
                    "The shot tears into the alien’s torso.\n"
                    "It shrieks — a sound halfway between pain and rage.\n"
                )
                alien_scientist["health"] -= 8
            else:
                suspense_print(
                    "You fumble for a weapon — but nothing fires.\n"
                    "The alien notices.\n"
                )

            suspense_print(
                "Before you can react, it retaliates with its energy weapon.\n"
            )
            resolve_scientist_fight(alien_scientist)
            return

        else:
            suspense_print("Invalid choice.")
def secret_factory_room(player):
    suspense_print(
        "You slip into the hidden chamber the alien fled into.\n"
        "The air here is warmer. Damp.\n"
        "Strange organic machinery lines the walls, softly pulsing.\n\n"
        "Research notes are scattered across metal tables.\n"
        "Some are stained with something dark.\n\n"
        "At the far end of the room, a data console hums quietly.\n"
    )

    while True:
        suspense_print("1) look around the room")
        suspense_print("2) examine the console")
        
        suspense_print("3) go back upstairs")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("secret_room_looted", False):
                suspense_print(
                    "You force yourself to search the room.\n"
                    "Every surface feels… wrong.\n\n"
                    "Among the alien instruments, you recover a few intact items.\n"
                )
                add_item(player, "alien_tech_part", 1)
                add_item(player, "strange_elixir", 1)
                add_item(player,"scout_files",1)
                player["secret_room_looted"] = True
            else:
                suspense_print(
                    "You search the room again.\n"
                    "There is nothing left — only the quiet hum of alien machines.\n"
                )

        elif choice == "2":
            suspense_print(
                "You approach the console.\n"
                "Its surface ripples slightly under your touch.\n"
            )

            if player.get("understand_alien_language", False):
                suspense_print(
                    "The symbols begin to make sense.\n\n"
                    "Experiment logs scroll across the screen:\n\n"
                    "• Gene splicing between local fauna and alien biomass\n"
                    "• Aggression amplification protocols\n"
                    "• Failure rates marked in red\n\n"
                    "One entry repeats again and again:\n"
                    "\"HOST FORM UNSTABLE\"\n\n"
                    "Near the end, a final section appears:\n"
                    "\"COLONIZATION TRIAL — PLANET VIABLE\"\n\n"
                    "They weren’t just experimenting.\n"
                    "They were preparing replacements.\n"
                )
                player["learned_alien_plan"] = True
            else:
                suspense_print(
                    "The symbols crawl and shift as you stare at them.\n"
                    "You recognize patterns… but no meaning.\n\n"
                    "Whatever this console contains, it was never meant for humans.\n"
                )
        
        elif choice == "3":
            suspense_print(
                "You turn away from the alien machinery.\n"
                "The feeling of being watched lingers as you leave the room.\n"
            )
            alien_lab_basement_after_boss(player)
            return

        else:
            suspense_print("Invalid choice.")


#ALIEN LAND AREA
def alien_land_1(player): # to finish
        suspense_print(
            "You arrived in a strange land full of alien flora and fauna\n"
            "the air is thick with spores and the sky is a sickly green color\n"
            "in a way its beautiful but also terrifying\n"
            "you see a path leading deeper into the alien land\n"
            )
        while True: 
            if player.get("can_breathe_in_alien_environments", False):
                suspense_print("as you try to breathe the air full of spores you choke and cough violently")
                player["health"] -= 10
                if player["health"] <= 0:
                    suspense_print("you have died from suffocation")
                    exit(0)
            suspense_print("1) go forward into alien land")
            suspense_print("2) go back to bastion")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print(
                    "you move forward into the alien land\n"
                    "the flora and fauna are unlike anything you have ever seen before\n"
                    "you see strange twisting plants with collorful leaves and flowers\n"
                    "you also see strange alien creatures moving in the distance\n"
                    "you feel a strange energy pulsing through the place"
                )
                from save_system import save_game
                save_game(player)
                print("game saved")
                if DEMO_MODE:
                    end_demo(player)
                else:
                    alien_land_2(player)

                #alien_land_2(player) futur
                return
            elif choice == "2":
                bastion_entrance(player)
                return
def end_demo(player):
    suspense_print(
        "as you explore the alien land you feel a strange sense of wonder and curiosity\n"
        "but also a sense of danger and unease\n"
        "you realize that this is just the beginning of your adventure\n"
        "and that there is much more to discover and explore in this strange new world\n"
        "thank you for playing my demo !! I hope to see you in the reste of this adventure !!"
    )
    return