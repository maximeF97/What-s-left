#OLD SURVIVOR_BASE
from combat import combats
from enemis import get_enemy
from inventory import add_item, remove_item
from systems import get_choice, handle_global_input, skill_check, gain_xp, randomized_bonus_loot
from game_area.rooms import grove_town, game_over, old_bunker, fight_enemy, fight_multiple_enemies
from text_effect import suspense_print


def mountain_tunnel(player):
    player["scene"] = "mountain_tunnel"
    
    # If door is already open, just enter
    if player.get("mountain_door_opened", False):
        suspense_print("The door hangs open. A cold exhale seeps from the darkness beyond.")
        suspense_print("1) Step into the black")
        suspense_print("2) Turn back toward Grovetown")
        choice = get_choice()
        if choice == "1":
            mountain_tunnel_inside(player)
            return
        else:
            grove_town(player)
        return
    
    # Door is locked - check if player has key
    if player.get("inventory", {}).get("mountain_tunnel_key", 0) > 0:
        suspense_print(
            "The key fits. The lock resists — then gives with a sound like cracking bone.\n"
            "Something stirs in the air beyond. Waiting."
        )
        player["mountain_door_opened"] = True
        remove_item(player, "mountain_tunnel_key", 1)
        mountain_tunnel_inside(player)
        return
    
    # No key - can't enter
    suspense_print(
        "A mountain looms over you like a gravestone.\n"
        "A rusted door is set into the rock, sealed. The metal is warm to the touch.\n"
        "Whatever is behind it doesn't want you in. Or maybe it does."
    )
    suspense_print("You need a key. You turn back — quickly.")
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
        "The tunnel swallows you whole.\n"
        "Cold air wraps around your throat like fingers.\n"
        "Something scratches inside the walls — rhythmic, deliberate.\n\n"
        "The tunnel forks ahead.\n"
        "Left: heavy footprints drag through the dirt. Something was hauled this way.\n"
        "Right: a slope descending into a darkness so thick it feels solid."
    )

    while True:
        suspense_print("1) Follow the drag marks left")
        suspense_print("2) Descend into the dark")
        suspense_print("3) Retreat")
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
            if player.get("thomas_seemed_human", False) or player.get("thomas_suspicious", False):
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
                player["thomas_seemed_human"] = True
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
        "The outpost sits in the open like a wound that never closed.\n"
        "A collapsed tent. A device bristling with wires at the center.\n"
        "Bodies everywhere, face-down, limbs bent wrong.\n"
        "Flies. The smell hits you before your eyes adjust."
    )

    if skill_check(player, "perception", 30):
        suspense_print("Some of the bodies appear to be breathing. Very slowly.")

    while True:
        suspense_print("1) Approach the tent")
        suspense_print("2) Examine the device")
        suspense_print("3) Search the bodies")
        suspense_print("4) Get out of here")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("abandoned_outpost_tent_searched"):
                suspense_print(
                    "The tent reeks of sweat and copper.\n"
                    "A journal lies open on the ground, pages stiff with dried blood.\n"
                    "Beside it, scattered rounds, a dented medkit, and a respirator caked in dust."
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
                    "I hope it works.\n"
                    "If it doesn't, I'll use the last bullet on myself."
                )

                player["abandoned_outpost_tent_searched"] = True
            else:
                suspense_print("The tent flaps in the wind. Nothing left but the smell.")

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
        suspense_print("One of the bodies on the right twitches. You almost convince yourself you imagined it.")
        player["abandoned_outpost_right_body_seen_moving"] = True

    while True:
        suspense_print("1) The body on the left, face-down in the dirt")
        suspense_print("2) The body on the right, curled on its side")
        suspense_print("3) The bodies near the device, piled together")
        suspense_print("4) Step away")
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
        suspense_print("You already picked this one clean. Nothing left but rot.")
        body_search(player)
        return

    while True:
        suspense_print("1) Examine the body up close")
        suspense_print("2) Creep in and put a blade through it")
        suspense_print("3) Shoot it from a distance")
        suspense_print("4) Rifle through its pockets")
        suspense_print("5) Leave it alone")
        suspense_print("I) Open inventory")
        
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "You kneel beside it. The face is gone, caved in or chewed off.\n"
                "A small pouch is knotted to its belt, crusted shut.\n"
                "Pale fungus threads through the skin like veins. It smells sweet. Wrong-sweet."
            )
            continue
        elif choice == "2":
            if skill_check(player, "stealth", 30):
                suspense_print(
                    "You slide the blade in. No resistance. No reaction.\n"
                    "Just the wet sound of something that was already dead.\n"
                    "You cut the pouch free. Your hands are shaking."
                )
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(player, {"coin": (5, 10), "revolver_ammo": (1, 3)})
                add_item(player,"abandoned_outpost_left_body_note",1) 
                suspense_print(
                    "The note inside reads:\n\n"
                    "Thomas still hasn't cracked the complex under the outpost.\n"
                    "He says there's something important down there.\n"
                    "I just hope he's right. I can't take another night up here.\n"
                    "Apparently it was an old military base before the blast."
                )
                player["abandoned_outpost_left_body_searched"] = True
                return
            else:
                suspense_print(
                    "Your foot catches a loose rock. You freeze.\n"
                    "Nothing stirs. It was already dead.\n"
                    "Probably."
                )
                continue
        elif choice == "3":
            suspense_print(
                "The shot cracks the silence wide open.\n"
                "The body jerks once from the impact, then nothing.\n"
                "You tear the pouch free with trembling fingers."
            )
            add_item(player, "healing_salve", 2)
            randomized_bonus_loot(player, {"coin": (5, 10), "revolver_ammo": (1, 3)})
            add_item(player,"abandoned_outpost_left_body_note",1)
            suspense_print(
                "The note inside reads:\n\n"
                "Thomas still hasn't cracked the complex under the outpost.\n"
                "He says there's something important down there.\n"
                "I just hope he's right. I can't take another night up here.\n"
                "Apparently it was an old military base before the blast."
            )
            player["abandoned_outpost_left_body_searched"] = True
            return
             
        elif choice == "4":
            suspense_print(
                "You force yourself to search the corpse.\n"
                "The fabric tears like wet paper. Underneath — coins, rounds, and a folded note."
            )
            add_item(player, "revolver_ammo", 3)
            add_item(player, "coin", 10)
            add_item(player,"abandoned_outpost_left_body_note",1) 
            suspense_print(
                "The note reads:\n\n"
                "Thomas still hasn't cracked the complex under the outpost.\n"
                "He says there's something important down there.\n"
                "I just hope he's right. I can't take another night up here.\n"
                "Apparently it was an old military base before the blast."
            )     
            player["abandoned_outpost_left_body_searched"] = True
            return
        elif choice == "5":
            body_search(player)
            return
        else:
            suspense_print("Invalid choice.")
