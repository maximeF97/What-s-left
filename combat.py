import random

WEAPONS = {
    "rusty_knife": {
        "min_damage": 1,
        "max_damage": 3,
        "hit_chance": 70,
        "uses_ammo": False
    },
    "sharp_kitchen_knife": {
        "min_damage": 2,
        "max_damage": 4,
        "hit_chance": 75,
        "uses_ammo": False
    },
    "revolver": {
        "min_damage": 2,
        "max_damage": 6,
        "hit_chance": 85,
        "uses_ammo": True,
        "ammo_type": "revolver_ammo"
    },
    "alien_laser_rifle": {
        "min_damage": 5,
        "max_damage": 10,
        "hit_chance": 90,
        "uses_ammo": True,
        "ammo_type": "alien_energy_cell"
    },
    "shotgun": {
        "min_damage": 4,
        "max_damage": 8,
        "hit_chance": 75,
        "uses_ammo": True,
        "ammo_type": "shotgun_shells"
    }
}

# -------------------------
# STAMINA DAMAGE REDUCTION
# -------------------------
def apply_stamina_damage_reduction(player, damage):
    stamina = player["skills"].get("stamina", 0)
    reduction = min(stamina * 0.01, 0.5)  # cap at 50%
    reduced_damage = int(damage * (1 - reduction))
    return max(1, reduced_damage)

# -------------------------
# WEAPON SELECTION
# -------------------------
def choose_weapon(player):
    # Default melee
    if "sharp_kitchen_knife" in player["inventory"]:
        player["weapon"] = "sharp_kitchen_knife"
    else:
        player["weapon"] = "rusty_knife"

    firearms = []
    for gun in ("revolver", "shotgun", "alien_laser_rifle"):
        if gun in player["inventory"]:
            firearms.append(gun)

    if firearms:
        print("Choose your weapon:")
        print("1) Melee")
        for i, gun in enumerate(firearms, 2):
            print(f"{i}) {gun.replace('_', ' ').title()}")

        choice = input("> ")
        if choice.isdigit():
            index = int(choice) - 2
            if 0 <= index < len(firearms):
                player["weapon"] = firearms[index]

# -------------------------
# COMBAT
# -------------------------
def combats(player, enemy):
    print("\nCombat starts!")
    choose_weapon(player)

    while player["health"] > 0 and enemy["health"] > 0:
        print(f"\nYour health: {player['health']}")
        print(f"Alien health: {enemy['health']}")
        print(f"Weapon: {player['weapon']}")

        print("1) Attack")
        print("2) Run")
        choice = input("> ")

        if choice == "1":
            weapon = WEAPONS[player["weapon"]]

            if weapon["uses_ammo"]:
                ammo = weapon["ammo_type"]
                if ammo not in player["inventory"]:
                    print("Click! You're out of ammo.")
                    print("You switch back to your melee weapon.")
                    choose_weapon(player)
                    continue
                else:
                    player["inventory"].remove(ammo)

            if random.randint(1, 100) <= weapon["hit_chance"]:
                damage = random.randint(
                    weapon["min_damage"],
                    weapon["max_damage"]
                )
                enemy["health"] -= damage
                print(f"You hit the alien for {damage} damage!")
            else:
                print("You miss!")

        elif choice == "2":
            print("You run away!")
            player["health"] -= 1
            print("You trip and lose 1 health.")
            return "run"

        else:
            print("Invalid choice.")
            continue

        if enemy["health"] <= 0:
            print("The alien collapses. You survived!")
            return {"result": "win", "xp": enemy.get("xp", 0)}

        # Alien turn
        if random.randint(1, 100) <= enemy["hit_chance"]:
            base_damage = random.randint(1, 2)
            damage = apply_stamina_damage_reduction(player, base_damage)
            player["health"] -= damage
            print(f"The alien hits you for {damage} damage!")
        else:
            print("The alien misses!")

    print("You have been killed...")
    return "lose"
