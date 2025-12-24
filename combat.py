
import random
def combats(player, enemy):

    print("\nCombat starts!")

    while player["health"] > 0 and enemy["health"] > 0:
        print(f"\nYour health: {player['health']}")
        print(f"Alien health: {enemy['health']}")

        print("1) Attack")
        print("2) Run")

        choice = input("> ")

        # PLAYER TURN
        if choice == "1":
            hit_roll = random.randint(1, 100)

            if hit_roll <= 70:  # player hit chance
                damage = random.randint(1, 3)
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

        # CHECK IF ALIEN DIED
        if enemy["health"] <= 0:
            print("The alien collapses. You survived!")
            return "win"

        # ALIEN TURN
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