def right_body_search(player):
    if player.get("abandoned_outpost_right_body_searched", False):
        suspense_print("What's left of it barely looks like it was ever alive.")
        body_search(player)
        return

    if player.get("abandoned_outpost_right_body_seen_moving", False):
        suspense_print("You remember the twitch. Your grip tightens.")

    while True:
        suspense_print("1) Get closer")
        suspense_print("2) Creep in with a blade")
        suspense_print("3) Put a bullet in it first")
        suspense_print("4) Walk away")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "You crouch beside it.\n"
                "Its chest rises and falls — but the rhythm is wrong. Too even. Too mechanical.\n"
                "Its fingers twitch. You hold your breath."
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
                    suspense_print("It collapses into a tangle of wet limbs. You search the remains with numb fingers.")
                    player["abandoned_outpost_right_body_searched"] = True
                    add_item(player, "healing_salve", 1)
                    randomized_bonus_loot(
                        player,
                        {"coin": (10, 15), "revolver_ammo": (2, 5), "shotgun_shells": (2, 5)}
                    )
                    return
                else:
                    suspense_print("Everything goes dark.")
                    game_over()

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
                suspense_print("It finally stops. The silence rushes back like a held breath.")
                player["abandoned_outpost_right_body_searched"] = True
                add_item(player, "healing_salve", 1)
                randomized_bonus_loot(
                    player,
                    {"coin": (10, 15), "revolver_ammo": (2, 5), "shotgun_shells": (2, 5)}
                )
                return
            else:
                suspense_print("Everything goes dark.")
                game_over()

        elif choice == "4":
            body_search(player)
            return

        else:
            suspense_print("Invalid choice.")
