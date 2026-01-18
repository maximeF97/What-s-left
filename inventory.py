from equipment import EQUIPMENT
import random
# -----------------------------
# Input helper (local, safe)
# -----------------------------
def get_choice():
    return input("> ").lower()


# -----------------------------
# INVENTORY UI
# -----------------------------
def open_inventory(player):
    while True:
        print("\n--- Inventory ---")

        print("EQUIPPED:")
        for slot, item in player["equipment"].items():
            if item:
                print(f"  {slot.capitalize()}: {item.replace('_', ' ')}")
            else:
                print(f"  {slot.capitalize()}: (empty)")

        print("\nITEMS:")
        if not player["inventory"]:
            print("Your inventory is empty.")
        else:
            for i, (item, qty) in enumerate(player["inventory"].items(), 1):
                print(f"{i}) {item.replace('_', ' ')} x{qty}")

        print("\nOPTIONS:")
        print("  [number] Inspect item")
        print("  U) Unequip item")
        print("  X) Use item")
        print("  B) Back")

        choice = get_choice()

        if choice == "b":
            return
        elif choice == "u":
            unequip_menu(player)
        elif choice == "x":
            use_item(player)
        elif choice.isdigit():
            index = int(choice) - 1
            items = list(player["inventory"].keys())
            if 0 <= index < len(items):
                try:
                    from systems import inspect_item
                    inspect_item(player, items[index])
                except ImportError:
                    print("Unable to inspect item right now.")
        else:
            print("Invalid choice.")


# -----------------------------
# EQUIPMENT
# -----------------------------
def unequip_menu(player):
    print("\nUNEQUIP WHICH SLOT?")
    slots = list(player["equipment"].keys())

    for i, slot in enumerate(slots, 1):
        current = player["equipment"][slot]
        name = current.replace("_", " ") if current else "(empty)"
        print(f"{i}) {slot.capitalize()} — {name}")

    print("B) Back")
    choice = get_choice()

    if choice == "b":
        return

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(slots):
            try:
                from systems import unequip_item
                unequip_item(player, slots[index])
            except ImportError:
                print("Unable to unequip right now.")


# -----------------------------
# INVENTORY HELPERS
# -----------------------------
def add_item(player, item, amount=1):
    player["inventory"][item] = player["inventory"].get(item, 0) + amount
    print(f"Added {amount} x {item.replace('_', ' ')}")


def remove_item(player, item, amount=1):
    if player["inventory"].get(item, 0) < amount:
        return False
    player["inventory"][item] -= amount
    if player["inventory"][item] <= 0:
        del player["inventory"][item]
    return True


def has_item(player, item, amount=1):
    return player["inventory"].get(item, 0) >= amount

def use_consumable(player: dict, item_id: str) -> bool:
    item = ITEMS.get(item_id)
    if not item or item.get("type") != "consumable":
        print("That item cannot be used.")
        return False

    if player.get("inventory", {}).get(item_id, 0) <= 0:
        print("You don't have that item.")
        return False

    # Apply skill boosts
    for skill, amount in item.get("skill_boost", {}).items():
        player.setdefault("temporary_skill_boosts", {})
        player["temporary_skill_boosts"][skill] = (
            player["temporary_skill_boosts"].get(skill, 0) + amount
        )

    remove_item(player, item_id, 1)

    print(f"You use {item['name']}. You feel more capable.")
    return True

from combat import take_damage,heal_player

