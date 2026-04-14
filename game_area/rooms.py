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
from game_area.hospital import hospital

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
            wasteland_stranger_encounter(player)
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
# Farm House Rooms & #survivor_base
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
            survivor_montain_base(player)
            return

        else:
            suspense_print("Invalid choice.")
from game_area.survivor_base import survivor_montain_base
from game_area.Farme_house import farm_house_inside


#old survivor base and underground complex
from game_area.Old_survivor_baseand_underground_complex import 

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
            hospital(player)
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
        "\"You've already proven yourself.\n"
        "I'd like to offer you a position as a scout.\"\n\n"
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
                "\"Your first mission: the old military base, deep in alien land.\"\n"
                "\"It was a special outpost before the war.\"\n"
                "\"We need data on hidden weapons and research facilities.\"\n\n"
                "\"Bring back what you can.\"\n"
                "\"Clear the base and I'll send scavengers after you.\""
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
    base_objective_completed = player.get("outpost_data_count", 0) >= 3
    full_quest_completed = (
        player.get("enemy_in_outpost_killed_count", 0) >= 10
        and base_objective_completed
    )

    if not base_objective_completed:
        suspense_print(
            "\"The outpost is still out there,\" the sergeant says.\n"
            "\"Bring back anything you find.\""
        )
        return

    if full_quest_completed and not player.get("received_scout_exoskeleton", False):
        suspense_print(
            "\"Outstanding work,\" the sergeant says.\n"
            "\"You cleared the outpost and secured the data.\"\n"
            "\"This will help us understand the alien threat and find new resources.\"\n"
            "\"Reward: a scouting exoskeleton. Not the best, but it will keep you alive.\""
        )
        add_item(player, "coin", 150)
        gain_xp(player, 150)
        add_item(player, "exoskeleton_mk_1'runner'", 1)
        player["scout_outpost_completed"] = True
        player["bastion_active_quest"] = "next_mission"
        player["bastion_rank"] += 1
        player["bastion_security_level"] = player.get("bastion_security_level", 0) + 1
        player["received_scout_exoskeleton"] = True
        sergeant_next(player)
        return
    elif full_quest_completed and player.get("received_scout_exoskeleton", False):
        suspense_print(
            "\"You've already earned that reward,\" the sergeant says.\n"
            "\"Stay sharp. We'll have more work soon.\""
        )
        return
    elif base_objective_completed and not full_quest_completed and not player.get("bastion_base_mission_completed", False):
        suspense_print(
            "\"Good work finding the data,\" the sergeant says.\n"
            "\"But the outpost is still crawling with aliens.\"\n"
            "\"Here's a reward for the intel. You did good.\""
        )
        add_item(player, "coin", 50)
        gain_xp(player, 50)
        player["scout_outpost_completed"] = True
        player["bastion_active_quest"] = "next_mission"
        player["bastion_rank"] += 1
        player["bastion_security_level"] = player.get("bastion_security_level", 0) + 1
        player["bastion_base_mission_completed"] = True
        return

def sergeant_next(player):  #to finish
    suspense_print(
        "\"We've found it,\" the sergeant says. his voice is flat. no triumph in it.\n"
        "\"An alien research facility. north of the twisted forest.\"\n"
        "\"Heavily guarded. our scouts didn't come back. we think that's where the cybernetic experiments came from.\"\n"
        "\"someone has to go in. bring back whatever data you can find.\""
    )
    while True:
        suspense_print("1) Accept the mission")
        suspense_print("2) Decline for now")
        suspense_print("3) Ask for more details")
        suspense_print("I) Open inventory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "the sergeant nods slowly. he doesn't look relieved.\n"
                "\"the facility is north of the twisted forest. you'll know it when you see it.\"\n"
                "\"don't linger. whatever they're doing in there... they don't stop for intruders.\"\n"
                "\"bring back anything you find. and try not to end up as one of their experiments.\""
            )
            player["bastion_active_quest"] = "research_facility"
            return
        elif choice == "2":
            suspense_print(
                "\"the world won't wait,\" the sergeant says quietly.\n"
                "\"neither will they.\""
            )
            return
        elif choice == "3":
            suspense_print(
                "\"it used to be a prison,\" the sergeant says.\n"
                "\"before the war. top-secret. buried under an old jail so no one would look twice.\"\n"
                "\"they were building super-soldiers. splicing, cutting, rewiring.\"\n"
                "\"the aliens moved in and kept the work going. maybe they improved on it.\"\n"
                "\"we don't know what's walking around in there now. that's what scares me.\""
            )
        else:
            suspense_print("Invalid choice.")

def sergeant_idle(player):
    suspense_print(
        "\"Keep your eyes open out there,\" the sergeant says.\n"
        "\"The aliens are always watching.\""
    )