def center_body_search(player):
    if player.get("abandoned_outpost_center_body_searched", False):
        suspense_print("Just stains and scraps. Nothing living. Nothing you'd want to touch again.")
        body_search(player)
        return

    if skill_check(player, "perception", 40):
        suspense_print("The bodies are moving not randomly. In unison. Breathing together. Like one thing.")

    while True:
        suspense_print("1) Look closer")
        suspense_print("2) Move in with a blade")
        suspense_print("3) Open fire")
        suspense_print("4) Back away slowly")
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
            suspense_print("You hold your breath. Inch forward. The blade feels slippery in your grip.")

            first_success = skill_check(player, "stealth", 30)
            second_success = skill_check(player, "stealth", 40)

            if first_success and second_success:
                suspense_print(
                    "Your blade finds flesh twice.\n"
                    "Quick. Quiet. Surgical.\n"
                    "Dark fluid spills across the ground.\n"
                    "Neither of them made a sound. That somehow makes it worse."
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
                "Your blade catches wrong.\n"
                "Something *twitches* beneath the skin.\n"
                "Then the bodies begin to move."
            )

            enemies = []

            if not first_success:
                enemies.append(get_enemy("small_metamorph"))

            if not second_success:
                enemies.append(get_enemy("small_metamorph"))

            suspense_print(f"{len(enemies)} creature{'s' if len(enemies) > 1 else ''} rise to attack!")

            won = fight_multiple_enemies(player, enemies)
            if won:
                suspense_print("The last spasm fades. The silence that follows is thick enough to choke on.")
                player["abandoned_outpost_center_body_searched"] = True
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(
                    player,
                    {"coin": (15, 20), "revolver_ammo": (3, 6), "shotgun_shells": (3, 6)}
                )
                return
            else:
                suspense_print("Everything goes dark.")
                game_over()


        elif choice == "3":
            suspense_print("Gunfire rips through the dead air. The echo feels like it lasts forever.")
            remove_item(player, "revolver_ammo", 1)
            enemies = [
                get_enemy("small_metamorph"),
                get_enemy("small_metamorph"),
            ]
            enemies[0]["health"] -= 4
            won = fight_multiple_enemies(player, enemies)
            if won:
                suspense_print("The ringing in your ears is the only proof you're still alive.")
                player["abandoned_outpost_center_body_searched"] = True
                add_item(player, "healing_salve", 2)
                randomized_bonus_loot(
                    player,
                    {"coin": (15, 20), "revolver_ammo": (3, 6), "shotgun_shells": (3, 6)}
                )
                return
            else:
                suspense_print("Everything goes dark.")
                game_over()

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
        suspense_print("1) Force the door")
        suspense_print("2) Retreat")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if "mountain_base_secret_lab_key" in player.get("inventory", {}):
                suspense_print(
                    "You use the secret lab key.\n"
                    "The lock clicks open.\n"
                    "You push against the door.\n"
                    "It resists, then slowly grinds open.\n\n"
                )
                remove_item(player, "mountain_base_secret_lab_key", 1)
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
        "The complex opens around you like a throat.\n"
        "Dim emergency lights stutter on the walls, red, then off, then red again.\n"
        "Machinery hums behind the walls. Not broken. Waiting.\n\n"
        "The air tastes of iron and machine oil.\n"
        "Something pulses through the floor beneath your feet, rhythmic, like a heartbeat."
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
    won = fight_multiple_enemies(player, enemies)

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
        game_over()
def _handle_corridor_check(player):
    if skill_check(player, "perception", 30):
        suspense_print(
            "A faint red pulse catches your eye, hidden in the wall seam.\n"
            "Blinking. Watching. Tracking."
        )
        player["has_seen_blinking_red_light"] = True

    elif skill_check(player, "intelligence", 50):
        suspense_print(
            "You've seen this layout before, in military schematics.\n"
            "Automated kill corridor. Designed to leave nothing standing."
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
        suspense_print("2) Toss debris to bait the turrets")
        suspense_print("3) Back away")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "You fire.\n"
                "The panel erupts in sparks and blue flame.\n"
                "The turret array dies with a grinding, mechanical moan.\n"
                "Silence. The kind that follows an execution."
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
                "You hurl a chunk of concrete down the corridor.\n"
                "A turret unfolds from the ceiling, barrel spinning, hunting for a target.\n"
                "It finds you instead."
            )

            won = fight_enemy(player, get_enemy("turret"))
            if won:
                suspense_print("The turret sputters and dies. Oil drips from its housing like tears.")
                add_item(player, "rifle_ammo", 10)
                randomized_bonus_loot(
                    player,
                    {"coin": (20, 30), "alien_power_cell": (1, 2)}
                )
                underground_complex_main_hall(player)
                return
            else:
                suspense_print("Everything goes dark.")
                game_over()

        elif choice == "3":
            underground_complex_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
