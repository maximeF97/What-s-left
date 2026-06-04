import random
from systems import level_up, skill_check
player = {
    "health": 15,
    "max_health": 15,
    "base_health": 15,
    "inventory": {},
    "weapon": "rusty_knife",
    "scene": ("old_bunker"),

    "level": 1,
    "experience": 0,
    "equipment": {
        "head": None,
        "body": None,
        "hand": None,
        "feet" : None,
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
    "old_bunker_first_visit": False,
    "has_seen_alien": False,
    "bunker_items_taken": False,
    "bunker_door_unlocked": False,
    "bunker_visite_count": 0,
    "has_taken_artifact": False,

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
    "wasteland_stranger_near_farm_alive": False,#to use later
    "wasteland_stranger_encounter_count": 0,


    "has_pass_hospital_road_count": 0,
    "has_seen_hospital_road_alien": False,
    "medkit_encounter_done": False,
    "has_deal_with_cactus": False,
    "farm_house_living_room_unlocked": False,
    "farm_house_fridge_searched": False,
    "farm_house_oven_searched": False,
    "farm_house_counter_searched": False,
    "toaster_metamorph_dead": False,
    "found_hospital_road_hideout": False,
    "beast_in_farm_house_defeated": False,
    "beast_in_farm_house_woken_up": False,
    "farm_house_upstairs_corpse_searched" : False,
    "farm_house_attic_searched": False,
    "has_visited_mountain_base_count": 0,
    "has_met_john_prisoner": False,
    "farm_house_leaving_room_searched": False,
    "leader_radio_quest_accepted": False,
    "leader_radio_quest_completed": False,
    "has_completed_leader_quest": False,
    "has_completed_leader_second_quest": False,
    "has_left_the_bunker": False,  
    "has_accepted_leader_quest": False,
    "has_accepted_leader_second_quest": False,
    #abandoned outpost related
    "abandoned_outpost_tent_searched": False,
    "abandoned_outpost_device_examined": False,
    "mountain_door_opened": False,
    "abandoned_outpost_left_body_searched": False,
    "abandoned_outpost_right_body_searched": False,
    "abandoned_outpost_center_body_searched": False,
    "abandoned_outpost_right_body_seen_moving": False,
    "thomas_encountered": False,
    "thomas_killed": False,
    "thomas_seemed_human": False,
    "thomas_suspicious": False,
    "thomas_allied": False,
    #secret mountain base related
    "cafeteria_hidden_compartment_found": False,
    "basement_machine_deactivated": False,
    "find_secret_ray_gun_in_basement": False,
    "first_visite_to_legionaire_room": False,
    "has_help_said": False,
    "woken_gardian": False,
    "found_research_development_lab_code": False,
    "found_red_striped_keycard": False,



    "can_accept_thomas_quest": False,
    "found_invisible_alien": False,
    "wasteland_4_count": 0,
    "invisible_alien_ally": False,# whether the invisible alien is allied with the player to use later"
    "can_breathe_in_alien_environments": False,
    "has_eaten_10_fruits": False,
    "thomas_quest_accepted": False,
    #bastion
    "bastion_security_level": 0,
    "bastion_entrance_visited": False,
    "way_toward_bastion_after_beast_count": 0,
    "way_toward_bastion_after_beast_luck_check_passed": False,
    "bastion_entrance_count": 0,
    "bastion_gard_paid": False,
    "bastion_scout_quest_accepted": False,
    "has_rescued_bastion_scout": False,
    "complited_bastion_scout_quest": False,
    "bastion_full_clearance": False,
    "has_given_alien_tech_to_engineer": 0,
    "engineer_reward_15_given": False,
    "engineer_reward_5_given": False,
    "engineer_reward_3_given": False,
    "engineer_reward_10_given": False,
    "has_upgraded_implant": False,
    "needs_implant_parts": False,
    "bastion_base_mission_completed": False,
    "received_scout_exoskeleton": False,
    #factory area
    "has_found_secret_path_near_factory": False,
    "has_looted_secret_stranger": False,
    "old_factory_entrance_skill_check_passed": False,
    "old_factory_centipede_killed": False,
    "has_help_bastion_scout": False,
    "has_retreve_scout_files": False,
    "found_hospital_road_hideout": False,
    "has_passed_wasteland_2_count": 0,
    "wasteland_2_shroom_man_killed": False,
    "found_lucky_loot_near_factory": False,
    "found_scavenged_loot_near_factory": False,
    "has_seen_laser_tripwires": False,
    "factory_machine_room_cleared": False,
    "kill_the_centipedes": False,
    "factory_first_floor_crates_looted": False,
    "has_verified_scout_identity": False,
    "factory_main_turret_destroyed": False, 
    "machine_room_looted": False,
    "understand_alien_language" : False,#implimentation later--------------------------------
    "eldritch_heart_seized": 0,
    #based on bastion system
    "became_bastion_scout": True,
    "bastion_rank": 1,
    "bastion_active_quest": "scout_outpost",
    "bastion_completed_quests": [],
    #alien land related
    "alien_land_2_count": 0,
    "spore_wall_zombie_killed": False,
    "has_survived_horde_in_alien_land": False,   
    "twisted_forest_searched_soldier": False,
    "outpost_data_count": 0,
    "side_entrance_alien_killed": False,
    "visited_military_base_entrance": False,
    "enemy_in_outpost_killed_count": 0,#------------------------
    "reactivated_security_robot": False,#-------------------------
    "has_deactivated_security_robots": False,
    "activated_security_system": False,
    "has_looted_safe_in_millitary_base": False,
    "has_looted_cabinet_in_millitary_base": False,
    "has_salvaged_armory_in_millitary_base": False,
    "ai_lied_about_core": False,
    "tried_core_by_force": False,
    "introduced_to_core": False,
    "understand_security_system": False,
    "defeated_medical_bay_enemies": False,
    "opend_bedroom_locker" : False,
    "searched_bedroom_secret_room": False,
    "searched_storage_room": False,
    "has_checked_computer_console": False,
    "searched_medical_bay_upstairs": False,
    "has_alien_targeting_implant": False,
    #prison ark related
    "has_oppend_fence_gate": False,

    "sporebound_slave_killed_in_forest": False,
    #eldrich heart related
    "midnight_tower_seized_heart": False,
}
player.setdefault("outpost_data_count", 0)
player.setdefault("enemy_in_outpost_killed_count", 0)
player.setdefault("weird_fruit_eaten", 0)
player.setdefault("status_effects", {})
player.setdefault("eldritch_eyes", False)
player.setdefault("eldritch_heart_seized", 0)
def _coerce_int(value, default):
    """
    Safely convert value to int; if conversion fails, return default.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default)
def eldrich_heart_seize(player):
    if player.get("eldritch_heart_seized", 0) == 3:
            eldrich_ending(player)
        
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



    
