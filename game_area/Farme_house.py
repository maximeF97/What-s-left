import random

from text_effect import suspense_print, slow_print_word
from combat import fight_enemy, combats, get_enemy, gain_xp, player_attack
from inventory import add_item, remove_item, ITEMS
from systems import get_choice, handle_global_input, skill_check, get_current_weapon
from game_area.rooms import old_farm_house

def farm_house_inside(player):
    suspense_print("You enter the old farmhouse. A dark living room yawns ahead; furniture slumps under a skin of dust.")
    if skill_check(player, "perception", 30):
        suspense_print("A low growl filters down from upstairs. Better be careful.")
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
        suspense_print("2) Go back to the hallway")
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
            suspense_print("You step back into the hallway.")
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
                suspense_print(
                    "You kneel beside the corpse. A massive claw mark splits the chest open.\n"
                    "You find a few coins and a folded note pressed under the ribs."
                )
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
            "Blood sprays as it slams into you again and again!"
        ])
        suspense_print(
            "The bat screams. Something breaks inside it.\n"
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
            # Loot flow already routes to post-beast attic.
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
                suspense_print("You back away. The attic swallows your footsteps.")
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
    if not player.get("farm_house_attic_beast_looted", False):
        gain_xp(player, 100)
    suspense_print("You deliver the final blow. A scream threads the beams and then comes apart.")
    player["beast_in_farm_house_defeated"] = True
    if not player.get("farm_house_attic_beast_looted", False):
        add_item(player, "sharp_wing_claw", 1)
        player["farm_house_attic_beast_looted"] = True
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