def underground_complex_main_hall(player):
    suspense_print(
        "The corridor opens into a cavernous hall.\n"
        "Before you — two colossal machines in the shape of men.\n"
        "Rusted. Towering. Holding shields the size of doors.\n"
        "Their eyes are dark. For now.\n\n"
        "Behind them, a sealed door — reinforced, important.\n"
        "Stairs lead up into flickering light. Others descend into silence.\n"
        "A passage opens to the right, swallowed by shadow."
    )
    while True:
        suspense_print("1) Approach the guardian bots")
        suspense_print("2) Climb the stairs")
        suspense_print("3) Descend into the dark")
        suspense_print("4) Enter the right passage")
        suspense_print("5) Go back")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("You approach the bots. Up close, you see keyholes sunk into their shields — precise, deliberate.")
            if player.get("inventory", {}).get("bot_left_shield_key", False) and player.get("inventory", {}).get("bot_right_shield_key", False):
                suspense_print(
                    "You insert both keys. The shields retract with a grinding shriek.\n"
                    "The bots shudder to life — red light floods from their eye sockets.\n\n"
                    "\"FACE RECOGNITION FAILED.\"\n"
                    "\"INTRUDER DETECTED.\"\n\n"
                    "The ground trembles as they advance."
                )
                remove_item(player, "bot_left_shield_key", 1)
                remove_item(player, "bot_right_shield_key", 1)
                montain_base_secret_lab_boss(player)
                return
            else:
                suspense_print("The keyholes stare back at you. Empty. You'll need to find the keys somewhere in this tomb.")
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
def build_lab_boss(beast, player):
    """Mutate the boss based on remaining health."""
    max_hp = beast.get("max_health", beast["health"])
    current_hp = beast["health"]
    hp_pct = current_hp / max_hp

    # Phase 2: Frenzied
    if hp_pct <= 0.6 and not beast.get("phase_2", False):
        beast["phase_2"] = True
        beast["damage"] += 2
        beast["special_attack_chance"] = 0.25
        beast["attack_messages"].extend([
            "The wardens put their heavy shields together before slamming them into you. The impact throws you to the other side of the room, and you can feel your bones cracking under the force of the blow!"
        ])
        suspense_print(
            "An alarm blares through the complex. The bots are damaged but not destroyed. They’re coming for you, and they’re angry."
        )

    # Phase 3: Death Spiral
    if hp_pct <= 0.25 and not beast.get("phase_3", False):
        beast["phase_3"] = True
        beast["damage"] += 3
        beast["special_attack_chance"] = 0.4
        beast["special_attack_multiplier"] = 2.5
        beast["attack_messages"].extend([
            "The bots slam their shields together, creating a shockwave that knocks you off your feet and sends you crashing into the wall. The force is intense enough to leave you gasping for air and struggling to stay conscious."
        ])
        suspense_print(
            "The bots are on the verge of destruction, but they’re not going down without a fight. They’re throwing everything they have at you."
        )

    if hp_pct <= 0.15 and not beast.get("phase_4", False) and not player.get("thomas_allied", False):
        beast["phase_4"] = True
        suspense_print(
            "GET DOWN! Thomas bursts into the room, wielding a makeshift weapon. A powerful laser shoots from the weapon, hitting one of the bots and causing it to spark and falter. Thomas shouts, 'That's all I got, but it should be enough to help you finish them off!'"
        )
        beast["health"] -= 15


def montain_base_secret_lab_boss(player):
    try:
        iron_wardens = get_enemy("iron_wardens")
    except Exception:
        iron_wardens = {
            "name": "Iron Wardens",
            "health": 120,
            "hit_chance": 85,
            "damage": 10,
            "xp": 300,
            "attack_messages": [
                "The Warden brings its fist down like a hammer!"
            ],
            "miss_messages": [
                "The blow shatters the ground beside you."
            ],
            "special_attack_chance": 0.25,
            "special_attack_multiplier": 2.0,
            "special_attack_messages": [
                "Its core glows white-hot as it unleashes a crushing strike!"
            ]
        }
    build_lab_boss(iron_wardens, player)
    suspense_print(
        "The bots lurch forward, their movements stiff but relentless.\n"
        "Their attacks are powerful, but slow. You might be able to outmaneuver them — if you can survive the hits."
    )
    won = fight_enemy(player, iron_wardens)
    won = fight_enemy(player, iron_wardens)
    if won:
        suspense_print(
            "The last bot collapses with a shower of sparks and twisted metal.\n"
            "The sealed door behind them clicks open, revealing a stairwell descending into darkness.\n\n"
            "You’ve made it past the guardians. Whatever’s down there is important. It has to be."
        )
        underground_complex_secret_room(player)
def cafeteria(player):
    suspense_print(
        "You step into what used to be a cafeteria.\n"
        "Dry blood paints the walls in patterns that might mean something — or nothing.\n"
        "Every table is set with trays still full of rotted meat and bone.\n"
        "The smell is ancient and thick. It clings to your throat.\n\n"
        "At the far end, a door pulses with a red light — steady, purposeful, alive."
    )
    while True:
        suspense_print("1) Scavenge the room")
        suspense_print("2) Approach the pulsing door")
        choice = get_choice()
        if choice == "1":
            if skill_check(player, "perception", 30) and not player.get("cafeteria_hidden_compartment_found", False):
                suspense_print(
                    "You notice one table's floorboards sit slightly wrong — warped, deliberate.\n"
                    "Underneath, a hollow space.\n"
                    "Shells. Power cells. Plasma rounds. Someone's stash. Someone who never made it out."
                )
                add_item(player, "shotgun_shells", 4)
                add_item(player, "alien_power_cell", 1)
                add_item(player, "plasma_cells", 1)
                player["cafeteria_hidden_compartment_found"] = True
                player["found_research_development_lab_code"] = True
                suspense_print("Among the scrap is a faded note with the access code for the red-lit door.")
            suspense_print("The room yields nothing else. Just tables and silence and the smell.")
        elif choice == "2":
            suspense_print(
                "You approach the door.\n"
                "The red light pulses faster as you get closer — rhythm accelerating, like a heartbeat that knows you're here.\n"
                "Energy hums from behind it. Warm. Hungry."
            )
            if player.get("found_research_development_lab_code", False):
                suspense_print("You punch in the code you found. The door hisses open, revealing a stairwell descending into absolute darkness.")
                researched_and_development_lab(player)
            else:
                suspense_print("The door is sealed. The light stares at you, unblinking. You need a code.")
        else:
            suspense_print("Invalid choice.")
