#OLD SURVIVOR_BASE
from random import choice

from combat import fight_enemy, combats, get_enemy, gain_xp, player_attack
from inventory import add_item, remove_item, ITEMS
from systems import get_choice, handle_global_input, skill_check, get_current_weapon
from game_area.rooms import grove_town, game_over,old_bunker
from text_effect import suspense_print
from rooms import hospital_road, wasteland_4,randomized_bonus_loot


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
        game_over(player)
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
                game_over(player)

        elif choice == "3":
            underground_complex_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
def underground_complex_main_hall(player):
    suspense_print("you arived in a big hall,before you stand two titanesque rusted bots holding massive shields in front of a door they look inactive"
                   "you also see a stairs going up,some going down and a room going to the right ")
    while True:
        suspense_print("1) examine the bots and open the door")
        suspense_print("2) go up the stairs")
        suspense_print("3) go down the stairs")
        suspense_print("4) go to the right room")
        suspense_print("5) go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("you examine the bots and find keyholes in their shields")
            if player.get("inventory", {}).get("bot_left_shield_key", False) and player.get("inventory", {}).get("bot_right_shield_key", False):
                suspense_print("You use the keys to unlock the bots,heavy grinding noises fill the air as the bots come to life, a red light emanates from their eyes\n"
                               "\"face recognition failed\" 'intruder detected'\n"
                               "the bots start attacking you")
                montain_base_secret_lab_boss(player)
                return
            else:
                suspense_print("you dont have the keys to unlock the bots,maybe you can find them somewhere in the complex")
        elif choice == "2":
            cafeteria(player)
            return  
        elif choice == "3":
            underground_complex_basement(player)
            return
        elif choice == "4":
            legionaire_room(player)
            return
        elif choice == "5":
            underground_complex_inside(player)
            return
        else:
            suspense_print("Invalid choice.")
def montain_base_secret_lab_boss(player):
    pass
def cafeteria(player):
    pass
def underground_complex_basement(player):
    pass
def legionaire_room(player):
    pass