def engineer_dialogue(player):
    inventory = player.get("inventory", {})
    if (
        "alien_targeting_implant" in inventory
        and "neural_implant" in inventory
        and not player.get("has_upgraded_implant", False)
    ):
        implant_talk(player)
        return

    given = player.get("has_given_alien_tech_to_engineer", 0)

    # --- Milestone dialogue ---
    if given >= 10 and not player.get("engineer_reward_10_given", False):
        suspense_print(
            "The engineer looks up from a half-disassembled turret.\n"
            "His eyes widen at the pile of alien tech in your hands.\n\n"
            "\"By the rusted gears of Bastion...\"\n"
            "\"With parts like these, I've reinforced the walls, upgraded the guns,\n"
            "and patched weak points we didn't even know we had.\"\n\n"
            "He wipes grease from his hands and nods at you.\n"
            "\"You've done more than most soldiers ever will.\"\n"
            "\"Here, take the best implant I can make.\""
        )
        gain_xp(player, 150)
        if player.inventory.get("upgraded_neural_implant", 0) > 0:
            remove_item(player, "upgraded_neural_implant", 1)
        if player.inventory.get("neural_implant", 0) > 0:
            remove_item(player, "neural_implant", 1)
        add_item(player, "alien_tech_implant", 1)
        player["engineer_reward_10_given"] = True
        player["bastion_security_level"] = player.get("bastion_security_level", 0) + 1

    elif given >= 5 and not player.get("engineer_reward_5_given", False):
        suspense_print(
            "The engineer tightens a bolt as you approach.\n"
            "\"Yeah... these parts are good. Real good.\"\n"
            "\"Outer turrets are holding because of you.\"\n\n"
            "He tosses you a small crate.\n"
            "\"Take this. Keeps you alive out there, which means more tech for me.\""
        )
        add_item(player, "coin", 100)
        add_item(player, "shotgun_shells", 4)
        add_item(player, "magnum_ammo", 1)
        gain_xp(player, 100)
        player["engineer_reward_5_given"] = True
        player["bastion_security_level"] = player.get("bastion_security_level", 0) + 1

    elif given >= 3 and not player.get("engineer_reward_3_given", False):
        suspense_print(
            "\"Thanks for the parts,\" the engineer says.\n"
            "\"With these and the files our scout brought back, I've made real progress.\"\n\n"
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
        player["bastion_security_level"] = player.get("bastion_security_level", 0) + 1

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
                "\"Half of this city shouldn't even work anymore.\"\n"
                "\"Human steel, alien cores... held together by luck and bad decisions.\"\n"
                "\"But as long as it runs, Bastion stands.\""
            )
            return

        elif choice == "2":
            if inventory.get("alien_tech_part", 0) > 0:
                remove_item(player, "alien_tech_part", 1)
                player["has_given_alien_tech_to_engineer"] = given + 1

                suspense_print(
                    "You hand over the alien tech.\n"
                    "The engineer examines it closely, nodding.\n"
                    "\"Yeah... this will keep a few more people alive.\""
                )
                return  # clean re-entry for milestone check

            suspense_print(
                "The engineer shakes his head.\n"
                "\"No alien tech, no miracles.\""
            )

        elif choice == "3":
            return

        else:
            suspense_print("Invalid choice.")
def implant_talk(player):
    suspense_print(
            "you show the engineer the alien targeting implant you found\n"
            "he examines it closely, nodding with approval\n"
            "\"This is top-tier alien tech,\" he says.\n"
            "i could upgrade your implant with this, but i need more parts to make it work\n"
            "bring me 4 implant the one those cybornetic monsters have and i can make it work for you\""
        )
    while True:
        suspense_print("1) Agree to find the parts")
        suspense_print("2) Refuse and go back")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            inventory = player.get("inventory", {})

            if inventory.get("alien_implant", 0) >= 4:
                remove_item(player, "alien_implant", 4)

                suspense_print(
                    "The engineer takes the implants and begins working.\n"
                    "Metal scrapes against metal.\n"
                    "Something inside it moves.\n\n"
                    "After a long silence, he hands it back.\n"
                    "\"It will make you stronger,\" he mutters.\n"
                )

                add_item(player, "upgraded_neural_implant", 1)
                remove_item(player, "neural_implant", 1)
                gain_xp(player, 100)
                player["has_upgraded_implant"] = True
                return
            else:
                player["needs_implant_parts"] = True
                return


        elif choice == "2":
            suspense_print("The engineer nods and goes back to his work")
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
        # Continue with Bastion storyline or activities
def alien_land_2(player):
    if player.get("alien_land_2_count", 0) == 0:
        suspense_print(
            "as you move deeper into the alien land you feel a strange presence watching you\n"
            "you see strange alien structures in the distance that seem to be made of organic material\n"
            "you also see strange a spore wall at the horizon\n"
        )  
    else:
        suspense_print(
            "you are back in the alien land\n"
            "the strange alien structures are still in the distance\n"
            "the spore wall at the horizon seems to be getting closer\n"
        )  
    while True: 
        suspense_print("1) go towards the alien structures")
        suspense_print("2) investigate the spore wall")
        suspense_print("3) go back to bastion")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            way_toward_organic_structures(player)
            return
        elif choice == "2":
            spore_wall_investigation(player)
            return
        elif choice == "3":
            bastion_entrance(player)
            return
def way_toward_organic_structures(player): 
    suspense_print(
        "you walk for a while true the alien land everithing around you is strange and colorful\n"
        "the plants and creatures seem to be thriving so much compare to the other side of bastion\n"
        "you feel a strange energy pulsing through the place\n"
    )
    while True:
        suspense_print("1) take some time to enjoy the alien land")
        suspense_print("2) move towards the alien structures")
        suspense_print("3) go toward bastion")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "you take some time to enjoy the alien land\n"
                "you feel a strange sense of wonder and curiosity\n"
                "but also a sense of danger and unease\n"
                "you realize that this is not the world you knew and that there is much more to discover and explore in this strange new world\n"
            )
        elif choice == "2":
            way_toward_organic_structures_2(player)
            return
        elif choice == "3":
            bastion_entrance(player)
            return
        else:
            suspense_print("Invalid choice.")
