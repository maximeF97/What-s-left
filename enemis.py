# enemies.py
import copy

def get_enemy(enemy_id):
    if enemy_id not in ENEMIES:
        raise ValueError(f"Unknown enemy: {enemy_id}")
    return copy.deepcopy(ENEMIES[enemy_id])

ENEMIES = {
    "small_alien": {
        "name": "Small Alien",
        "health": 6,
        "description": (
            "A small, dark insectoid alien.\n"
            "It has sharp claws and a chitinous exoskeleton.\n"
            "Its multifaceted eyes glint with intelligence."
        ),
        "hit_chance": 60,
        "xp": 10
    },
    "small_metamorph": {
        "name": "Small Metamorph",
        "description": (
            "A small, shape-shifting creature.\n"
            "Its form constantly shifts and changes.\n"
            "It moves with eerie grace and unpredictability."
        ),
        "health": 8,
        "hit_chance": 65,
        "xp": 20
},
    "alien_metamorph": {
        "name": "Alien Metamorph",
        "health": 10,
        "hit_chance": 75,
        "xp": 70
    },

    "cyborg_scavenger": {
        "name": "Cyborg Scavenger",
        "health": 11,
        "hit_chance": 70,
        "xp": 80
    },

    "wasteland_cowboy": {
        "name": "Wasteland Stranger",
        "health": 16,
        "hit_chance": 80,
        "xp": 100
    },
   "hell_genetically_altered_bat": {
    "name": "Altered Bat",
    "description": (
    "A genetically altered bat.\n"
    "Its wings end in grasping claws.\n"
    "Too many eyes blink out of sync.\n"
    "It screams with a voice that isn’t its own."
    ),
    "health": 25,
    "hit_chance": 66,
    "dammage": 6,
    "xp": 200
},
  "humain": {
        "name": "Humain",
        "health": 12, 
        "hit_chance": 75,
        "damage": 4,
        "xp": 50
    },  
    "turret": {
        "name": "Turret",
        "health": 20,
        "hit_chance": 80,
        "description": (
            "An automated turret that can hide and shoot at intruders.\n"),
        "damage": 8,
        "xp": 150
    },
    "iron_warden": {
        "name": "Iron Warden",
        "description": (
            "A towering robotic guardian.\n"
            "made to protect ancient secrets from alien threats.\n"),
        "health": 40,   
        "hit_chance": 85,
        "damage": 10,
        "xp": 300
},
"rustbound_gardian": {
        "name": "Rustbound Guardian",
        "description": (
            "A massive robot, corroded by time but still functional.\n"
            "It patrols the ruins, attacking anything that moves."
        ),
        "health": 20,
        "hit_chance": 80,
        "damage": 7,
        "xp": 150,
        "specials": [
            {
                "id": "overdrive",
                "text": "The Guardian powers up its systems, increasing its attack power.", 
                "effect": {"attack_bonus": 3, "duration": 2}
            }
        ]
    },
"rustbound_sentinel": {
        "name": "Rustbound Sentinel",
        "description": (
            "A smaller, agile robot covered in rust.\n"
            "It darts around quickly, making it hard to hit."
        ),
        "health": 15,
        "hit_chance": 75,
        "damage": 5,
        "xp": 100,
        "specials": [
            {
                "id": "evasive_maneuver",
                "text": "The Sentinel swiftly dodges incoming attacks, increasing its evasion.",    
                "effect": {"evasion_bonus": 15, "duration": 1}
            }
        ]
    },
"Rustbound Enforcer": {
        "name": "Rustbound Enforcer",
        "description": (
            "A heavily armored robot, built for combat.\n"
            "Its rusted exterior belies its deadly capabilities."
        ),
        "health": 30,
        "hit_chance": 70,
        "damage": 9,
        "xp": 250
    },

    "perimeter_drone": {
        "name": "Perimeter Drone",
        "description": (
            "A hovering security drone stitched together from rusted alloys.\n"
            "Its lenses flicker as it scans for intruders long after its creators died."
        ),
        "health": 18,
        "attack": 4,
        "defense": 1,
        "accuracy": 75,
        "xp": 25,
        "specials": [
            {
                "id": "scan",
                "text": "The drone scans you, adjusting its aim.",
                "effect": {"accuracy_bonus": 20, "duration": 1}
            }
        ]
    },

    "iron_legionnaire": {
        "name": "Iron Legionnaire",
        "description": (
            "A towering automaton clad in scorched military plating.\n"
            "It marches forward, executing a war that never ended."
        ),
        "health": 35,
        "attack": 6,
        "defense": 4,
        "accuracy": 65,
        "xp": 60,
        "specials": [
            {
                "id": "armor_plating",
                "text": "Thick armor absorbs part of the damage.",
                "effect": {"flat_damage_reduction": 2, "hits": 2}
            }
        ]
    },

    "vanguard_mk2": {
        "name": "Vanguard Mk-II",
        "description": (
            "An elite combat unit marked with faded command insignia.\n"
            "Its movements are precise, calculated, and lethal."
        ),
        "health": 28,
        "attack": 8,
        "defense": 2,
        "accuracy": 80,
        "xp": 80,
        "specials": [
            {
                "id": "adaptive_targeting",
                "text": "The Vanguard recalibrates after every move.",
                "effect": {"accuracy_ramp": 5}
            }
        ]
    },

    "weeping_cyborg": {
        "name": "Weeping Cyborg",
        "description": (
            "Oil and tears drip from a ruined face.\n"
            "Something human still screams inside the metal shell."
        ),
        "health": 30,
        "attack": 7,
        "defense": 2,
        "accuracy": 70,
        "xp": 75,
        "specials": [
            {
                "id": "pain_surge",
                "text": "The cyborg screams as its systems overload.",
                "effect": {"attack_bonus_below_hp_pct": 50, "attack_bonus": 2}
            }
        ]
    },

    "echoframe": {
        "name": "Echoframe",
        "description": (
            "This machine mutters broken phrases from another life.\n"
            "Its limbs twitch as if haunted by memory."
        ),
        "health": 22,
        "attack": 5,
        "defense": 1,
        "accuracy": 75,
        "xp": 45,
        "specials": [
            {
                "id": "echo_pulse",
                "text": "Distorted voices disorient you.",
                "effect": {"player_accuracy_penalty": 15, "duration": 1}
            }
        ]
    },

    "sporebound_automaton": {
        "name": "Sporebound Automaton",
        "description": (
            "Fungal growths burst through cracked steel.\n"
            "The machine no longer follows human commands."
        ),
        "health": 26,
        "attack": 6,
        "defense": 2,
        "accuracy": 65,
        "xp": 65,
        "specials": [
            {
                "id": "spore_cloud",
                "text": "A cloud of alien spores fills the air.",
                "effect": {"player_stamina_penalty": 1, "duration": 2}
            }
        ]
    },

    "broken_sentinel": {
        "name": "Broken Sentinel",
        "description": (
            "Half-buried in debris, the Sentinel reactivates.\n"
            "Its warning siren blares as it defends nothing."
        ),
        "health": 40,
        "attack": 5,
        "defense": 5,
        "accuracy": 55,
        "xp": 70,
        "specials": [
            {
                "id": "alarm_mode",
                "text": "The Sentinel locks into a defensive stance.",
                "effect": {"defense_bonus": 2, "duration": 1}
            }
        ]
    },

    "remnant_walker": {
        "name": "Remnant Walker",
        "description": (
            "A heavy machine drags itself forward.\n"
            "The mind inside never realized it was already dead."
        ),
        "health": 34,
        "attack": 6,
        "defense": 3,
        "accuracy": 60,
        "xp": 70,
        "specials": [
            {
                "id": "relentless",
                "text": "The walker struggles back to its feet.",
                "effect": {"revive_chance": 0.3, "revive_hp_pct": 0.3}
            }
        ]
    },
}

