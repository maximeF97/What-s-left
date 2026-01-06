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
}