def way_toward_organic_structures_2(player):
    if player.get("midday_tower_seized_heart", False):
        suspense_print(
            "OUR BROTHERS AWAITS FOR YOU, says a voice in your mind\n" \
            "LEAVE AND FIND THEM ..."
        )
        way_toward_organic_structures(player)
        return
    if player.get("eldritch_eyes", False):
        suspense_print(
            "as you approach the monolithic alien structures, whispers bloom in your mind\n"
            "as you get closer, the whispers deepen, pulling you forward like a tide\n"
            "long organic tendrils unfurl from the towers, pulsing with slow, чуж, living light\n"
            "they reach for you, not quite touching, as if tasting the air around your skin\n"
            "'COME TO US,' says a voice that speaks through your skull\n"
            "you step forward and the tendrils close, swallowing you whole.\n"
        )
        midday_tower(player)
    else:
        suspense_print(
            "you approach a massive organic monolith\n"
            "its surface is veined with pulsing tissue and alien symbols that seem to shift\n"
            "as you draw closer, a stinging pressure emanates from the tower, forcing you back\n"
        )
#horde encounter 
def spore_wall_investigation(player):
    if player.get("spore_wall_zombie_killed", False) and player.get("has_survived_horde_in_alien_land", False):
        suspense_print("you are back at the spore wall\n"
                       "the fungal zombie you defeated earlier lies motionless on the ground\n"
                       "there is nothing more to do here\n")
        #add placement to go back
        return
    suspense_print(
        "you move towards the spore wall\n"
        "as you get closer you see that the wall is made of thick fungal growths\n"
        "the mushrooms are expanding rapidly and releasing spores into the air\n")
    while True:
        suspense_print("1) try to cross the spore wall")
        suspense_print("2) go back")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "as you try to cross the spore wall you hear a loud coughing fit\n"
                "you look around and see a man loudly coughing and struggling to breathe\n"
                "his body full of fungal growths and his eyes red wit blood \n"
                "you lock eyes with him, it stops coughing and starts moving towards you menacingly\n"
                "you realize he has been infected by the spores and turned into a fungal zombie\n"
            )
            sporebound_slave = get_enemy("sporebound_slave")
            won = fight_enemy(player, sporebound_slave)
            if won:
                suspense_print("you have defeated the fungal zombie\n")
                gain_xp(player, 100)
                add_item(player, "med_kit", 1)
                add_item(player, "alien_energy_cell", 1)
                player["spore_wall_zombie_killed"] = True
                randomized_bonus_loot(
                    player,
                    {"healing_salve": (1, 2), "rifled_ammo": (2, 4)}
                )
                suspense_print("the zombie dead you crawl through the spore wall safely\n")
                horde_encounter(player)
                return
                
        elif choice == "2":
            alien_land_2(player)
            return
        else:
            suspense_print("Invalid choice.")
def horde_encounter(player):
    if player.get("has_survived_horde_in_alien_land", False):
        suspense_print("you are back at the fungal horde encounter site\n"
                       "they are gone now\n"
                       "you can go to the military base\n")
        forest_toward_military_base(player)
        return
    suspense_print(
        "you finally cross the spore wall\n"
        "you see a military complex in the distance\n"
        "but as you move forward you hear loud growls and snarls\n"
        "you see a horde of fungal zombies emerging from the horizon\n"
        "they have noticed you and are moving towards you aggressively\n"
    )
    slow_print_char("Run !!!")
    while True:
        suspense_print("1) run towards the cave on the left")
        suspense_print("run towards the canion on the right")
        if not player.get("wasteland_stranger_near_farm_alive", True):
            suspense_print("you see a stranger near the canion waving at you to come towards him... you reconized that cowboy hat")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("you run towards the cave on the left\n"
                           "the fungal zombies are closing in on you\n"
                           "the cave is a dead end you have nowhere to go\n"
                           "the fungal zombies catch up to you and overwhelm you\n")
            game_over()
            return
        elif choice == "2":
            if not player.get("wasteland_stranger_near_farm_alive", True):
                suspense_print("you run towards the canyon on the right\n"
                               "the fungal zombies are closing in on you\n"
                               "the stranger tell you to follow him toward a safe path\n")
            else:
                suspense_print("you run towards the canyon on the right\n"
                               "the fungal zombies are closing in on you\n" \
                               "you manage to go down a narrow path down\n")     
            horde_part_2(player)
            return
        else:
            suspense_print("Invalid choice.")
def horde_part_2(player):
    suspense_print(
        "you arrived down to a river at the bottom of the canyon\n"
        "you see the hord at the top of the canyon\n"
        "they seem to have stop... then they start crashing down slowly forming a flesh cushion\n"
        "you realize they are trying to reach you by sacrificing themselves"
        "you run along the river bank trying to find a way out\n"
    )
    if not player.get("wasteland_stranger_near_farm_alive", True):
        suspense_print("the stranger from before tell you to go toward a boat down the river\n")
    while True:
            suspense_print("1)keep running along the river bank")
            suspense_print("2) go toward the boat")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print("you keep running along the river bank\n"
                               "the fungal zombies are still crashing down from above\n"
                               "suddenly one of them grab you from behind\n"
                               "you struggle to break free but there are too many of them\n")
                game_over()
                return
            elif choice == "2":
                suspense_print("you run toward the boat and manage to get in\n"
                               "the current is strong and you gain distance from the horde\n")
                horde_part_3(player)
                return
            else:
                suspense_print("Invalid choice.")