def researched_and_development_lab(player):
    suspense_print(
        "You enter the research and development lab. It's empty and it looks pristine, like it was never used or someone cleaned it very well. The only thing in the room is a terminal with a blinking red light.\n"
        "A massive blast door is on the other side of the room. The door is slightly open and closes with a mechanical hissing sound. The sign above it says: `S.A.I.D.`"
    )
    while True:
        suspense_print("1) Examine the terminal")
        suspense_print("2) Approach the blast door")
        choice = get_choice()
        if choice == "1":
            suspense_print(
                "The terminal's screen flickers to life as you approach, displaying some research data and logs.\n"
                "The moment you see the data, the screen goes black, and the terminal powers down. The red light on it goes off, and you hear a loud mechanical noise coming from the blast door, like something is moving behind it. You can feel the ground tremble slightly under your feet.\n"
            )
            player["woken_gardian"] = True
            continue
        if choice == "2":
            if player.get("woken_gardian", False):
                suspense_print(
                    "You approach the blast door, and it opens slowly, revealing a massive high-tech legionnaire automaton. Its blade extends as it steps forward, its eyes glowing red as it locks onto you as its target."
                )
                suspense_print(
                    "The legionnaire turns off powering down, and a voice echoes from the back of the dark room, saying: `Hello, sir. I am S.A.I.D.\n"
                    "S-System for Automated Intelligence and Defense...\n"
                    "I was designed to protect this facility and its secrets, but it seems I have been dormant for a long time...`\n"
                    "Come inside. Let's talk."
                )
                underground_complex_said_room(player)
                return
            else:
                suspense_print("The blast door is sealed tight. The red light above it is dark. You can hear something moving behind it, but it's not active yet.")
                continue
def underground_complex_said_room(player):
    suspense_print(
        "You step inside the room, and the blast door closes behind you with a loud mechanical hissing sound, light turn on revealing a massive computer system, with multiple screens and a central console, the wall are filled with vats with wats seems to be brain in them"
        "hello player{name}, i am S.A.I.D. the system for automated intelligence and defense, i was designed to protect this facility and its secrets, but it seems i have been dormant for a long time, i can help you with information about this place and its secrets, but first, i need help"
    )
    while True:
        suspense_print("1) Ask S.A.I.D. for information about the facility")
        suspense_print("2) Ask S.A.I.D. what it needs help with")
        suspense_print("3) Try to shut down S.A.I.D.")
        suspense_print("4) Leave the room")
        choice = get_choice()
        if choice == "1" and not player.get("has_help_said", False):
            suspense_print("help me first, and i will tell you everything you want to know about this place")
        elif choice == "1" and player.get("has_help_said", False):
            question_said(player)
        elif choice == "2":
            suspense_print(
                "S.A.I.D. explains that it was disconnected from the main mainframe of the facility, and it needs to be reconnected in order to access its full capabilities. It asks that you validate a connection request in the general office.\n"
                "You will need this key to get to the general office, but be careful. The place is dangerous, and you will need to be prepared before going there."
            )
            add_item(player, "bot_right_shield_key", 1)
        elif choice == "3":
            suspense_print(
                "You try to shut down S.A.I.D. A mysterious haze fills the air, choking you as you collapse to the ground. You can hear S.A.I.D.'s voice echoing in your head saying: `You can't shut me down. I am the guardian of this place, and I will protect it at all costs... your brain will do great processing power for me now...`"
            )
            game_over()
        elif choice == "4":
            underground_complex_main_hall(player)
            return
def question_said(player):
    suspense_print(
        "S.A.I.D. answers your questions and describes the facility layout. A small compartment opens on the console, and a keycard drops into your hand."
    )
    add_item(player, "armory_keycard", 1)
    player["has_help_said"] = True
    suspense_print("You now have an armory keycard.")
