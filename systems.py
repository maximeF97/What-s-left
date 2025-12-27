import random 
def level_up(player):
    player["level"] += 1
    player["health"] += 5
    player["experience"] = 0
    print(f"\nYou reached level {player['level']}!")
    print("Health increased by 5.")

    while True:
        print("\nChoose a skill to upgrade:")
        skills = list(player["skills"].keys())

        for i, skill in enumerate(skills, 1):
            print(f"{i}) {skill} (level {player['skills'][skill]})")

        choice = input("> ")

        if choice.isdigit() and 1 <= int(choice) <= len(skills):
            selected_skill = skills[int(choice) - 1]
            player["skills"][selected_skill] += 1
            print(f"{selected_skill} increased to {player['skills'][selected_skill]}!")
            break
        else:
            print("Invalid choice.")



def skill_check(player, skill_name, difficulty):
    skill_value = player["skills"].get(skill_name, 0)
    roll = random.randint(1, 20)

    total = roll + skill_value + player["level"]

    print(f"Skill check ({skill_name}): roll {roll} + skill {skill_value} + level {player['level']} = {total}")

    return total >= difficulty



def gain_xp(player, amount):
    player["experience"] += amount
    print(f"You gained {amount} XP!")

    while player["experience"] >= xp_needed(player["level"]):
        level_up(player)

def xp_needed(level):
    return 20 + (level - 1) * 10

def open_inventory(player, item):
    while True:
        print("/n--- Inventory ---")

        if not player["inventory"]:
            print("Your inventory is empty.")
        else:
            for i, inv_item in enumerate(player["inventory"], 1):
                print(f"{i}) {item}")

        print("\nOptions:")
        print("1) Use item")
        print("2) Close inventory")

        choice = input("> ")

        if choice == "1":
            use_item(player)
        elif choice == "2":
            return
        else:
            print("Invalid choice.")

def use_item(player):
    if not player["inventory"]:
        print("You have nothing to use.")
        return

    print("Choose an item to use:")
    for i, item in enumerate(player["inventory"], 1):
        print(f"{i}) {item}")

    choice = input("> ")

    if not choice.isdigit():
        print("Invalid choice.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(player["inventory"]):
        print("Invalid item.")
        return

    item = player["inventory"][index]

    if item == "medkit":
        player["health"] += 5
        player["inventory"].remove(item)
        print("You used a medkit and recovered 5 health.")
        print(f"Health: {player['health']}")

    else:
        print(f"You can’t use {item} right now.")

def get_choice():
    choice = input("> ").lower()
    return choice

def handle_global_input(choice, player):
    if choice == "i":
        open_inventory(player)
        return True
    return False


              