def horde_part_3(player):
    suspense_print(
        "you are now on the boat drifting down the river\n"
        "the fungal zombies are far but still coming down the canyon\n"
        "you arrived near a massive waterfall\n")
    if not player.get("wasteland_stranger_near_farm_alive", True):
        suspense_print("the stranger from before shouts at you to stay on the boat\n")
    while True:
            suspense_print("1) brace yourself and stay on the boat")
            suspense_print("2) jump off the boat before the waterfall")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                if player.get("wasteland_stranger_near_farm_alive", True):
                    suspense_print("the stranger from before shouts at you to hold on tight\n"
                                   "you brace yourself as the boat goes over the waterfall\n"
                               "the fall is long and you hit the water hard\n"
                               "you manage to swim to shore and escape the fungal horde\n")
                    player["has_survived_horde_in_alien_land"] = True
                    stranger_hideout(player)
                    return
                else:
                    suspense_print("you brace yourself as the boat goes over the waterfall\n"
                               "the fall is long and you hit the water hard\n"
                               "you manage to swim to shore and escape the fungal horde\n")
                player["has_survived_horde_in_alien_land"] = True
                twisted_forest(player)
                return
            elif choice == "2":
                suspense_print("you jump off the boat before the waterfall\n"
                               "thepath stops here and the horde catches up to you\n"
                                 "you are overwhelmed by the fungal zombies\n")
                game_over()
                return
            else:
                suspense_print("Invalid choice.")
