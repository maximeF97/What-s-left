import random
from systems import level_up, skill_check
player = {
    "health": 10,
    "max_health": 15,
    "base_health": 15,
    "inventory": {},
    "weapon": "rusty_knife",

    "level": 1,
    "experience": 0,
    "equipment": {
        "head": None,
        "body": None,
        "hand": None,
        "boot": None,
        "implant": None
    },
    "skills": {
        "stealth": 1,
        "perception": 1,
        "scavenging": 1,
        "lockpicking": 1,
        "intelligence": 1,
        "stamina": 1,
        "luck": 1,
        "charisma": 1
    },

    # story flags
    "has_seen_alien": False,
    "bunker_items_taken": False,
    "bunker_door_unlocked": False,
    "wasteland_2_body_looted": False,
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
    "Hospital_first_floor_right_room_note_taken": False,
    "has_opened_hospital_back_door": False,
    "passed_wastland_3_skill_check": False, #still thinking to use or not
    "looted_the_bedroll": False,
    "met_wasteland_stranger_near_farm": False,
}




    
