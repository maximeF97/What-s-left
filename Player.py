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
    "has_pass_hospital_road_count": 0,
    "has_seen_hospital_road_alien": False,
    "farm_house_living_room_unlocked": False,
    "farm_house_fridge_searched": False,
    "farm_house_oven_searched": False,
    "farm_house_counter_searched": False,
    "toaster_metamorph_dead": False,
    "beast_in_farm_house_defeated": False,
    "beast_in_farm_house_woken_up": False,
    "farm_house_upstairs_corpse_searched" : False,
    "farm_house_attic_searched": False,
    
    "farm_house_leaving_room_searched": False,
}

def _coerce_int(value, default):
    """
    Safely convert value to int; if conversion fails, return default.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default)
def apply_setup_to_player(player_dict: dict, setup: dict) -> dict:
    """
    Apply the dict returned by choose_name_and_stats() to the module-level player dict.
    setup: {'name': str, 'stats': {...}} where stats include:
      stealth, perception, scavenging, lockpicking, intelligence, stamina, luck, charisma, health, max_health
    This function updates player_dict in-place and also returns it.
    """
    if not isinstance(player_dict, dict):
        raise TypeError("player_dict must be a dict")

    name = setup.get("name", "Player")
    stats = setup.get("stats", {}) or {}

    # Update skills (safe coercion, keep defaults if missing)
    for skill in ("stealth", "perception", "scavenging", "lockpicking",
                  "intelligence", "stamina", "luck", "charisma"):
        player_dict.setdefault("skills", {})
        player_dict["skills"][skill] = _coerce_int(stats.get(skill, player_dict["skills"].get(skill, 1)), 1)

    # Update health derived from stamina if provided, otherwise use provided health
    stamina = player_dict["skills"].get("stamina", 1)
    computed_max = 15 + stamina * 10
    # If the setup provided explicit health/max_health use them, otherwise compute from stamina
    provided_max = stats.get("max_health")
    provided_health = stats.get("health")
    if provided_max is not None:
        player_dict["max_health"] = _coerce_int(provided_max, computed_max)
    else:
        player_dict["max_health"] = computed_max

    if provided_health is not None:
        player_dict["health"] = _coerce_int(provided_health, player_dict["max_health"])
    else:
        player_dict["health"] = player_dict["max_health"]

    # Keep base_health in sync (optional)
    player_dict["base_health"] = player_dict.get("base_health", 15)
    # store player name
    player_dict["name"] = name
    player_dict["player_name"] = name

    # mark that player was created via setup
    player_dict["created_via_setup"] = True

    return player_dict



    
