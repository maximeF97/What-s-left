import random
from typing import Dict

from save_system import save_game, load_game
from equipment import EQUIPMENT
from ui import ui_print, ui_input, ui_update_equipment

# -----------------------------
# Player progression and stats
# -----------------------------

def xp_needed(level: int) -> int:
    return 20 + (level - 1) * 10


def level_up(player: Dict) -> None:
    player["level"] += 1
    player["experience"] = 0
    apply_stamina_health_bonus(player)
    player["health"] = player["max_health"]
    save_game(player)
    ui_print("You feel refreshed. Health fully restored!")
    ui_print("the game as been saved")
    ui_print(f"\nYou reached level {player['level']}!")

    while True:
        ui_print("\nChoose a skill to upgrade:")
        skills = list(player["skills"].keys())

        for i, skill in enumerate(skills, 1):
            ui_print(f"{i}) {skill} (level {player['skills'][skill]})")

        choice = ui_input("> ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(skills):
            selected_skill = skills[int(choice) - 1]
            player["skills"][selected_skill] += 1
            ui_print(f"{selected_skill} increased to {player['skills'][selected_skill]}!")

            if selected_skill == "stamina":
                apply_stamina_health_bonus(player)
            ui_update_equipment(player)  # ← Add this line
            break
        else:
            ui_print("Invalid choice.")
def get_effective_skill(player: Dict, skill_name: str) -> int:
    base = player.get("skills", {}).get(skill_name, 0)

    equipment_bonus = player.get("equipment_bonuses", {}).get(skill_name, 0)
    temp_bonus = player.get("temporary_skill_boosts", {}).get(skill_name, 0)

    return base + equipment_bonus + temp_bonus


def skill_check(
    player: Dict,
    skill_name: str,
    difficulty: int,
    visible: bool = True
) -> bool:
    skill = get_effective_skill(player, skill_name)
    skill_value = skill * 2
    roll = random.randint(1, 20)
    level = player.get("level", 1)

    total = roll + skill_value + level

    if visible:
        ui_print(
            f"Skill check ({skill_name}): "
            f"roll {roll} + skill {skill_value} + level {level} "
            f"= {total} vs DC {difficulty}"
        )
    return total >= difficulty


def gain_xp(player: Dict, amount: int) -> None:
    intelligence = player.get("skills", {}).get("intelligence", 0)
    bonus_multiplier = 1 + (intelligence * 0.05)
    gained_xp = int(amount * bonus_multiplier)
    player["experience"] += gained_xp
    ui_print(f"You gained {gained_xp} XP!")
    ui_update_equipment(player)  # ← Add this line

    while player["experience"] >= xp_needed(player["level"]):
        level_up(player)


def apply_stamina_health_bonus(player: Dict) -> None:
    # Ensure base_health exists; default to current max_health to avoid KeyError
    base = player.get("base_health", player.get("max_health", 10))
    player["base_health"] = base
    stamina = player.get("skills", {}).get("stamina", 0)
    bonus_multiplier = 1 + (stamina * 0.05)
    player["max_health"] = int(base * bonus_multiplier)
    if player.get("health", 0) > player["max_health"]:
        player["health"] = player["max_health"]

def apply_max_health_bonus(player: Dict) -> None:
    bonus = player.get("equipment_bonuses", {}).get("max_health", 0)
    base_max = player.get("base_max_health", player["max_health"])

    player["max_health"] = base_max + bonus
    player["health"] = min(player["health"], player["max_health"])

def apply_health_restore_bonus(player: Dict) -> None:
    pass#todo

def apply_bonuses(player: Dict, bonuses: Dict[str, int]) -> None:
    for stat, value in bonuses.items():
        player["skills"][stat] = player["skills"].get(stat, 0) + int(value)


def remove_bonuses(player: Dict, bonuses: Dict[str, int]) -> None:
    for stat, value in bonuses.items():
        player["skills"][stat] = max(0, player["skills"].get(stat, 0) - int(value))


# -----------------------------
# Equipment helpers
# -----------------------------

def ensure_equipment_struct(player: Dict) -> None:
    """
    Ensure the player has equipment slots and aggregated bonuses container.
    """
    player.setdefault("equipment", {"head": None, "body": None, "hand": None, "feet": None})
    player.setdefault("equipment_bonuses", {})


def _aggregate_equipment_bonuses(player: Dict) -> None:
    """
    Aggregate bonuses and flags from all equipped items.
    """
    ensure_equipment_struct(player)

    bonuses: Dict[str, int] = {}
    flags: Dict[str, bool] = {}

    for slot, item_id in player["equipment"].items():
        if not item_id:
            continue

        info = EQUIPMENT.get(item_id)
        if not info:
            continue

        # Stat bonuses
        for key, val in info.get("bonuses", {}).items():
            bonuses[key] = bonuses.get(key, 0) + int(val)

        # Flags (boolean effects)
        for flag, value in info.get("flags", {}).items():
            flags[flag] = bool(value)

    # Replace aggregated data
    player["equipment_bonuses"] = bonuses

    # Clear previous equipment flags
    for flag in list(player.keys()):
        if flag.startswith("equip_"):
            del player[flag]

    # Apply new flags (namespaced = safer)
    for flag, value in flags.items():
        player[f"equip_{flag}"] = value

def equip_item(player: Dict, item: str) -> bool:
    ensure_equipment_struct(player)

    info = EQUIPMENT.get(item)
    if not info:
        ui_print(f"{item.replace('_', ' ').title()} cannot be equipped.")
        return False

    if player.get("inventory", {}).get(item, 0) <= 0:
        ui_print(f"You don't have {item.replace('_', ' ')}.")
        return False

    slot = info.get("slot")
    if not slot:
        ui_print(f"{item.replace('_', ' ').title()} has no slot defined.")
        return False

    # Determine which slots this item will occupy
    slots_to_occupy = [slot]
    
    if info.get("flags", {}).get("occupies_hands"):
        if "hand" not in slots_to_occupy:
            slots_to_occupy.append("hand")
    
    if info.get("flags", {}).get("occupies_feet"):
        if "feet" not in slots_to_occupy:
            slots_to_occupy.append("feet")

    # Unequip any existing items in those slots
    for occupied_slot in slots_to_occupy:
        current_item = player["equipment"].get(occupied_slot)
        if current_item and current_item != item:
            ui_print(f"Unequipping {current_item.replace('_', ' ')} from {occupied_slot}.")
            # Clear ALL slots that old item occupied
            for s, equipped in list(player["equipment"].items()):
                if equipped == current_item:
                    player["equipment"][s] = None

    # Equip the new item in all required slots
    for occupied_slot in slots_to_occupy:
        player["equipment"][occupied_slot] = item

    _aggregate_equipment_bonuses(player)

    # Build friendly message
    if len(slots_to_occupy) == 1:
        ui_print(f"Equipped {item.replace('_', ' ')} ({slot}).")
    else:
        slot_names = ", ".join(slots_to_occupy)
        ui_print(f"Equipped {item.replace('_', ' ')} ({slot_names}).")
    
    ui_update_equipment(player)  # ← Add this line
    return True


def unequip_item(player: Dict, slot: str) -> bool:
    ensure_equipment_struct(player)

    if slot not in player["equipment"]:
        ui_print(f"Unknown equipment slot: {slot}")
        return False

    item = player["equipment"].get(slot)
    if not item:
        ui_print(f"No item equipped in {slot}.")
        return False

    # Remove item from ALL slots it occupies
    for s, equipped in player["equipment"].items():
        if equipped == item:
            player["equipment"][s] = None

    _aggregate_equipment_bonuses(player)
    ui_print(f"Unequipped {item.replace('_', ' ')}.")
    ui_update_equipment(player)  # ← Add this line
    return True

def inspect_item(player: Dict, item: str) -> None:
    info = EQUIPMENT.get(item)
    if info:
        desc = info.get("description", "No description.")
        ui_print(f"\n{item.replace('_', ' ').title()} — {info['slot'].title()}")
        ui_print(desc)
        ui_print("\nOptions:")
        ui_print("E) Equip")
        ui_print("B) Back")
        choice = ui_input("> ").strip().lower()
        if choice == "e":
            equip_item(player, item)
        return
    else:
        ui_print(f"\n{item.replace('_', ' ').title()}: This item cannot be equipped.")
        ui_print("B) Back")
        ui_input("> ")


# -----------------------------
# Input helpers and global hotkeys
# -----------------------------

def get_choice() -> str:
    return ui_input("> ").strip().lower()

def get_perception(player):
    base = player.get("perception", 0)
    bonus = player.get("status_effects", {}).get("perception_bonus", 0)
    return base + bonus
def should_alien_attack(player, enemy):
    if enemy.get("type") == "alien":
        if player.get("status_effects", {}).get("alien_marked"):
            ui_print("The alien tilts its head… then backs away.")
            return False
    return True
from inventory import open_inventory, add_item, remove_item
def handle_global_input(choice: str, player: Dict) -> bool:
    if choice == "i":
        # Ensure equipment exists before opening inventory
        ensure_equipment_struct(player)
        open_inventory(player)
        return True

    if choice.lower() == "s":
        save_game(player)
        return True

    if choice.lower() == "l":
        loaded_player = load_game()
        if loaded_player:
            player.clear()
            player.update(loaded_player)
        return True

    return False


# -----------------------------
# Loot
# -----------------------------

def randomized_bonus_loot(player: Dict, loot_table: Dict[str, tuple]) -> None:
    """
    loot_table example:
    {
        "coin": (1, 3),
        "revolver_ammo": (1, 2),
        "alien_implant": (0, 1)
    }
    """
    scavenging = player.get("skills", {}).get("scavenging", 0)

    # Base chance + skill scaling
    base_chance = 20            # 20%
    bonus_per_level = 6         # +6% per scavenging level
    chance = base_chance + scavenging * bonus_per_level

    roll = random.randint(1, 100)
    if roll > chance:
        ui_print("You search carefully, but find nothing more.")
        return

    # Pick random item from table
    item = random.choice(list(loot_table.keys()))
    min_amt, max_amt = loot_table[item]
    amount = random.randint(min_amt, max_amt)

    if amount <= 0:
        ui_print("You almost miss something… but it turns out to be useless debris.")
        return

    add_item(player, item, amount)
    ui_print(
        f"You dig deeper into the wreckage.\n"
        f"Your instincts pay off.\n"
        f"You find {amount} x {item.replace('_', ' ')}."
    )