def handle_weird_fruit(player):
    player.setdefault("weird_fruit_eaten", 0)
    player.setdefault("status_effects", {})

    player["weird_fruit_eaten"] += 1
    count = player["weird_fruit_eaten"]

    print("The fruit tastes wrong. Sweet… and metallic.")

    # Early unease
    if random.random() < 0.2:
        print("For a moment… you swear it moves in your stomach.")

    # 🍽️ Always heal a bit when eaten
    heal_player(player, 4)
    
    # 🔍 3 fruits → perception bonus
    if count == 3:
        print("Your senses sharpen. Sounds feel closer. Shadows clearer.")
        player["status_effects"]["perception_bonus"] = 1

    # 🔍 Scaling perception (soft cap)
    if count > 3:
        player["status_effects"]["perception_bonus"] = min(3, 1 + count // 5)

    # 👽 10 fruits → aliens stop attacking
    if count == 7:
        print("Something inside you stirs… and the world feels quieter.")
        print("Alien creatures hesitate when they look at you.")
        player["status_effects"]["alien_marked"] = True
        player["can_breathe_in_alien_environments"] = True
        player["has_eaten_10_fruits"] = True
    # ☠️ Too many fruits → body rejection
    if count >= 8 and random.random() < 0.1:
        print("Pain erupts inside you."
              "tentacles erupt from your skin, writhing wildly before retracting back.")
        take_damage(player, 25)


# -----------------------------
# NOTES
# -----------------------------
def read_note(player, note_id):
    notes = {
        "wastland_field_note": (
            "Something is watching the roads.\n"
        ),

        "wasteland_note_small_1": (
            "Saw one near the ruins.\n"
            "Small. Fast. Curious.\n\n"
            "It didn’t attack.\n"
            "Just watched.\n"
            "Like an animal.\n"
        ),

        "wasteland_2_note": (
            "They’re everywhere.\n"
            "I don’t know when it started.\n\n"
            "They don’t always look alien.\n"
            "Sometimes they look… familiar.\n\n"
            "If you’re reading this,\n"
            "don’t trust what you see.\n"
            "Don’t sleep."
        ),

        "wasteland_note_small_2": (
            "The little ones aren’t soldiers.\n"
            "They scatter when shot.\n"
            "Unlike the big one they can breathe our air.\n\n"
            "I think they’re wildlife.\n"
            "Or pets.\n\n"
            "God help us if they grow."
        ),

        "farmer_note": (
            "A small, bat-shaped thing started haunting the farm.\n"
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
        ),

        "grovetown_note_1": (
            "There are two kinds.\n"
            "I’m sure of it now.\n\n"
            "The small ones mimic shapes.\n"
            "Animals. Objects. Trash.\n\n"
            "The tall ones mimic *us*."
        ),

        "grovetown_note_2": (
            "The humanoids don’t hunt like animals.\n"
            "They set traps.\n"
            "They wait.\n\n"
            "One of them watched me eat.\n"
            "Like it was studying how."
        ),

        "hospital_terminal_log_1": (
            "Atmospheric mismatch confirmed.\n"
            "Humanoid entities show respiratory distress\n"
            "in unaltered Earth air.\n\n"
            "They avoid long exposure.\n"
            "They *need* the terraformed zones."
        ),

        "hospital_note_doctor": (
            "They’re intelligent.\n"
            "More than we thought.\n\n"
            "But they choke here.\n"
            "That’s why they send the small ones first.\n\n"
            "Scouts.\n"
            "Pets.\n"
            "Weapons."
        ),
        "abandoned_outpost_journal": (
            "Another shooting happened.\n"
                    "A mother shot her son. Said his eyes moved wrong.\n\n"
                    "Nobody trusts anyone anymore.\n"
                    "Thomas is building a device to interfere with their morphing.\n"
                    "I hope it works."
        ),
        "abandoned_outpost_left_body_note": (
            "thomas still havent find a way to get the the complex under the outpost\n"
            "he say there is someting important down there\n"
            "i just hope he is right and we can get out of this hell\n"   
            "apparently it was an old secret military base before the blast"
        ),
        "wasteland_note_small_2": ("Found this place while escaping.\n"
        "Safe from the creatures above.\n\n"
        "Left some supplies here.\n"
        "Might come back later.\n\n"
        "If you find this,\n"
        "use them well."
        ),
        "scout_note":("The factory was supposed to be abandoned, but I just saw an alien\n"
                        "in serious gear leaving. He came back with bugs in a jar...\n"
                        "A ship landed. They loaded vats inside.\n"
                        "Something big is happening.\n"
                        "I need to g—"),
    }

    print(notes.get(note_id, "The note is unreadable."))



# -----------------------------
# USE ITEM (CLEAN VERSION)
# -----------------------------
def use_item(player):
    if not player["inventory"]:
        print("You have nothing to use.")
        return

    items = list(player["inventory"].keys())

    print("Choose an item to use:")
    for i, item in enumerate(items, 1):
        print(f"{i}) {item.replace('_', ' ')} x{player['inventory'][item]}")

    choice = get_choice()
    if not choice.isdigit():
        print("Invalid choice.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(items):
        print("Invalid item.")
        return

    item_id = items[index]
    data = ITEMS.get(item_id)

    if not data:
        print("You don’t understand how to use this.")
        return

    item_type = data.get("type", "misc")

    # -------- CONSUMABLE --------
    if item_type == "consumable":
        heal = data.get("heal", 0)
        max_bonus = data.get("max_health_bonus", 0)

        if heal:
            player["health"] = min(
                player["health"] + heal,
                player["max_health"]
            )

        if max_bonus:
            player["max_health"] += max_bonus

        remove_item(player, item_id, 1)

        print(f"You use the {data['name']}.")
        if heal:
            print(f"+{heal} health")
        if max_bonus:
            print("You feel changed.")

        print(f"Health: {player['health']}/{player['max_health']}")
        return

    # -------- NOTE --------
    if item_type == "note":
        read_note(player, item_id)
        return

    # -------- AMMO --------
    if item_type == "ammo":
        print("You can’t use ammo directly.")
        return

    # -------- TOOL / MISC --------
    print(data.get("description", "Nothing happens."))


# -----------------------------
# ITEM DATABASE
# -----------------------------
ITEMS = {
    # CONSUMABLES
    "medkit": {
        "name": "Medkit",
        "type": "consumable",
        "heal": 5,
        "sell": 1,
        "buy": 5,
    },
    "healing_salve": {
        "name": "Healing Salve",
        "type": "consumable",
        "heal": 3,
        "sell": 1,
        "buy": 3,
    },
    "canned_food": {
        "name": "Canned Food",
        "type": "consumable",
        "heal": 2,
        "sell": 1,
        "buy": 2,
    },
    "weird_fruit": {
        "name": "Weird Fruit",
        "type": "consumable",
        "heal": 4,
        "max_health_bonus": 1,
        "on_use": handle_weird_fruit,
        "sell": 2,
        "buy": 6,
    },
    "centipede_chitin": {
        "name": "Centipede Chitin",
        "type": "consumable",
        "heal": 1,
        "sell": 5,
        "buy": 7,
    },
    # TOOLS
    "bobby_pins": {
        "name": "Bobby Pins",
        "type": "tool",
        "description": "Perfect for lockpicking.",
        "sell": 1,
        "buy": 2,
    },
    
    # AMMO
    "revolver_ammo": {
        "name": "Revolver Ammo",
        "type": "ammo",
        "sell": 1,
        "buy": 3,
    },
    "rifle_ammo": {
        "name": "Rifle Ammo",
        "type": "ammo",
        "sell": 1,
        "buy": 3,
    },
    "shotgun_shells": {
        "name": "Shotgun Shells",
        "type": "ammo",
        "sell": 1,
        "buy": 4,
    },
    "alien_energy_cell": {
        "name": "Alien Energy Cell",
        "type": "ammo",
        "sell": 5,
        "buy": 15,
    },
    "magnum_ammo": {
        "name": "Magnum Ammo",
        "type": "ammo",
        "sell": 2,
        "buy": 5,
    },

    # NOTES
    "farmer_note": {
        "name": "Farmer's Note",
        "type": "note",
    },
    "grovetown_note_1": {
        "name": "Grovetown Note",
        "type": "note",
    },
        
    "wastland_field_note": {
        "name": "Wasteland Field Note",
        "type": "note",
    },
    "wasteland_note_small_1": {
        "name": "Wasteland Note (Small I)",
        "type": "note",
    },
    "wasteland_2_note": {
        "name": "Wasteland Note II",
        "type": "note",
    },
    "wasteland_note_small_2": {
        "name": "Wasteland Note (Small II)",
        "type": "note",
    },
    "farmer_note": {
        "name": "Farmer's Note",
        "type": "note",
    },
    "grovetown_note_1": {
        "name": "Grovetown Note I",
        "type": "note",
    },
    "grovetown_note_2": {
        "name": "Grovetown Note II",
        "type": "note",
    },
    "hospital_terminal_log_1": {
        "name": "Hospital Terminal Log",
        "type": "note",
    },
    "hospital_note_doctor": {
        "name": "Doctor's Note",
        "type": "note",
    },
    "abandoned_outpost_journal": {
        "name": "Abandoned Outpost Journal",
        "type": "note",
    },
    "abandoned_outpost_left_body_note": {
        "name": "Left Body Note",
        "type": "note",
    },
    "alien_tech_part": {
        "name": "Alien Tech Part",
        "type": "misc",
        "description": "A fragment of alien technology. It hums faintly.",
    },
    #_____Quest Items_____
    "radio_device": {
        "name": "Radio Device",
        "type": "quest_item",
        "description": "A strange, unstable radio device.",
    },
    "energy_core": {
        "name": "Energy Core",
        "type": "quest_item",
        "description": "A near limitless power source used in military technology.",
    },"scout_note": {
        "name": "Scout Note",
        "type": "note",
        "description": "A hastily written note from a scout about alien activity.",
    },
    #_____Skill_Boosters_____
    #impliment later
    "scavenging_notebook": {
        "name": "Scavenging Notebook",
        "type": "consumable",
        "skill_boost": {
            "scavenging": 2
        },

        "description": "A scavenger notebook filled with tips on scavenging.",
    },
    "lockpicking_guide": {
        "name": "Lockpicking Guide",
        "type": "consumable",
        "skill_boost": {
            "lockpicking": 2
        },
        "description": "A detailed guide on lockpicking techniques.",
    },
    "4_leaf_clover": {
        "name": "4-Leaf Clover",
        "type": "consumable",
        "skill_boost": {
            "luck": 2
        },
        "description": "A rare four-leaf clover said to bring good luck.\n"
        "even luckier when plants dont grow in wasteland",
    },
    "strange_elixir": {
        "name": "Strange Elixir",
        "type": "consumable",
        "skill_boost": {
            "intelligence": 2
        },
        "description": "A glowing elixir that sharpens the mind.",
    },
    "bubbling_goo": {
        "name": "Bubbling Goo",
        "type": "consumable",
        "skill_boost": {
            "stamina": 2
        },
        "description": "A viscous substance that invigorates the body.",
    },
    "mutation_serum": {
        "name": "Mutation Serum",
        "type": "consumable",
        "skill_boost": {
            "stealth": 2
        },
        "description": "A serum that enhances stealth capabilities.",
    },
    "pulsing_vial": {
        "name": "Pulsing Vial",
        "type": "consumable",
        "skill_boost": {
            "carisma": 2
        },
        "description": "A vial containing a substance that enhances charisma.",
    },
#weapon________
    "magnum": {
        "name": "Magnum",
        "type": "weapon",
        "description": "A powerful handgun known for its stopping power.",
        "sell": 100,
        "buy": 300,
    },
    #ingredients for crafting______
    "alien_biomass": {
        "name": "Alien Biomass",
        "type": "crafting_material",
        "description": "Organic material harvested from alien creatures.",
        "sell": 10,
        "buy": 30,
    },
    "centipede_chitin": {
        "name": "Centipede Chitin",
        "type": "crafting_material",
        "description": "Durable exoskeleton material from genetically modified centipedes.",
        "sell": 8,
        "buy": 25,
    },
}