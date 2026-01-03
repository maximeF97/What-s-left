import random
from typing import Dict
from save_system import save_game, load_game
from equipment import EQUIPMENT
from inventory import open_inventory, add_item, remove_item

# -----------------------------
# Player progression and stats
# -----------------------------

def xp_needed(level: int) -> int:
    return 20 + (level - 1) * 10


def level_up(player: Dict) -> None:
    player["level"] += 1
    player["experience"] = 0
    # Recompute max health immediately from stamina bonus
    apply_stamina_health_bonus(player)
    # Restore health and save
    player["health"] = player["max_health"]
    save_game(player)
    print("You feel refreshed. Health fully restored!")
    print("the game as been saved")
    print(f"\nYou reached level {player['level']}!")

    while True:
        print("\nChoose a skill to upgrade:")
        skills = list(player["skills"].keys())

        for i, skill in enumerate(skills, 1):
            print(f"{i}) {skill} (level {player['skills'][skill]})")

        choice = input("> ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(skills):
            selected_skill = skills[int(choice) - 1]
            player["skills"][selected_skill] += 1
            print(f"{selected_skill} increased to {player['skills'][selected_skill]}!")

            if selected_skill == "stamina":
                apply_stamina_health_bonus(player)
            break
        else:
            print("Invalid choice.")

def get_effective_skill(player: Dict, skill_name: str) -> int:
    base = player.get("skills", {}).get(skill_name, 0)
    bonus = player.get("equipment_bonuses", {}).get(skill_name, 0)
    return base + bonus

def skill_check(player: Dict, skill_name: str, difficulty: int) -> bool:
    skill_value = get_effective_skill(player, skill_name)
    roll = random.randint(1, 20)
    level = player.get("level", 1)
    total = roll + skill_value + level
    print(f"Skill check ({skill_name}): roll {roll} + skill {skill_value} + level {level} = {total} vs DC {difficulty}")
    return total >= difficulty


def gain_xp(player: Dict, amount: int) -> None:
    # Intelligence is usually tracked in player['skills']
    intelligence = player.get("skills", {}).get("intelligence", 0)
    bonus_multiplier = 1 + (intelligence * 0.05)  # 5% per INT
    gained_xp = int(amount * bonus_multiplier)
    player["experience"] += gained_xp
    print(f"You gained {gained_xp} XP!")

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
    Aggregate bonuses from all equipped items into player['equipment_bonuses'].
    """
    ensure_equipment_struct(player)
    bonuses: Dict[str, int] = {}
    for slot, item in player["equipment"].items():
        if not item:
            continue
        info = EQUIPMENT.get(item)
        if not info:
            continue
        for key, val in info.get("bonuses", {}).items():
            bonuses[key] = bonuses.get(key, 0) + int(val)
    player["equipment_bonuses"] = bonuses


def equip_item(player: Dict, item: str) -> bool:
    """
    Equip an item if it is equippable and present in the inventory.
    Returns True on success.
    """
    ensure_equipment_struct(player)

    info = EQUIPMENT.get(item)
    if not info:
        print(f"{item.replace('_', ' ').title()} cannot be equipped.")
        return False

    # Check possession (inventory must be a dict of item -> quantity)
    qty = player.get("inventory", {}).get(item, 0)
    if qty <= 0:
        print(f"You don't have {item.replace('_', ' ')}.")
        return False

    slot = info["slot"]
    current = player["equipment"].get(slot)
    player["equipment"][slot] = item

    _aggregate_equipment_bonuses(player)

    if current and current != item:
        print(f"Equipped {item.replace('_', ' ')} in {slot} (replacing {current.replace('_', ' ')}).")
    else:
        print(f"Equipped {item.replace('_', ' ')} in {slot}.")

    # Preview bonuses
    bonuses = player.get("equipment_bonuses", {})
    if bonuses:
        preview = ", ".join(f"{k.replace('_', ' ')} +{v}" for k, v in bonuses.items())
        print(f"Active equipment bonuses: {preview}")
    return True


def unequip_item(player: Dict, slot: str) -> bool:
    """
    Unequip whatever is in the given slot: 'head', 'body', 'hand', or 'feet'.
    """
    ensure_equipment_struct(player)
    if slot not in player["equipment"]:
        print(f"Unknown equipment slot: {slot}")
        return False

    current = player["equipment"].get(slot)
    if not current:
        print(f"No item equipped in {slot}.")
        return False

    player["equipment"][slot] = None
    _aggregate_equipment_bonuses(player)
    print(f"Unequipped {current.replace('_', ' ')} from {slot}.")
    return True


def inspect_item(player: Dict, item: str) -> None:
    """
    Inspect an item and offer to equip it if equippable.
    """
    info = EQUIPMENT.get(item)
    if info:
        desc = info.get("description", "No description.")
        print(f"\n{item.replace('_', ' ').title()} — {info['slot'].title()}")
        print(desc)
        print("\nOptions:")
        print("E) Equip")
        print("B) Back")
        choice = input("> ").strip().lower()
        if choice == "e":
            equip_item(player, item)
        return
    else:
        print(f"\n{item.replace('_', ' ').title()}: This item cannot be equipped.")
        print("B) Back")
        input("> ")


# -----------------------------
# Input helpers and global hotkeys
# -----------------------------

def get_choice() -> str:
    return input("> ").strip().lower()


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
        print("You search carefully, but find nothing more.")
        return

    # Pick random item from table
    item = random.choice(list(loot_table.keys()))
    min_amt, max_amt = loot_table[item]
    amount = random.randint(min_amt, max_amt)

    if amount <= 0:
        print("You almost miss something… but it turns out to be useless debris.")
        return

    add_item(player, item, amount)
    print(
        f"You dig deeper into the wreckage.\n"
        f"Your instincts pay off.\n"
        f"You find {amount} x {item.replace('_', ' ')}."
    )