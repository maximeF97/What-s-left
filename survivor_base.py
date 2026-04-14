from game_area.rooms import farm_house_inside, old_farm_house, wasteland_3 
from inventory import add_item, remove_item, ITEMS
from text_effect import suspense_print
from combat import fight_enemy, combats, get_enemy, gain_xp, player_attack
from systems import get_choice, handle_global_input, skill_check, get_current_weapon


def survivor_base(player):
    """Compatibility entry point imported by rooms.py."""
    old_farm_house(player)


def survivor_montain_base(player):
    if "survivor_base_access_card" in player.get("inventory", {}):
        suspense_print("You use the access card to enter the base. You feel watched.")
        survivor_mountain_base_inside(player)
        return
    suspense_print(
        "You follow the map behind the farmhouse.\n"
        "After a long trek, you arrive at a hidden mountain base.\n"
        "At the front gate, a guard waits with a rifle in hand."
    )
    suspense_print("1) talk to the guard")
    suspense_print("2) go back to the farmhouse")
    suspense_print("I) Open inventory")
    if player.get("has_received_survivor_base_access_card", False):
        if "survivor_base_access_card" not in player.get("inventory", {}):
            add_item(player, "survivor_base_access_card", 1)
        suspense_print("The guard recognizes you and lets you through.")
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
                "You explain that John gave you the map when you saved him from the alien prison and that you seek refuge.\n"
                "He nods slowly, then steps aside to let you in.\n\n"
                "Inside, you find a community of survivors."
            )
            add_item(player, "survivor_base_access_card", 1)
            player["has_received_survivor_base_access_card"] = True
            survivor_mountain_base_inside(player)
            return
        elif choice == "2":
            suspense_print("You head back to the farmhouse.")
            old_farm_house(player)
            return
        else:
            suspense_print("Invalid choice.")


def survivor_mountain_base(player):
    """Alias with corrected spelling kept for compatibility."""
    survivor_montain_base(player)


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
            if (
                player.get("leader_radio_quest_accepted", False)
                and not player.get("has_completed_leader_quest", False)
                and "radio_device" in player.get("inventory", {})
            ):
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
            elif (
                player.get("has_accepted_leader_second_quest", False)
                and not player.get("has_completed_leader_second_quest", False)
                and "energy_core" in player.get("inventory", {})
            ):
                suspense_print(
                    "You approach the leader.\n"
                    "She looks at you with weary eyes.\n\n"
                    "\"You have the energy core,\" she says.\n"
                    "\"This will help power the base's defenses.\"\n\n"
                    "You hand over the energy core.\n"
                    "Thank you. she says with a faint glimmer of hope."
                )
                player["has_completed_leader_second_quest"] = True
                if player.get("thomas_allied", False):
                    suspense_print(
                        "Oh - Thomas has returned. He has something to discuss with you.\n"
                        "You should go find him."
                    )
                    player["can_accept_thomas_quest"] = True
                remove_item(player, "energy_core", 1)
                gain_xp(player, 100)
                add_item(player, "coin", 50)
                add_item(player, "rifle",1)
                add_item(player, "rifle_ammo", 10)
                add_item(player, "weird_fruit", 1)
                continue
            elif "radio_device" in player.get("inventory", {}):
                suspense_print(
                    "You approach the leader.\n"
                    "She notices the device and narrows her eyes.\n\n"
                    "\"If you want to hand that over, hear me out first,\" she says."
                )
                remove_item(player, "radio_device", 1)
                leader_quest(player)
                continue
            elif "energy_core" in player.get("inventory", {}):
                suspense_print(
                    "You approach the leader.\n"
                    "The core's glow reflects in her face.\n\n"
                    "\"I need to explain what that means for this base before we use it,\" she says."

                )
                remove_item(player, "energy_core", 1)
                leader_second_quest(player)
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
                "She gives you the key to the outpost.\n"
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
                "The leader explains that the outpost was attacked during the night.\n"
                "Too many died before the survivors could retreat.\n"
                "They fled fast and left critical supplies behind.\n\n"
                "The radio device projects a high-frequency shield that disrupts metamorph shifts.\n"
                "\"It's in a dangerous area beyond the mountain tunnel near Grove Town,\" she warns.\n"
                "\"But if anyone can get it, it's you.\""
            )
        else:
            suspense_print("Invalid choice.")
def leader_second_quest(player):
    suspense_print(
        "The leader’s voice is quiet.\n\n"
        "\"This wasn’t the first incident,\" she admits.\n"
        "\"We tried activating the radio device… but it needs power.\"\n\n"
        "\"An energy core is required to run it.\"\n\n"
        "\"The only known source is beyond the hospital.\n"
        "In the old military research base.\"\n\n"
        "\"Past the terraformed zone. In alien land.\"\n\n"
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
                "The leader explains that the energy core is a rare near-limitless military power source.\n"
                "It can be found in the old research base near the hospital.\n"
                "She warns you that the base is heavily infested with metamorphs and other alien creatures.\n"
                "Only a few have ever returned from there."
            )
            continue
        else:
            suspense_print("Invalid choice.")
def thomas_quest(player):   
    suspense_print(
        "Thomas looks at you with hopeful eyes.\n\n"
        "\"I need your help,\" he says.\n"
        "\"I finally unlocked the door to the secret lab.\"\n\n"
        "\"But the security system is still active.\"\n"
        "\"Many security bots are patrolling the area.\"\n\n"
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
                "It contains advanced technology that could help humanity fight back against the alien threat.\n"
                "It was a weapons research lab before the invasion.\n"
                "He warns you that the security bots are heavily armed and dangerous.\n"
                "They will attack anyone who enters the lab without authorization.\n"
                "You can keep any useful weapons or items you find there.\n"
                "He only needs them disabled so he can finish his work."
            )
            continue
            
        else:
            suspense_print("Invalid choice.")    
