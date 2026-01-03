from systems import  inspect_item, unequip_item, get_choice
from equipment import EQUIPMENT
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

        choice = get_choice().lower()

        # 🔙 Exit inventory
        if choice == "b":
            return

        # 🧤 Unequip
        if choice == "u":
            unequip_menu(player)
            continue

        if choice == "x":
            use_item(player)
            continue

        items = list(player["inventory"].keys())
        # 🔍 Inspect item
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(items):
                item = items[index]
                inspect_item(player, item)
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
            unequip_item(player, slots[index])
def add_item(player, item, amount=1):
    inventory = player["inventory"]
    inventory[item] = inventory.get(item, 0) + amount
    print(f"You received {amount} x {item.replace('_', ' ')}.")

def extra_loot(player, item, amount=1):
    inventory = player.get("inventory", {})
    scavenging = player.get("skills", {}).get("scavenging", 0)

    if scavenging >= 5:
        inventory[item] = inventory.get(item, 0) + amount
        print(
            print(
    f"scavenging Bonus!\n"
    f"You search deeper than most would dare.\n"
    f"Hidden beneath the filth, you find {amount} x "
    f"{item.replace('_', ' ')}."
)

        )


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

    choice = input("> ")

    if not choice.isdigit():
        print("Invalid choice.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(items):
        print("Invalid item.")
        return

    item = items[index]

    if item == "medkit":
        player["health"] = min(player["health"] + 5, player["max_health"])
        player["inventory"].remove(item)
        print("You used a medkit and recovered 5 health.")
        print(f"Health: {player['health']}")
    elif item == "healing salve":
        player["health"] = min(player["health"] + 3, player["max_health"])
        player["inventory"].remove(item)
        print("you use a healing salve and recover 3 health")
        print(f"Health: {player['health']}")
    elif item =="bobby_pins":
        print("A pin perfect for lockpiking")
    elif item =="alien_implant":
        print("A weird-looking implant, maybe of some use.")
    elif item == "map_to_base":
        print(
            "The map says: from the crossroad near Grovetown, go straight into the wasteland "
            "until you find an old farmhouse. "
            "The entry is hidden behind the farm at the bottom of the mountain."
        )
    elif item == "wasteland_2_note": #exemple note
        print(
            "They’re everywhere.\n"
            "I don’t know when it started.\n\n"
            "They don’t always look alien.\n"
            "Sometimes they look… familiar.\n\n"
            "If you’re reading this,\n"
            "don’t trust what you see.\n"
            "Don’t sleep."
        )
    elif item == "coin":
        print("A odly shape coin it looks like it made with scrap metal")

    
   
#______________NOTES__________________________________________________
    elif item == "wastland_field_note": #exemple of multy note
        if player["has_seen_small_metamorph"]:
            print("They’re not random. They’re sent ahead.")
        elif player["has_seen_humanoid_metamorph"]:
            print("The small ones obey the tall ones.")
        else:
            print("Something is watching the roads.")   
    elif item == "wasteland_note_small_1": # to use
        print(
    "Saw one near the ruins.\n"
    "Small. Fast. Curious.\n\n"
    "It didn’t attack.\n"
    "Just watched.\n"
    "Like an animal.\n\n"
    "Still… it learned too fast."
    
)

    elif item == "wasteland_note_small_2": # to use
        print(
    "The little ones aren’t soldiers.\n"
    "They scatter when shot.\n"
    "Unlike the big one they can breathe our air.\n\n"
    "I think they’re wildlife.\n"
    "Or pets.\n\n"
    "God help us if they grow."
    )

    elif item ==  "grovetown_note_1":
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

    elif item == "hospital_terminal_log_1": # to use
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
        print("a worn-out key, it looks old")
    
    elif item == "hospital_safe_key":
        print("a gelatinous key, it look alive")
    
    elif item == "police_station_key":
        print("a key to the police station")

    else:
        print(f"You can’t use {item} right now.")

