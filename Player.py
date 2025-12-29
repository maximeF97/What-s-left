import random
from systems import level_up, skill_check
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
        "stamina": 1,
        "luck": 1
    },

    # story flags
    "has_seen_alien": False,
    "bunker_items_taken": False,
    "bunker_door_unlocked": False,

    "has_seen_police_station_alien": False,
    "has_freed_police_station_prisoner": False,
    "has_taken_police_station_evidence_items": False,
    "has_unlocked_police_station_evidence_room": False,
    "burned_houses_looted": False,
    "has_opened_hospital_safe": False,
    "has_oppened_hospital_lock": False,
    "has_killed_cactus": False,
    "has_pass_window_check": False,
    "hospital_metamorph_killed": False,
    "hospital_scavenger_killed": False,
    "has_hospital_left_room_been_searched": False,
    "has_defeated_hospital_boss": False,
    "has_help_basement_prisoner": False,
    "hospital_flower_pot_check": False,
    "hospital_trash_pot_check": False,
    "try_hacking_hospital_pc": False,
    "has_taken_hospital_pc_fafe": False,
}



    