def legionaire_room(player):
    if player.get("power_turnd_on", False):
        suspense_print(
            "You see a massive blast door, scorched and scarred but still sealed tight.\n"
            "The red light above it is dark.\n"
            "there must be a way to turn the power on and open it, but for now, it's just a barrier.")
        underground_complex_main_hall(player)
        return
    if not player.get("power_turnd_on", False) and player.get("first_visite_to_legionaire_room", False):
        suspense_print(
            "With the power back on the blast door opens slowly as you approach, behind it you can hear a fast shifting of gears and a low growl, like something big waking up.\n"
            "The door opens fully, revealing a pristine high tech legionaire automaton, his blade slowly extends as he steps forward, his eyes glowing red as he locks onto you as his target.")
        won = fight_enemy(player, get_enemy("iron_legionnaire"))
        if won:
            suspense_print(
                "The legionnaire collapses, sparks flying from his joints.\n"
                "His eyes go dark. The growling stops.\n"
                "The blast door behind him is now open, the sign above says: `ARMORY`"
            )
            gain_xp(player, 200)
            add_item(player, "rifle_ammo", 20)
            randomized_bonus_loot(
                player,
                {"coin": (50, 100), "alien_power_cell": (2, 4), "shotgun_shells": (10, 20)}
            )
            player["first_visite_to_legionaire_room"] = True

            underground_complex_armory(player)
            return
        else:
            suspense_print("Everything goes dark.")
            game_over()
    if not player.get("power_turnd_on", False) and not player.get("first_visite_to_legionaire_room", False):
        suspense_print("The legionnaire is still tweaking on the ground. Why was it not rusted like the other machines?")
        while True:
            suspense_print("1 go the the armory")
            suspense_print("2) go back to the main hall")
            choice = get_choice()
            if choice == "1":
                underground_complex_armory(player)
                return
            elif choice == "2":
                underground_complex_main_hall(player)
                return
            else:
                suspense_print("Invalid choice.")

def underground_complex_armory(player):
    suspense_print(
        "You enter the armory. The walls are lined with racks of weapons and armor—most damaged and rusted, but some pieces remain in good condition.\n"
        "Behind an airtight plexiglass wall at the back, a sleek high-tech exosuit and a beautiful plasma rifle rest on a pedestal. The sign above reads: `EXPERIMENTAL WEAPONRY - DO NOT TOUCH - Thomas'"
    )
    while True:
        suspense_print("1) Scavenge the armory")
        suspense_print("2) Try to access the experimental weaponry")
        suspense_print("3) Go back")
        choice = get_choice()
        if choice == "1":
            if skill_check(player, "perception", 30) and not player.get("armory_hidden_compartment_found", False):
                suspense_print(
                    "You notice one of the weapon racks is slightly loose.\n"
                    "Behind it, a hidden compartment.\n"
                    "Inside: grenades, energy cells, and a prototype combat stim."
                )
                add_item(player, "grenade", 2)
                add_item(player, "magnum_ammo", 2)
                add_item(player, "combat_stim", 1)
                player["armory_hidden_compartment_found"] = True
            suspense_print("The armory yields nothing else. Just racks and silence.")    
        if choice == "2":
            suspense_print(
                "You try to access the experimental weaponry, but it's locked behind a security system.\n"
                "A card reader wait blinking red. You need a keycard to access it."
            )
            if player.get("inventory", {}).get("armory_keycard", False):
                suspense_print("You insert the keycard into the reader.")
                suspense_print(
                    "The system beeps and the plexiglass wall slides open.\n"
                    "You step inside, the airlock seals behind you.\n"
                    "The plasma rifle hums with barely contained energy. The exosuit looks like it could withstand a nuclear blast."
                )
                add_item(player, "plasma_rifle", 1)
                add_item(player, "experimental_exosuit", 1)
            else:
                suspense_print("You don't have the right keycard.")

