import random

WEAPONS = {
    "knife": {
        "min_damage": 1,
        "max_damage": 3,
        "hit_chance": 70,
        "uses_ammo": False
    },
    "revolver": {
        "min_damage": 2,
        "max_damage": 6,
        "hit_chance": 85,
        "uses_ammo": True,
        "ammo_type": "revolver_ammo"
    }
}

def combats(player, enemy):
    print("\nCombat starts!")

    # Weapon selection (once)
    if "revolver" in player["inventory"]:
        print("Choose your weapon:")
        print("1) Rusty knife")
        print("2) Revolver")

        choice = input("> ")
        if choice == "2":
            player["weapon"] = "revolver"
        else:
            player["weapon"] = "knife"
    else:
        player["weapon"] = "knife"

    while player["health"] > 0 and enemy["health"] > 0:
        print(f"\nYour health: {player['health']}")
        print(f"Alien health: {enemy['health']}")
        print(f"Weapon: {player['weapon']}")

        print("1) Attack")
        print("2) Run")

        choice = input("> ")

        if choice == "1":
            weapon = WEAPONS[player["weapon"]]

            # Ammo check
            if weapon["uses_ammo"]:
                ammo = weapon["ammo_type"]
                if ammo not in player["inventory"]:
                    print("Click! You have no revolver ammo.")
                    print("You switch back to your knife.")
                    player["weapon"] = "knife"
                    weapon = WEAPONS["knife"]
                else:
                    player["inventory"].remove(ammo)
                    print("You fire the revolver!")

            hit_roll = random.randint(1, 100)
            if hit_roll <= weapon["hit_chance"]:
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

        # Enemy defeated
        if enemy["health"] <= 0:
            print("The alien collapses. You survived!")
            return "win"

        # Alien turn
        alien_hit = random.randint(1, 100)
        if alien_hit <= enemy["hit_chance"]:
            damage = random.randint(1, 2)
            player["health"] -= damage
            print(f"The alien hits you for {damage} damage!")
        else:
            print("The alien misses!")

    if player["health"] <= 0:
        print("You have been killed...")
        return "lose"
