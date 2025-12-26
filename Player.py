player = {
    "health": 10,
    "inventory": [],
    "weapon": "knife",
    "level": 1,
    "experience": 0,
    "skills": {
        "stealth": 1,
        "perception": 1,
        "scavenging": 1,
        "lockpicking": 1,
        "intelligence": 1,
        "stamina": 1
    }, 
    "has_seen_alien": False,
    "bunker_items_taken": False,
    "bunker_door_unlocked": False,
    "has seen police station alien": False,
    "has police station prisoner was freed": False,
    "has police station evidence room itemstaken": False,
    "has unlocked police station evidence room door": False,
    "has hospital safe opened": False,
    
def level_up(player):
    player["level"] += 1
    player["health"] += 5
    while True: 
        print("Choose a skill to upgrade:")
        for idx, skill in enumerate(player["skills"].keys(), 1):
            print(f"{idx}) {skill} (current level: {player['skills'][skill]})")
        
        choice = input("> ")
        skill_names = list(player["skills"].keys())
        if choice.isdigit() and 1 <= int(choice) <= len(skill_names):
            selected_skill = skill_names[int(choice) - 1]
            player["skills"][selected_skill] += 1
            break
        else:
            print("Invalid choice, please try again.")
    print(f"You leveled up to level {player['level']}! Health increased to {player['health']}")
}
 def skill_check(player, difficulty):
    roll = random.randint(1, 20) + player["level"]
    return roll >= difficulty
}