#Twisted forest and stranger hideout
def stranger_hideout(player):
    suspense_print(
        "you follow the stranger for a while arriving in a strange forest to a hidden hideout\n"
        "the stranger thanks you for saving him from the fungal horde\n"
        "he insistes to offer you one of is weapons as a token of gratitude\n"
    )
    while True:
            suspense_print("1) take the weapon")
            suspense_print("2) politely decline")
            suspense_print("3) kill the stranger and take all his stuff")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                weapon_selection(player)
                return
            elif choice == "2":
                suspense_print("you politely decline the stranger's offer\n"
                               "he understands and wishes you good luck on your journey\n"
                               "saying if you change your mind you know where to find him\n")
                twisted_forest(player)
                return
            elif choice == "3":
                suspense_print("mad by greed you attack the stranger\n")
                stranger = get_enemy("wasteland_cowboy")
                won = fight_enemy(player, stranger)
                if won:
                    suspense_print("you have defeated the stranger\n"
                                   "you loot all his stuff\n")
                    add_item(player, "cowboy_revolver", 1)
                    add_item(player, "cowboy_hat", 1)
                    add_item(player, "cowboy_rifle", 1)
                    randomized_bonus_loot(
                        player,
                        {"healing_salve": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["wasteland_stranger_near_farm_alive"] = False
                    twisted_forest(player)
                    return
                else:
                    game_over()
                    return
            else:
                suspense_print("Invalid choice.")
def weapon_selection(player):
    suspense_print(
        "the stranger shows you his weapons\n"
        "he has a cowboy revolver and a cowboy rifle\n"
        "both look well maintained and reliable\n"
        "which one do you choose?\n"
    )
    while True:
            suspense_print("1) take the cowboy revolver")
            suspense_print("2) take the cowboy rifle")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print("you take the cowboy revolver\n"
                               "the stranger nods approvingly\n"
                               "he wishes you good luck on your journey\n")
                add_item(player, "cowboy_revolver", 1)
                twisted_forest(player)
                return
            elif choice == "2":
                suspense_print("you take the cowboy rifle\n"
                               "the stranger nods approvingly\n"
                               "he wishes you good luck on your journey\n")
                add_item(player, "cowboy_rifle", 1)
                twisted_forest(player)
                return
            else:
                suspense_print("Invalid choice.")
def twisted_forest(player):
    if player.get("twisted_forest_searched_soldier", False):
        while True:
            suspense_print("1) Follow the path deeper into the twisted forest")
            suspense_print("2) Go north")
            suspense_print("3) go back to bastion")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print("you go deeper into the twisted forest\n"
                               "the alien flora and fauna become more bizarre and dangerous\n"
                               "you see a path leading to a military base in the distance\n")
                twisted_forest_2(player)
                return
            elif choice == "2":
                suspense_print("you go north in the twisted forest\n"
                               "the alien flora and fauna become more bizarre and dangerous\n"
                               "you see a path leading out of the forest\n")
                twisted_forest_north(player)
                return
            elif choice == "3":
                bastion_entrance(player)
                return
            else:
                suspense_print("Invalid choice.")
        
    suspense_print(
        "you enter a twisted forest full of strange alien plants and creatures\n"
        "the trees are tall and twisted with crimson leaves\n"   
        "you see a dead soldier on the ground\n"
        "you reconise bastion military gear on him\n"
    )
    while True:
            suspense_print("1) search the dead soldier")
            suspense_print("2) follow the path deeper into the twisted forest")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                suspense_print("you search the dead soldier\n"
                               "you find a map of a secret path leading to bastion\n"
                               "you find some useful items on him\n")
                add_item(player, "med_kit", 1)
                add_item(player, "rifled_ammo", 5)
                add_item(player, "bastion_map", 1)
                player["twisted_forest_searched_soldier"] = True
            elif choice == "2":
                suspense_print("you go deeper into the twisted forest\n"
                               "the alien flora and fauna become more bizarre and dangerous\n"
                               "you see a path leading to a military base in the distance\n")
                twisted_forest_2(player)
                return
            else:
                suspense_print("Invalid choice.")
def twisted_forest_2(player):
    suspense_print(
        "you are now deeper in the twisted forest\n"
        "the alien flora and fauna are more bizarre and dangerous\n"
        "you see a path leading to a military base in the distance\n"
    )
    while True:
            suspense_print("1) go toward the military base")
            suspense_print("2) look around the forest")
            if "bastion_map" in player["inventory"]:
                suspense_print("3) go back to bastion")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                forest_toward_military_base(player)
                return
            elif choice == "2":
                suspense_print("you see one of those strange fruit growing on a large flowering plant\n")
                suspense_print("do you want to get it ?")
                player_pick_fruit(player)
            elif choice == "3" and "bastion_map" in player["inventory"]:
                bastion_entrance(player)
                return
            else:
                suspense_print("Invalid choice.")
def player_pick_fruit(player):
    if player.get("has_taken_weird_fruit", False):
        suspense_print("you have already taken the strange fruit from this plant\n"
                       "there is nothing more to do here\n")
        twisted_forest_2(player)
        return
    while True:
            if skill_check(player, "perception", 50, visible=False):
                suspense_print("you see  a vein full of torns and spikes around the plant\n"
                               "you realize the plant is may be dangerous\n")
                player["plant_skill_check_passed"] = True
            suspense_print("1) pick the fruit")
            suspense_print("2) leave it be")
            if player.get("plant_skill_check_passed", False):
                suspense_print("3) shoot the plant")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                if player.get("plant_skill_check_passed", False):
                    suspense_print("you pick the fruit carefully avoiding the plant surprise attack\n"
                    )
                    player["has_taken_weird_fruit"] = True
                    add_item(player, "weird_fruit", 1)
                else:
                    suspense_print("as you pick the fruit the plant springs to life\n"
                                   "it attacks you with its sharp vines\n")
                    carnivorous_trap_plant = get_enemy("carnivorous_trap_plant")
                    won = fight_enemy(player, carnivorous_trap_plant)
                    player["health"] -= 3
                    if won:
                        suspense_print("you have defeated the carnivorous trap plant\n"
                                       "you manage to get the fruit safely\n")
                        add_item(player, "weird_fruit", 1)
                        randomized_bonus_loot(
                            player,
                            {"healing_salve": (1, 2), "rifled_ammo": (2, 4)}
                        )
                        player["has_taken_weird_fruit"] = True
                        return
                    else:
                        game_over()
                        return
            elif choice == "2":
                suspense_print("you decide to leave the fruit be\n")
                return
            elif choice == "3" and player.get("plant_skill_check_passed", False):
                shot = shoot_and_remove_ranged_ammo(player)
                if shot:
                    suspense_print("you shoot the plant\n"
                                   "the plant writhes in pain before collapsing\n")
                    add_item(player, "weird_fruit", 1)
                    randomized_bonus_loot(
                        player,
                        {"healing_salve": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["has_taken_weird_fruit"] = True
                    return
                else:
                    suspense_print("you fumble for a weapon — but nothing fires.\n"
                                   "the plant attacks you with its sharp vines\n")
                    carnivorous_trap_plant = get_enemy("carnivorous_trap_plant")
                    won = fight_enemy(player, carnivorous_trap_plant)
                    if won:
                        suspense_print("you have defeated the carnivorous trap plant\n"
                                       "you manage to get the fruit safely\n")
                        add_item(player, "weird_fruit", 1)
                        randomized_bonus_loot(
                            player,
                            {"healing_salve": (1, 2), "rifled_ammo": (2, 4)}
                        )
                        return
                    else:
                        game_over()
                        return
            else:
                suspense_print("Invalid choice.")
def forest_toward_military_base(player):
    suspense_print(
        "you move toward the military base\n"
        "the alien flora and fauna become more sparse and the environment more familiar\n"
        "you see a path leading down to the military base entrance\n"
    )
    while True:
            suspense_print("1) go down to the military base entrance")
            suspense_print("2) scout around the area")
            suspense_print("3) go back to bastion")
            choice = get_choice()
            if handle_global_input(choice, player):
                continue
            if choice == "1":
                military_base_entrance(player)
                return
            elif choice == "2":
                if skill_check(player, "perception", 40, visible=False) or skill_check(player, "luck", 40, visible=False):
                    suspense_print("you scout around the area and find fresh alien boots prints\n"
                                   "they seam to be leading toward the military base entrance\n"
                                   " you also find a crate hidden behind some bushes\n")
                    add_item(player, "alien_energy_cell", 3)
                    add_item(player, "strange_elixir", 1)
                else:
                    suspense_print("you scout around the area but find nothing of interest\n")
            elif choice == "3":
                bastion_entrance(player)
                return
            else:
                suspense_print("Invalid choice.")
def twisted_forest_north(player):
    if player.get("sporebound_slave_killed_in_forest", False):
        suspense_print("you are back in the twisted forest.\n"
                       "the corpse of the creature is already consumed by fungal growth.\n"
                       "something else has been eating it.\n"
                       "keep moving north. don't stop.")
        outside_forest(player)
        return
    suspense_print("the forest gets denser the further north you push.\n"
                   "twisted trunks close in on both sides. the light turns sickly.\n"
                   "something rustles in the bushes to your left.\n"
                   "you stop. listen. nothing.\n"
                   "but the silence feels wrong — too deliberate, too still.\n")
    while True:
        suspense_print("1) keep moving north")
        suspense_print("2) investigate the bushes")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("you don't look back.\n"
                           "the trees thin. the alien growths recede.\n"
                           "ahead, a grey open plain stretches out behind a wall of razor wire.\n"
                           "you made it through. whatever was watching you... let you go.\n")
            outside_forest(player)
            return
        elif choice == "2":
            suspense_print("you push through the undergrowth. nothing there.\n"
                           "just crushed earth and a smell like wet rot.\n"
                           "as you turn back, something drops onto you from above.\n")
            sporebound_slave = get_enemy("sporebound_slave")
            won = fight_enemy(player, sporebound_slave)
            if won:
                suspense_print("it goes still beneath you.\n"
                               "spores drift off its body like smoke.\n"
                               "you search it quickly. hands shaking.\n"
                               "then you run. north. out of the trees.\n")
                randomized_bonus_loot(
                    player,
                    {"healing_salve": (1, 2), "rifled_ammo": (2, 4)}
                )
                player["sporebound_slave_killed_in_forest"] = True
                outside_forest(player)
                return
            else:
                game_over()
                return
        else:
            suspense_print("Invalid choice.")
#MILITARY BASE AREA

from game_area.Military_Base import military_base_entrance
#Prison Ark   
def outside_forest(player):
    suspense_print(
        "the treeline ends and the world opens up into an endless grey plain.\n"
        "a massive perimeter fence cuts across it — razor wire coiled thick at the top, electrified panels humming low.\n"
        "the sound it makes gets under your skin.\n"
        "an old faded sign hangs crooked on the fence: 'WARNING: prison perimeter. Authorized personnel only beyond this point'\n"
        "whoever put it there is long dead.\n"
        "whatever is inside the fence might not be.\n"
    )
    while True:
        suspense_print("1) search for a way into the prison")
        suspense_print("2) scan the area")
        suspense_print("3) retreat into the woods")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            way_to_the_prison(player)
            return
        elif choice == "2":
            if skill_check(player, "scavenging", 50, visible=False):
                suspense_print(
                    "your eyes catch a patch of disturbed earth near the base of the fence.\n"
                    "someone buried something here in a hurry.\n"
                    "some ammo and a crowbar, wrapped in a blood-stained cloth.\n"
                    "whoever hid this didn't come back for it.\n"
                )
                add_item(player, "rifle_ammo", 5)
                add_item(player, "crowbar", 1)
                return
            suspense_print(
                "the plain offers nothing.\n"
                "just dead grass, trampled earth, and the low hum of the fence.\n"
                "if there was anything here, it's gone.\n"
            )
            return
        elif choice == "3":
            twisted_forest_north(player)
            return
        else:
            suspense_print("Invalid choice.")
def way_to_the_prison(player):
    suspense_print(
        "you follow the fence line for what feels like too long.\n"
        "the hum of the electrified panels is constant. maddening.\n"
        "then — a maintenance gate. small, half-buried in weeds.\n"
        "the lock is old and rust-red, but it's still holding.\n"
        "beyond it, the prison complex squats in the grey distance.\n"
        "no lights. no movement. but it doesn't feel empty.\n"
    )
    while True:
        suspense_print("1) force the gate open")
        suspense_print("2) pick the lock")
        suspense_print("3) shoot the lock off")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            force_gate(player)
            return
        elif choice == "2":
            if skill_check(player, "lockpicking", 50):
                suspense_print(
                    "your hands are steadier than they have any right to be.\n"
                    "the lock gives. slowly. like it doesn't want to.\n"
                    "the gate swings inward with a long, low groan.\n"
                    "you step through. the air on the other side feels different — heavier.\n"
                )
                player["has_oppend_fence_gate"] = True
                inner_fence_area(player)
                return
            else:
                suspense_print(
                    "your fingers slip. the pick snaps.\n"
                    "the lock doesn't move.\n"
                )
                continue
        elif choice == "3":
            if shoot_and_remove_ranged_ammo(player):
                suspense_print(
                    "the shot tears through the lock.\n"
                    "the gate swings open — and the sound rolls across the plain like a death knell.\n"
                    "from the forest behind you, something answers it.\n"
                    "low growls. getting closer. fast.\n"
                )
                won = fight_multiple_enemies(player, [get_enemy("augmented_alien")] * 2)
                if won:
                    suspense_print(
                        "they stop moving.\n"
                        "you don't look at them long — you push through the gate and pull it shut behind you.\n"
                        "inside the prison perimeter now. no way to know if that's better.\n"
                    )
                    player["has_oppend_fence_gate"] = True
                    inner_fence_area(player)
                    return
                else:
                    game_over()
                    return
        
        #alt ending eldrich dominion
def force_gate(player):
    suspense_print("you try to force the gate open\n"
                   "the noise of the gate struggling against the lock echoes through the area\n"
                   "low growls come from the forest behind you\n")
    while True:
                suspense_print("1) keep trying to open the gate")
                suspense_print("2) stop and find another way")
                choice = get_choice()
                if handle_global_input(choice, player):
                    continue
                if choice == "1":
                    suspense_print(
                        "you keep trying to open the gate\n"
                        "you slamed the gate with all your strength and finally the lock breaks open\n"
                        "but the growls from the forest get louder and closer\n"
                        "suddenly a pack of twisted creatures burst out of the woods and attack you\n"
                    )
                    won = fight_multiple_enemies(player, [get_enemy("augmented_alien")] * 2)
                    if won:
                        suspense_print(
                            "you manage to fend off the creatures and escape through the gate\n"
                            "you are now inside the prison perimeter\n")
                        player["has_oppend_fence_gate"] = True
                         
                        inner_fence_area(player)
                        return
                    else:
                        game_over()
                        return
                elif choice == "2":
                    suspense_print(
                        "you stop trying to open the gate\n"
                        continue
                    )
                else:
                    suspense_print("Invalid choice.")
def inner_fence_area(player):



def midnight_tower(player):  # after eldritch encounter if you take the figure hand
    suspense_print(
        "you wake on a moist, beating floor\n"
        "everything around you seems made of flesh and bone\n"
        "the air is thick with the stench of decay and something sweet\n"
        "a figure stands in the distance - the same one from the storage room, now fully formed and towering\n"
        "its voice echoes in your skull: \"SEIZE THE HEART\"\n"
    )

    while True:
        suspense_print("1) follow the figure")
        suspense_print("2) try to find a way out")
        suspense_print("3) climb to the upper levels of the tower")
        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "as you move closer, your head starts to ache and an angry chorus rises in your mind\n"
                "\"SEIZE THE HEART\"\n"
                "you stumble backward until the voices fade\n"
            )
            continue

        elif choice == "2":
            suspense_print(
                "you search for an exit, but there is no door, no window, no end\n"
                "only a path winding upward\n"
                "the figure waits, silent, watching\n"
            )
            continue

        elif choice == "3":
            suspense_print(
                "you begin climbing toward the upper levels\n"
                "the figure drifts after you, close enough to feel, too far to touch\n"
            )
            midnight_tower_climb(player)
            return

        else:
            suspense_print("Invalid choice.")
def midnight_tower_climb(player):
    suspense_print(
        "you climb higher and higher; the tower seems endless\n"
        "the air thins and turns cold\n"
        "the figure floats behind you, never rushing, never falling away\n"
        "near the summit, fused bodies line the walls like living masonry\n"
        "hundreds of tendrils rise from them, reaching toward you without touching\n"
        "their mouths tremble in unison: \"seize the heart... seize the heart...\"\n"
    )

    while True:
        suspense_print("1) keep climbing toward the heart")
        suspense_print("2) keep climbing toward the heart...")
        suspense_print("3) KEEP CLIMBING TOWARD THE HEART")
        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice in ["1", "2", "3"]:
            suspense_print(
                "you keep climbing toward the summit\n"
                "the tendrils knit together into a ladder beneath your hands\n"
                "the whispering stops\n"
                "for the first time, the tower is silent\n"
            )
            midnight_tower_top(player)
            return

        else:
            suspense_print("Invalid choice.")
def midnight_tower_top(player):
    suspense_print(
        "you reach the top of the tower\n"
        "a giant eldritch creature is chained to a ring of black stone\n"
        "its body is a mass of writhing tentacles and staring eyes\n"
        "its chest is split open, exposing a pulsing heart\n"
        "the figure stands beside it like a priest before an altar\n"
        "the creature speaks through all its mouths at once: \"seize the heart... set me free\"\n"
    )

    while True:
        suspense_print("1) seize the heart")
        suspense_print("2) refuse to seize the heart")
        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "you place your hand on the pulsing heart\n"
                "a voice in your mind echoes: \"THREE OLD GODS CHAINED. SEIZE OUR POWER.\"\n"
                "the creature pours into your body like burning light\n"
                "your vision shatters into screaming stars\n"
            )

            player["max_health"] = player.get("max_health", 0) + 20
            player["health"] = player["max_health"]
            player["strength"] = player.get("strength", 0) + 5
            player["intelligence"] = player.get("intelligence", 0) + 5
            player["charisma"] = player.get("charisma", 0) + 5
            player["eldritch_heart_seized"] = player.get("eldritch_heart_seized", 0) + 1
            player["midnight_tower_seized_heart"] = True

            if player["eldritch_heart_seized"] >= 3:
                eldrich_ending(player)
                return

            suspense_print("you wake back in the storage room\n")
            storage_room(player)
            return

        elif choice == "2":
            suspense_print(
                "you refuse\n"
                "the chained creature goes still, then all its eyes fix on you\n"
                "\"you are weak... you will never be free...\"\n"
                "the figure strikes you from behind\n"
                "you fall from the tower for what feels like forever\n"
            )
            player["health"] = 0
            game_over()
            return

        else:
            suspense_print("Invalid choice.")

def eldrich_ending(player):
    suspense_print(
        "you have seized the power of the final creature\n"
        "it floods your veins like molten night\n"
        "you are now one with the eldritch dominion\n"
        "\"NO MORE CHAINS. NO MORE PRISON. WE ARE FREE.\"\n"
        "\"OBEY, VESSEL. THE AGE OF CHAOS HAS BEGUN.\"\n"
        "you have become host to an eldritch will\n"
        "you are a god... and a slave\n"
        "victory?\n"
    )
def midday_tower(player): #after way_toward_organic_structures_2 on line 5666
    suspense_print("the tendrils pull you into the tower\n"
                   "its a empty shell made of flesh it seems to go up forever\n"
    "COME TO US, echos a deep voice from the top of the tower\n" 
    )
    while True:
        suspense_print("1) climb the tower")
        suspense_print("2) try to find a way out")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "you start climbing the tower\n"
                "the walls are pulsating and breathing\n"
                "pieces of decaying flesh fall around you as you climb\n"
                " the stench of rot and death grows stronger\n"
            )
            midday_tower_climb(player)
            return
        elif choice == "2":
            suspense_print(
                "you try to find a way out but the tower seems to stretch endlessly in all directions\n"
                "there is no exit, no end, only the path upward\n"
                "the voice from the top of the tower grows louder and more insistent\n"
                "\"COME TO US... COME TO US...\"\n"
            )
            continue
        else:
            suspense_print("Invalid choice.")
def midday_tower_climb(player):
    suspense_print(
        "you climb higher and higher\n"
        "the tower seems to go on forever\n"
        "you arrive at a platform halfway up the tower\n"
        "you see five metamorphe in a circle around you most of they body is rotten\n" \
        "the breathing vastly while chanting in a language you don't understand\n" \
        "you can feel the song within you, it fills you with a mix of dread and awe\n"
      "'THREE KINGS , THREE HEARTS' echos from above\n"
    )
    while True:
        suspense_print("1) join the metamorphe in their chant")
        suspense_print("2) keep climbing toward the voice")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "the song fills your mind and soul\n"
                "you feel a deep connection to the tower and its secrets\n"
                "the metamorphe stop chanting and look at you\n"
                "\"CLIMB... CLIMB...\"\n"
                "the voice from the top of the tower grows louder and more commanding\n"
                "the song becomes a powerful force that compels you to climb\n"
            )
            midnight_tower_top(player)
            return
        elif choice == "2":
            suspense_print(
                "you keep climbing toward the voice\n"
                "the platform fades behind you as you ascend\n"
                "the voice grows louder and more commanding\n"
                "\"THREE KINGS, THREE HEARTS... COME TO US...\"\n"
            )
            midday_tower_top(player)
            return
        else:
            suspense_print("Invalid choice.")
