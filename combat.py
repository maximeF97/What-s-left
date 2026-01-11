import random
from typing import Dict, Optional, Tuple

from inventory import remove_item, use_item
from systems import skill_check, get_choice, gain_xp

WEAPONS: Dict[str, Dict] = {
    # Melee
    "rusty_knife": {"min_damage": 1, "max_damage": 3, "hit_chance": 70, "uses_ammo": False},
    "sharp_kitchen_knife": {"min_damage": 2, "max_damage": 4, "hit_chance": 75, "uses_ammo": False},

    # Ranged
    "revolver": {"min_damage": 3, "max_damage": 6, "hit_chance": 85, "uses_ammo": True, "ammo_type": "revolver_ammo"},
    "alien_laser_rifle": {"min_damage": 7, "max_damage": 12, "hit_chance": 90, "uses_ammo": True, "ammo_type": "alien_energy_cell"},
    "shotgun": {"min_damage": 6, "max_damage": 8, "hit_chance": 75, "uses_ammo": True, "ammo_type": "shotgun_shells"},
    "magnum": {"min_damage": 8, "max_damage": 12, "hit_chance": 80, "uses_ammo": True, "ammo_type": "magnum_ammo"},
    "rifle": {"min_damage": 5, "max_damage": 10, "hit_chance":90, "uses_ammo": True, "ammo_type": "rifle_ammo"},
}   


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def get_current_weapon(player: Dict) -> Tuple[Optional[str], Optional[Dict]]:
    weapon_name = player.get("weapon")
    if not weapon_name:
        return None, None
    return weapon_name, WEAPONS.get(weapon_name)


def _default_melee(player: Dict) -> None:
    """Set a deterministic melee fallback for the player."""
    if "sharp_kitchen_knife" in player.get("inventory", {}):
        player["weapon"] = "sharp_kitchen_knife"
    else:
        player["weapon"] = "rusty_knife"


def choose_weapon(player: Dict) -> None:
    """
    Let player pick melee or a firearm they have. Defaults to a melee knife.
    Sets player["weapon"] accordingly.
    """
    inventory = player.get("inventory", {})
    _default_melee(player)

    firearms = [gun for gun in ("revolver", "shotgun", "alien_laser_rifle") if gun in inventory]

    if not firearms:
        print("You ready your melee weapon.")
        return

    print("Choose your weapon:")
    print("1) Melee")
    for i, gun in enumerate(firearms, start=2):
        print(f"{i}) {gun.replace('_', ' ').title()}")

    choice = get_choice()
    if choice.isdigit():
        index = int(choice)
        if index == 1:
            _default_melee(player)
        else:
            idx = index - 2
            if 0 <= idx < len(firearms):
                player["weapon"] = firearms[idx]
            else:
                # Invalid selection -> keep default melee
                _default_melee(player)
    else:
        # Non-numeric -> keep default melee
        _default_melee(player)


def player_attack(player: Dict, enemy: Dict) -> bool:
    """
    Perform one player attack using current weapon.
    Returns True if an attack action occurred (hit or miss), False if unarmed.
    """
    weapon_name, weapon = get_current_weapon(player)
    if not weapon:
        print("You are unarmed!")
        return False

    inventory = player.get("inventory", {})
    # Ranged ammo handling
    if weapon["uses_ammo"]:
        ammo_key = weapon["ammo_type"]
        if inventory.get(ammo_key, 0) <= 0:
            print("Click! You're out of ammo.")
            _default_melee(player)
            weapon_name, weapon = get_current_weapon(player)
        else:
            # Attempt to consume one ammo; if it fails, fallback to melee
            if not remove_item(player, ammo_key, 1):
                print("Click! You're out of ammo.")
                _default_melee(player)
                weapon_name, weapon = get_current_weapon(player)

    # Luck can slightly improve hit chance
    luck = player.get("skills", {}).get("luck", 0)
    chance_to_hit = _clamp(weapon["hit_chance"] + luck * 3, 5, 95)

    roll = random.randint(1, 100)
    if roll > chance_to_hit:
        print("You miss!")
        return True

    # Damage resolution
    dmg = random.randint(weapon["min_damage"], weapon["max_damage"])
    enemy["health"] = max(0, enemy["health"] - dmg)
    print(f"You hit with your {weapon_name.replace('_', ' ')} for {dmg} damage!")
    return True

