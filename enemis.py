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
        "hit_chance": 60,
        "xp": 10
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
   "altered_bat": {
    "name": "Altered Bat",
    "description": (
    "A genetically altered bat.\n"
    "Its wings end in grasping claws.\n"
    "Too many eyes blink out of sync.\n"
    "It screams with a voice that isn’t its own."
    ),
    "health": 6,
    "hit_chance": 50,
    "xp": 40
}

}