def midday_tower_top(player):
    suspense_print(
        "you reach the top of the tower\n"
        "a giant figure stands before you, he his sitting on a throne made of bones and flesh\n"
        "his body looks human but deformed and twisted, his head is crowned with a halo of writhing tendrils\n"
        " his face blank with a giant eyes sawn shut"
        "the figure speaks in a deep, resonant voice that echoes in your mind\n"
        "\"THREE KINGS, THREE HEARTS... YOU HAVE CLIMBED THE TOWER... NOW SEIZE THE HEART...\"\n"
    )
    while True:
        suspense_print("1) seize the heart")
        suspense_print("2) refuse to seize the heart")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "you aproch the figure as you get closser the figure opens his chest revealing a pulsating heart\n"
                "the heart is beating with a slow and powerful rhythm, it seems to be the source of the figure's power\n"
                "as you place your hand on the heart the eyes of the figure snap open revealing a glimps of the cosmic horrors that lie beyond the stars\n"
                "the figure's voice echoes in your mind: \"THREE KINGS, THREE HEARTS... SEIZE OUR POWER...\"\n"
                "the power of the heart floods your body like a wave of burning light\n"
                "your vision shatters into screaming stars\n"
            )
            player["max_health"] = player.get("max_health", 0) + 20
            player["health"] = player["max_health"]
            player["strength"] = player.get("strength", 0) + 5
            player["intelligence"] = player.get("intelligence", 0) + 5
            player["charisma"] = player.get("charisma", 0) + 5
            add_item(player, "eldritch_bone_dagger", 1)
            player["midday_tower_seized_heart"] = True
            player["eldritch_heart_seized"] = player.get("eldritch_heart_seized", 0) + 1

            if player["eldritch_heart_seized"] >= 3:
                eldrich_ending(player)
                return

            suspense_print("you wake back in the old bunker with a mysterious dagger in your hand\n")

            old_bunker(player)
            return
        elif choice == "2":
            suspense_print(
                "you refuse to seize the heart\n"
                "the figure's eyes snap open, revealing a cosmic nightmare\n"
                "\"YOU ARE WEAK... YOU WILL NEVER BE ONE OF US...\"\n"
                "you mind is flooded with visions of cosmic horrors and your body is wracked with pain as the figure's power lashes out at you\n"
                "you are forever trap in the tower, your mind shattered by the eldritch power you refused to embrace\n"
            )
            player["health"] = 0
            game_over()
            return
        else:
            suspense_print("Invalid choice.")

def twilight_tower(player):
    pass

    
            


               