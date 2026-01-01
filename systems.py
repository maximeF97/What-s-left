import random 
from save_system import save_game, load_game
def level_up(player):
    player["level"] += 1
    player["experience"] = 0
    save_game(player)
    print("the game as been saved")
    print(f"\nYou reached level {player['level']}!")
    
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

            # 👇 Apply stamina effects immediately
            if selected_skill == "stamina":
                apply_stamina_health_bonus(player)
                player["health"] = player["max_health"]
                print("You feel refreshed. Health fully restored!")

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
    intelligence = player.get("intelligence", 0)
    bonus_multiplier = 1 + (intelligence * 0.05)  # 5% per INT

    gained_xp = int(amount * bonus_multiplier)
    player["experience"] += gained_xp

    print(f"You gained {gained_xp} XP!")

    while player["experience"] >= xp_needed(player["level"]):
        level_up(player)


def xp_needed(level):
    return 20 + (level - 1) * 10

def open_inventory(player):
    while True:
        print("\n--- Inventory ---")

        if not player["inventory"]:
            print("Your inventory is empty.")
        else:
            for i, inv_item in enumerate(player["inventory"], 1):
                print(f"{i}) {inv_item}")


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
    elif item == "healing salve":
        player["health"] += 3
        player["inventory"].remove(item)
        print("you use a healing salve and recover 3 health")
        print(f"Health: {player['health']}")
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

    elif item == "wastland_field_note":
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

    elif item ==  "grovetown_note_1": # to use
        print(
        "There are two kinds.\n"
        "I’m sure of it now.\n\n"
        "The small ones mimic shapes.\n"
        "Animals. Objects. Trash.\n\n"
        "The tall ones mimic *us*."
    )
    elif item == "grovetown_note_2": # to use
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
    

    else:
        print(f"You can’t use {item} right now.")

def get_choice():
    choice = input("> ").lower()
    return choice

def handle_global_input(choice, player):
    if choice == "i":
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

def apply_stamina_health_bonus(player):
    stamina = player["skills"].get("stamina", 0)

    bonus_multiplier = 1 + (stamina * 0.05)
    player["max_health"] = int(player["base_health"] * bonus_multiplier)

    if player["health"] > player["max_health"]:
        player["health"] = player["max_health"]



              