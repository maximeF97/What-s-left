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
        print(
            f"Skill check ({skill_name}): "
            f"roll {roll} + skill {skill_value} + level {level} "
            f"= {total} vs DC {difficulty}"
        )

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

def apply_max_health_bonus(player: Dict) -> None:
    bonus = player.get("equipment_bonuses", {}).get("max_health", 0)
    base_max = player.get("base_max_health", player["max_health"])

    player["max_health"] = base_max + bonus
    player["health"] = min(player["health"], player["max_health"])


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
        print(f"{item.replace('_', ' ').title()} cannot be equipped.")
        return False

    if player.get("inventory", {}).get(item, 0) <= 0:
        print(f"You don't have {item.replace('_', ' ')}.")
        return False

    slot = info["slot"]

    # Equip primary slot
    player["equipment"][slot] = item

    # Handle multi-slot occupation
    if info.get("flags", {}).get("occupies_hands"):
        player["equipment"]["hand"] = item
    if info.get("flags", {}).get("occupies_feet"):
        player["equipment"]["feet"] = item

    _aggregate_equipment_bonuses(player)

    print(f"Equipped {item.replace('_', ' ')} (body, hands, feet).")
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
from combat import take_damage,heal_player
def eat_item(player, item_id):
    if not remove_item(player, item_id, 1):
        print("You don't have that item.")
        return

    if item_id == "weird_fruit":
        handle_weird_fruit(player)
    elif item_id == "medkit":
        heal_player(player, 20)
    # other food items here
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
    if count == 10:
        print("Something inside you stirs… and the world feels quieter.")
        print("Alien creatures hesitate when they look at you.")
        player["status_effects"]["alien_marked"] = True
        player["can_breathe_in_alien_environments"] = True
        player["has_eaten_10_fruits"] = True
    # ☠️ Too many fruits → body rejection
    if count >= 12 and random.random() < 0.1:
        print("Pain erupts inside you."
              "tentacles erupt from your skin, writhing wildly before retracting back.")
        take_damage(player, 25)

def get_perception(player):
    base = player.get("perception", 0)
    bonus = player.get("status_effects", {}).get("perception_bonus", 0)
    return base + bonus
def should_alien_attack(player, enemy):
    if enemy.get("type") == "alien":
        if player.get("status_effects", {}).get("alien_marked"):
            print("The alien tilts its head… then backs away.")
            return False
    return True

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