#downstairs area
def underground_complex_basement(player):
    suspense_print(
        "Sound dies in the basement. Cold presses at your bones, heavy as a hand. Rust runs down the machines like old tears. The floor is painted with dried blood — dragged in long streaks, as if something was hauled away. No body. No remains. Just the proof that whatever happened here left on its own feet."
    )
    while True:
        suspense_print("1) Examine the machine")
        suspense_print("2) Search the room")
        suspense_print("3) Go to the next room")
        suspense_print("4) Go back")
        choice = get_choice()
        if choice == "1":
            suspense_print(
                "The machine dominates the center of the room — towering, skeletal, wrong.\n"
                "Wires bristle from its frame like antennae.\n"
                "Bullet holes perforate its metal skin. Dozens of them.\n"
                "Someone tried very hard to kill it.\n\n"
                "A faint pulse emanates from its core. Not electric. Not quite.\n"
                "Something in there is still alive. Still waiting."
            )
            if skill_check(player, "perception", 30) and skill_check(player, "intelligence", 30) and not player.get("basement_machine_deactivated", False):
                suspense_print(
                    "Your instincts scream. This machine, it's a prototype. An experiment.\n"
                    "Responsible for the blood. For whatever walked out of here.\n\n"
                    "Your hands move through the security protocols shutting it down, layer by layer.\n"
                    "The pulse dies. The machine goes silent for the first time in years.\n\n"
                    "In its hollow core: rifle rounds someone tried to use against it. Useless.\n"
                    "You take them anyway. Better than leaving them."
                )
                add_item(player, "rifle_ammo", 10)
                gain_xp(player, 150)
                player["basement_machine_deactivated"] = True

            else:
                suspense_print(
                    "The machine is beyond your understanding.\n"
                    "The wiring, the design — it makes your head ache to look at it.\n"
                    "Some things are better left alone. This is one of them."
                )
                continue
        elif choice == "2":
            if skill_check(player, "luck", 80) and not player.get("find_secret_ray_gun_in_basement", False):
                suspense_print(
                    "You're about to leave when your boot catches something beneath the floorboards.\n"
                    "The wood gives way — rotten, deliberate.\n\n"
                    "Inside the hidden compartment: a weapon unlike anything you've seen.\n"
                    "Sleek. Ancient. Still humming with barely-contained power.\n"
                    "A ray gun. The kind that turns things to ash.\n\n"
                    "A faded note sits beside it, written in desperate handwriting:\n"
                    "'Experimental prototype. One charge remaining.\n"
                    "Can annihilate anything in its path — but only once.\n"
                    "We couldn't figure out how to recharge it. We tried.\n"
                    "If you're reading this, things got bad. Use it wisely.\n"
                    "Or don't. Maybe it's better if this never fires.'"
                )
                add_item(player, "secret_ray_gun", 1)
                add_item(player, "ray_gun_note", 1)
                player["find_secret_ray_gun_in_basement"] = True
            suspense_print("The room yields nothing else. Just blood and silence.")
        elif choice == "3":
            underground_complex_reactor_room(player)
            return  
        elif choice == "4":
            underground_complex_inside(player)
            return
        else:
            suspense_print("Invalid choice.")
def underground_complex_reactor_room(player):
    suspense_print(
        "The reactor chamber reeks of ozone and decay.\n"
        "A colossal core throbs at the center, veins of glowing conduits pulsing like infected arteries.\n"
        "The air burns your lungs radiation crawling beneath your skin\n\n"
        "The floor is slick with congealed blood, dragged in long, desperate streaks toward the next room.\n"
        "The same blood from the basement. Whatever bled here... it didn't stop."
    )
    while True:
        suspense_print("1) Approach the reactor core")
        suspense_print("2) Follow the blood trail to the next room")
        suspense_print("3) Go back")
        choice = get_choice()
        if choice == "1":
            reactor_interaction(player)
        elif choice == "2":
            suspense_print(
                "You follow the blood trail to the next room.\n"
                "The door opens but stops after a few inches, not enough power to open fully.\n"
            )
            if player.get("power_turnd_on", False):
                suspense_print(
                    "you follow the blood trail to the next room.\n"
                    "for a moment, you think the door is stuck. Then it shudders and swings open, powered by the reactor's energy.\n"
                )
                vangard_room(player)
            return
        elif choice == "3":
            underground_complex_inside(player)
            return
        else:
            suspense_print("Invalid choice.")
def reactor_interaction(player):
    if player.get("power_turnd_on", False):
        suspense_print("The reactor is already running, its hum a constant, maddening drone.")
        return

    suspense_print(
        "You approach the reactor core.\n"
        "The hum escalates to a bone-rattling roar, vibrating through your marrow.\n"
        "Raw power courses through the room like a living thing  hungry, aware.\n\n"
        "The control panel is corroded, stained with what might be blood or worse."
    )

    while True:
        suspense_print("1) Attempt to power on the reactor")
        suspense_print("2) Step back")
        choice = get_choice()
        if choice == "1":
            if skill_check(player, "intelligence", 40):
                suspense_print(
                    "You claw at the controls, deciphering the maddening interface.\n"
                    "After an eternity of tension, you shatter the safety locks and ignite the reactor.\n"
                    "The roar crescendos as energy floods the complex. The door to the next room awakens, hissing open like a predator's maw."
                )
                gain_xp(player, 100)
                add_item(player, "alien_power_cell", 1)
                randomized_bonus_loot(
                    player,
                    {"coin": (20, 30), "rifle_ammo": (10, 15)}
                )
                player["power_turnd_on"] = True
                vangard_room(player)
                return
            else:
                suspense_print(
                    "You tamper with the reactor, and it rebels.\n"
                    "Sparks erupt in a frenzy. The hum warps into a shrieking howl.\n"
                    "The core overloads, unleashing a blast that hurls you into darkness."
                )
                player["health"] -= 10
                if player["health"] > 0:
                    suspense_print("You stagger upright as the reactor stabilizes — barely. It's dormant, but the silence feels like a threat.")
                    continue
                else:
                    suspense_print("The darkness claims you.")
                    game_over()
        elif choice == "2":
            underground_complex_inside(player)
            return
        else:
            suspense_print("Invalid choice.")
