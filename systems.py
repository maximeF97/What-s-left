import random 
from save_system import save_game, load_game
from equipment import EQUIPMENT

def level_up(player):
    player["level"] += 1
    player["experience"] = 0
    save_game(player)
    player["health"] = player["max_health"]
    print("You feel refreshed. Health fully restored!")
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



def get_choice():
    #return ui.wait_for_input()

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



def apply_bonuses(player, bonuses):
    for stat, value in bonuses.items():
        player["skills"][stat] = player["skills"].get(stat, 0) + value

def remove_bonuses(player, bonuses):
    for stat, value in bonuses.items():
        player["skills"][stat] = max(
            0,
            player["skills"].get(stat, 0) - value)


def equip_item(player, item):
    if item not in EQUIPMENT:
        print("You can't equip that.")
        return

    gear = EQUIPMENT[item]
    slot = gear["slot"]

    current = player["equipment"].get(slot)
    if current:
        remove_bonuses(player, EQUIPMENT[current]["bonuses"])
        print(f"You remove the {current.replace('_', ' ')}.")

    player["equipment"][slot] = item
    apply_bonuses(player, gear["bonuses"])

    print(f"You equip the {item.replace('_', ' ')}.")
              
def unequip_item(player, slot):
    current = player["equipment"].get(slot)
    if not current:
        print("Nothing equipped there.")
        return

    remove_bonuses(player, EQUIPMENT[current]["bonuses"])
    player["equipment"][slot] = None
    print(f"You remove the {current.replace('_', ' ')}.")
def inspect_item(player, item):
    if item in EQUIPMENT:
        print(EQUIPMENT[item]["description"])
        print("1) Equip")
        print("2) Back")

        choice = get_choice()
        if choice == "1":
            equip_item(player, item)
