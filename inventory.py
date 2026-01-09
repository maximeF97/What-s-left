from equipment import EQUIPMENT

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
            "i just hope he is right and we can get out of this hell"   
            "apparently it was an old secret military base before the blast"
        ),
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
        "sell": 2,
        "buy": 6,
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
    },
}