def vangard_room(player):
    if player.get("defeated_vanguards_basement", False):
        suspense_print(
            "You're back in the vanguard room. The silence is heavier now.")
        while True:
            suspense_print("1) Go to the storage room")
            suspense_print("2) Go to the reactor room")
            choice = get_choice()   
            if choice == "1":
                alien_storage_room(player)
                return
            elif choice == "2":
                underground_complex_reactor_room(player)
                return
            else:
                suspense_print("Invalid choice.")
    suspense_print(
        "You enter the room. Darkness swallows you for a heartbeat, then the door slams shut with a final, echoing thud.\n"
        "The reactor's energy surges through the walls, lights flickering to life — revealing two rusted sentinels.\n"
        "Their eyes ignite with crimson malice, locking onto you like prey.\n"
        "Time has corroded them, but their purpose remains: to kill."
    )
    won = fight_multiple_enemies(player, [get_enemy("rustbound_vanguard"), get_enemy("rustbound_vanguard")])
    if won:
        suspense_print(
            "The vanguards crumple into jagged heaps of metal.\n"
            "The door to the next room unlocks with a predatory hiss."
        )
        gain_xp(player, 150)
        add_item(player, "shotgun_shells", 10)
        randomized_bonus_loot(
            player,
            {"coin": (20, 30), "alien_power_cell": (1, 2)}
        )
        alien_storage_room(player)
        player["defeated_vanguards_basement"] = True
        return
    else:
        suspense_print("The darkness consumes you.")
        game_over()
def alien_storage_room(player): 
    suspense_print(
        "The storage room is a tomb of crates and alien-marked containers.\n"
        "In the shadows, vats bubble with murky fluid, holding corpse-like forms, twisted, surgical scars crisscrossing their flesh, wires embedded like parasites.\n"
        "The stench of chemicals and rot clings to everything.\n"
        "The blood trail from before leads behind the vats, where something waits."
    )
    while True:
        suspense_print("1) Search the crates")
        suspense_print("2) Examine the vats")
        suspense_print("3) Follow the blood trail to the sealed container")
        suspense_print("4) Go back")
        choice = get_choice()
        if choice == "1":
            if skill_check(player, "perception", 30) and not player.get("found_alien_tech_in_storage_room", False):
                suspense_print(
                    "You rifle through the crates, uncovering alien tech that still pulses with unnatural life.\n"
                    "A device hums faintly — an energy cell that could power forbidden weapons.\n"
                    "Beside it, a psychic artifact whispers at the edges of your mind, promising horrors."
                )
                add_item(player, "alien_energy_cell", 1)
                add_item(player, "psychic_artifact", 1)
                player["found_alien_tech_in_storage_room"] = True
            else:
                suspense_print("The crates yield only debris and the echoes of screams.")
        elif choice == "2":
            suspense_print(
                "You peer into the vats. The forms within are abominations humanoid shapes warped into monstrosities.\n"
                "Surgical scars mar their flesh, wires snaking beneath skin like living veins.\n"
                "These were experiments. Living nightmares, frozen in agony.\n"
                "The sight twists something inside you."
            )
        elif choice == "3":
            if not player.get("found_red_striped_keycard", False):
                suspense_print(
                    "You follow the blood trail to a slumped skeleton, armor shattered, body rent asunder.\n"
                    "In its bony grasp: a red-striped keycard, stained with the owner's final moments."
                    "You take the keycard, it might be useful. you also notice a gun behind the skeleton, its a SFX9 handgun, top of the line.")
                add_item(player, "sfx9_handgun", 1)
                add_item(player, "bot_left_shield_key", 1)
                player["found_red_striped_keycard"] = True
            else:
                suspense_print("you've already found the keycard, the skeleton is just a grim reminder of what happened here.")
        elif choice == "4":
            vangard_room(player)
            return
        else:
            suspense_print("Invalid choice.")

#final zone
def underground_complex_secret_room(player):
    suspense_print(
        "You step through the opened door and into the heart of the facility.\n"
        "Dim lights reveal a chamber lined with dormant equipment and a final console at the center.\n"
        "The air hums with a low, patient energy. This room feels like the end of a long, terrible path."
    )
    suspense_print("For now, the secrets here are not yet unlocked.")
    return