def heal_player(player, amount):
    before = player["health"]
    player["health"] = min(player["health"] + amount, player["max_health"])
    healed = player["health"] - before
    if healed > 0:
        print(f"You recover {healed} health.")
    else:
        print("You are already at full health.")

def apply_stamina_damage_reduction(player, damage):
    """Reduce incoming damage based on stamina (capped at 50%), plus flat equipment damage_reduction."""
    stamina = player.get("skills", {}).get("stamina", 0)
    reduction_pct = min(stamina * 0.01, 0.5)
    flat = int(player.get("equipment_bonuses", {}).get("damage_reduction", 0))
    reduced = int(damage * (1 - reduction_pct)) - flat
    return max(1, reduced)


def take_damage(player: Dict, amount: int) -> None:
    final = apply_stamina_damage_reduction(player, amount)

    # Equipment-based damage reduction
    dr_pct = player.get("equipment_bonuses", {}).get("damage_reduction_pct", 0)
    if dr_pct:
        final = int(final * (1 - dr_pct / 100))

    final = max(0, final)
    player["health"] = max(0, player["health"] - final)

    print(f"You take {final} damage.")


def enemy_attack(player: Dict, enemy: Dict) -> None:
    """Enemy attacks the player once."""
    enemy_hit = random.randint(1, 100) <= enemy.get("hit_chance", 60)
    if enemy_hit:
        base_damage = random.randint(1, 4)
        final = apply_stamina_damage_reduction(player, base_damage)
        player["health"] = max(0, player["health"] - final)
        print(f"The enemy hits you for {final} damage.")
    else:
        print("The enemy misses.")


def _attempt_run(player: Dict) -> bool:
    """Return True if the player successfully runs away."""
    try:
        # Slightly easier checks for running away
        return skill_check(player, "stamina", difficulty=40) or skill_check(player, "luck", difficulty=35)
    except Exception:
        # Fallback: use raw stat values with a small random factor
        stam = player.get("skills", {}).get("stamina", 1)
        luck = player.get("skills", {}).get("luck", 1)
        return (stam + luck + random.randint(0, 3)) >= 5


def _ensure_defaults(player: Dict, enemy: Dict) -> None:
    """Ensure required fields exist on player and enemy."""
    player.setdefault("inventory", {})
    player.setdefault("skills", {})
    player.setdefault("health", 10)
    player.setdefault("max_health", player["health"])

    enemy.setdefault("health", 5)
    enemy.setdefault("hit_chance", 60)
    enemy.setdefault("xp", 0)


def combats(player: Dict, enemy: Dict) -> Dict[str, int | str]:
    """
    Turn-based combat loop.
    Returns a dict: {"result": "win"|"lose"|"run", "xp": int}
    Note: XP is only included in the return; awarding should happen at the call site.
    """
    _ensure_defaults(player, enemy)

    print("\n--- Combat Begins ---")
    choose_weapon(player)

    while True:
        print(f"\nYour Health: {player['health']}/{player['max_health']} | Enemy Health: {enemy['health']}")
        print("Choose an action:")
        print("1) Attack")
        print("2) Use item")
        print("3) Run")

        choice = get_choice().strip()

        # Player turn
        if choice == "1":
            acted = player_attack(player, enemy)
            if acted and enemy["health"] <= 0:
                print("You defeated the enemy!")
                return {"result": "win", "xp": int(enemy.get("xp", 0))}

        elif choice == "2":
            # Use an item (e.g., heal, buff, etc.)
            try:
                use_item(player)
            except Exception as e:
                print(f"Item use failed: {e}")

        elif choice == "3":
            if _attempt_run(player):
                print("You managed to escape!")
                return {"result": "run", "xp": 0}
            else:
                print("You try to run, but the enemy cuts you off!")

        else:
            print("Invalid choice.")
            continue  # re-prompt without giving enemy a free attack

        # Enemy turn (if enemy still alive)
        if enemy["health"] > 0:
            enemy_attack(player, enemy)
            if player["health"] <= 0:
                print("You have been defeated.")
                return {"result": "lose", "xp": 0}