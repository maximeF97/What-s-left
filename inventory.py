from equipment import EQUIPMENT

# Provide local get_choice so inventory does not import systems at import-time.
def get_choice():
    return input("> ").lower()

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
        print("  [number] Inspect / Equip item")
        print("  U) Unequip item")
        print("  X) Use item")
        print("  B) Back")

        choice = get_choice().lower()

        if choice == "b":
            return

        if choice == "u":
            unequip_menu(player)
            continue

        if choice == "x":
            use_item(player)
            continue

        items = list(player["inventory"].keys())
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(items):
                item = items[index]
                # Lazy import to avoid circular dependency
                try:
                    from systems import inspect_item
                    inspect_item(player, item)
                except ImportError:
                    print("Unable to inspect item right now (module not fully loaded).")
            else:
                print("Invalid item.")

def unequip_menu(player):
    print("\nUNEQUIP WHICH SLOT?")
    slots = list(player["equipment"].keys())

    for i, slot in enumerate(slots, 1):
        current = player["equipment"][slot]
        name = current.replace("_", " ") if current else "(empty)"
        print(f"{i}) {slot.capitalize()} — {name}")

    print("B) Back")

    choice = get_choice().lower()

    if choice == "b":
        return

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(slots):
            # Lazy import to avoid circular dependency
            try:
                from systems import unequip_item
                unequip_item(player, slots[index])
            except ImportError:
                print("Unable to unequip right now (module not fully loaded).")

def add_item(player, item, amount=1):
    inventory = player["inventory"]
    inventory[item] = inventory.get(item, 0) + amount
    print(f"Added {amount} x {item.replace('_', ' ')}")

def remove_item(player, item, amount=1):
    inventory = player["inventory"]
    if inventory.get(item, 0) < amount:
        return False
    inventory[item] -= amount
    if inventory[item] <= 0:
        del inventory[item]
    return True

def has_item(player, item, amount=1):
    return player["inventory"].get(item, 0) >= amount

def use_item(player):
    if not player["inventory"]:
        print("You have nothing to use.")
        return

    items = list(player["inventory"].keys())

    print("Choose an item to use:")
    for i, item in enumerate(items, 1):
        print(f"{i}) {item.replace('_', ' ')} x{player['inventory'][item]}")

    choice = input("> ").strip().lower()

    if not choice.isdigit():
        print("Invalid choice.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(items):
        print("Invalid item.")
        return

    item = items[index]
    # Health items
    if item == "medkit":
        player["health"] = min(player["health"] + 5, player["max_health"])
        remove_item(player, item, 1)
        print("You used a medkit and recovered 5 health.")
        print(f"Health: {player['health']}")
    elif item == "healing_salve":
        player["health"] = min(player["health"] + 3, player["max_health"])
        remove_item(player, item, 1)
        print("You use a healing salve and recover 3 health")
        print(f"Health: {player['health']}")
    elif item == "canned_food":
        player["health"] = min(player["health"] + 2, player["max_health"])
        remove_item(player, item, 1)
        print("You eat the canned food and recover 2 health")
        print(f"Health: {player['health']}")
    elif item == "weird_fruit":
        player["health"] = min(player["health"] + 4, player["max_health"])
        player["max_health"] += 1
        remove_item(player, item, 1)
        print("You eat the weird fruit. You recover 4 health and your max health increases by 1.")
        print(f"Health: {player['health']}")
#______________ITEMS DESCRIPTION____________________________________
    elif item == "bobby_pins":
        print("A pin perfect for lockpicking")
    elif item == "alien_implant":
        print("A weird-looking implant, maybe of some use.")
    elif item == "map_to_base":
        print(
            "The map says: from the crossroad near Grovetown, go straight into the wasteland "
            "until you find an old farmhouse. "
            "The entry is hidden behind the farm at the bottom of the mountain."
        )

    elif item == "coin":
        print("An oddly shaped coin, looks like it's made with scrap metal")
#____________AMMO__________________
    elif item == "revolver_ammo":
        print("Ammunition for a revolver")
    elif item == "rifle_ammo":
        print("Ammunition for a rifle")
    elif item == "shotgun_shells":
        print("Ammunition for a shotgun")
    elif item == "alien_energy_cell":
        print("A strange energy cell, it hums with power.")

#______________NOTES__________________________________________________
    elif item == "wastland_field_note":
        if player.get("has_seen_small_metamorph"):
            print("They’re not random. They’re sent ahead.")
        elif player.get("has_seen_humanoid_metamorph"):
            print("The small ones obey the tall ones.")
        else:
            print("Something is watching the roads.")
    elif item == "wasteland_note_small_1":
        print(
            "Saw one near the ruins.\n"
            "Small. Fast. Curious.\n\n"
            "It didn’t attack.\n"
            "Just watched.\n"
            "Like an animal.\n\n"
        )
    elif item == "wasteland_2_note":
        print(
            "They’re everywhere.\n"
            "I don’t know when it started.\n\n"
            "They don’t always look alien.\n"
            "Sometimes they look… familiar.\n\n"
            "If you’re reading this,\n"
            "don’t trust what you see.\n"
            "Don’t sleep."
        )
    elif item == "wasteland_note_small_2":
        print(
            "The little ones aren’t soldiers.\n"
            "They scatter when shot.\n"
            "Unlike the big one they can breathe our air.\n\n"
            "I think they’re wildlife.\n"
            "Or pets.\n\n"
            "God help us if they grow."
        )
    elif item == "farmer_note":
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
    elif item == "grovetown_note_1":
        print(
            "There are two kinds.\n"
            "I’m sure of it now.\n\n"
            "The small ones mimic shapes.\n"
            "Animals. Objects. Trash.\n\n"
            "The tall ones mimic *us*."
        )
    elif item == "grovetown_note_2":
        print(
            "The humanoids don’t hunt like animals.\n"
            "They set traps.\n"
            "They wait.\n\n"
            "One of them watched me eat.\n"
            "Like it was studying how."
        )
    elif item == "hospital_terminal_log_1":
        print(
            "Atmospheric mismatch confirmed.\n"
            "Humanoid entities show respiratory distress\n"
            "in unaltered Earth air.\n\n"
            "They avoid long exposure.\n"
            "They *need* the terraformed zones."
        )
    elif item == "hospital_note_doctor":
        print(
            "They’re intelligent.\n"
            "More than we thought.\n\n"
            "But they choke here.\n"
            "That’s why they send the small ones first.\n\n"
            "Scouts.\n"
            "Pets.\n"
            "Weapons."
        )
    #_________KEYS_________
    elif item == "old_key":
        print("A worn-out key, it looks old")
    elif item == "hospital_safe_key":
        print("A gelatinous key, it looks alive")
    elif item == "second_hospital_safe_key":
        print("A pulsing metallic key with strange engravings")
    elif item == "third_hospital_safe_key":
        print("A leaking key that seems to pulse faintly")
    elif item == "police_station_key":
        print("A key to the police station")
    elif item == "old_farm_house_leaving_room_key":
        print("A rusty key for the living room door of the old farmhouse")
    else:
        print(f"You can’t use {item} right now.")