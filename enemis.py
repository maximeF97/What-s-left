import copy

def get_enemy(enemy_id):
    if enemy_id not in ENEMIES:
        raise ValueError(f"Unknown enemy: {enemy_id}")
    return copy.deepcopy(ENEMIES[enemy_id])


ENEMIES = {

# ---------------- BASIC ALIENS ----------------

"small_alien": {
    "name": "Small Alien",
    "health": 6,
    "hit_chance": 60,
    "damage": 3,
    "xp": 10,
    "attack_messages": [
        "The alien moves like a shadow, claws flashing toward you!"
    ],
    "miss_messages": [
        "The alien darts past you, striking only air."
    ],
    "special_attack_chance": 0.15,
    "special_attack_multiplier": 1.8,
    "special_attack_messages": [
        "The alien shrieks as barbed tendrils whip toward your throat!"
    ]
},

"small_metamorph": {
    "name": "Small Metamorph",
    "health": 8,
    "hit_chance": 65,
    "damage": 4,
    "xp": 20,
    "attack_messages": [
        "The metamorph twists mid-strike, slamming into you!"
    ],
    "miss_messages": [
        "The creature liquefies and slips past your counter."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "Its body spikes outward, tearing into you!"
    ]
},

"alien_metamorph": {
    "name": "Alien Metamorph",
    "health": 10,
    "hit_chance": 75,
    "damage": 5,
    "xp": 70,
    "attack_messages": [
        "The alien morphs instantly, striking with surgical precision!"
    ],
    "miss_messages": [
        "The creature melts away before your eyes."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 2.2,
    "special_attack_messages": [
        "It erupts into a monstrous form and crashes into you!"
    ]
},
"alien_soldier": {
    "name": "Alien Soldier",
    "health": 25,
    "hit_chance": 80,
    "damage": 10, 
    "xp": 150,
    "description": "A towering alien warrior clad in advanced armor, wielding a high-powered energy weapon.",
    "attack_messages": [
        "The alien soldier fires its energy weapon with deadly accuracy!"
    ],
    "miss_messages": [
        "The blast sizzles past you, scorching the ground."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.5,
    "special_attack_messages": [
        "The soldier charges up a massive energy blast and unleashes it!"
    ]
},
"alien_scientist": {
    "name": "Alien Scientist",
    "health": 15,
    "hit_chance": 70,
    "damage": 6,
    "xp": 100,
    "description": "A cunning alien researcher, using advanced technology to manipulate the battlefield.",
    "attack_messages": [
        "The scientist shoots a burst of energy!"
    ],
    "miss_messages": [
        "The gun misfires harmlessly."
    ],
    "special_attack_chance": 0.3,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "The scientist unleashes a devastating energy pulse!"
    ]
},

# ---------------- HUMANOIDS ----------------

"cyborg_scavenger": {
    "name": "Cyborg Scavenger",
    "health": 11,
    "hit_chance": 70,
    "damage": 5,
    "xp": 80,
    "attack_messages": [
        "The scavenger lunges, servo-blades screaming!"
    ],
    "miss_messages": [
        "The cyborg recalibrates after missing its strike."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 1.7,
    "special_attack_messages": [
        "Hidden weapons deploy, unloading a brutal burst!"
    ]
},

"wasteland_cowboy": {
    "name": "Wasteland Stranger",
    "health": 16,
    "hit_chance": 80,
    "damage": 7,
    "xp": 100,
    "attack_messages": [
        "The stranger fires without hesitation!"
    ],
    "miss_messages": [
        "The bullet kicks up dust beside your head."
    ],
    "special_attack_chance": 0.15,
    "special_attack_multiplier": 2.5,
    "special_attack_messages": [
        "He steadies his breath and pulls the trigger — dead center!"
    ]
},

"humain": {
    "name": "Human Raider",
    "health": 12,
    "hit_chance": 75,
    "damage": 4,
    "xp": 50,
    "attack_messages": [
        "The raider swings wildly at you!"
    ],
    "miss_messages": [
        "The raider stumbles and misses."
    ]
},
"thomas": {
    "name": "Thomas the Outpost Survivor",
    "health": 18,
    "hit_chance": 80,
    "damage": 6,
    "xp": 150,
    "attack_messages": [
        "Thomas fires his rifle with shaky hands!"
    ],
    "miss_messages": [
        "His hesitation costs him the shot."
    ]
},
# ---------------- CREATURES ----------------

"giant_centipede": {
    "name": "Giant Centipede",
    "health": 15,
    "hit_chance": 65,
    "damage": 6,
    "xp": 200,
    "attack_messages": [
        "The centipede lunges, mandibles snapping!"
    ],
    "miss_messages": [
        "The creature snaps shut just beside you."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "It coils around your leg and bites deep!"
    ]
},

"armored_giant_centipede": {
    "name": "Armored Giant Centipede",
    "health": 30,
    "hit_chance": 70,
    "damage": 6,
    "xp": 250,
    "attack_messages": [
        "The armored centipede slams into you!"
    ],
    "miss_messages": [
        "Its plated body scrapes past you."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 2.2,
    "special_attack_messages": [
        "The centipede impales you with armored fangs!"
    ]
},


# ---------------- BOSSES ----------------

"mutated_capibara": {
    "name": "Mutated Capibara",
    "health": 40,
    "hit_chance": 75,
    "damage": 10,
    "xp": 300,
    "attack_messages": [
        "The thing barrels toward you, flesh rippling unnaturally!"
        "You hear bone grinding beneath its skin as it charges!"
    ],
    "miss_messages": [
        "It crashes past you, tearing chunks from the ground."
        "It slams into the ground, leaving a smear of blood and fur behind."
        
    ],
    "special_attack_chance": 0.3,
    "special_attack_multiplier": 2.5,
    "special_attack_messages": [
        "Its jaw unhinges wider than possible — and it charges."
    ]
},

"iron_warden": {
    "name": "Iron Warden",
    "health": 40,
    "hit_chance": 85,
    "damage": 10,
    "xp": 300,
    "attack_messages": [
        "The Warden brings its fist down like a hammer!"
    ],
    "miss_messages": [
        "The blow shatters the ground beside you."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "Its core glows white-hot as it unleashes a crushing strike!"
    ]
},
"hell_genetically_altered_bat": {
    "name": "Altered Bat",
    "health": 25,
    "hit_chance": 66,
    "damage": 6,
    "xp": 200,
    "attack_messages": [
        "The bat dives, claws raking!"
    ],
    "miss_messages": [
        "The bat shrieks as it misses."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.1,
    "special_attack_messages": [
        "A mind-shattering screech precedes a savage strike!"
    ]
},

# ---------------- DEFENSE SYSTEMS ----------------

"turret": {
    "name": "Automated Turret",
    "health": 20,
    "hit_chance": 80,
    "damage": 8,
    "xp": 150,
    "attack_messages": [
        "The turret whirs to life and fires a burst of gunfire!"
    ],
    "miss_messages": [
        "Rounds spark against the walls as the turret misses."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "The turret locks on — unloading a devastating barrage!"
    ]
},

# ---------------- HEAVY ROBOTS ----------------


"rustbound_guardian": {
    "name": "Rustbound Guardian",
    "health": 20,
    "hit_chance": 80,
    "damage": 7,
    "xp": 150,
    "attack_messages": [
        "The guardian swings a rusted arm toward you!"
    ],
    "miss_messages": [
        "The massive arm crashes down just short."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "The guardian enters overdrive, smashing you relentlessly!"
    ]
},

"rustbound_legionnaire": {
    "name": "Rustbound Legionnaire",
    "health": 15,
    "hit_chance": 75,
    "damage": 5,
    "xp": 100,
    "attack_messages": [
        "The legionnaire swings its corroded blade!"
    ],
    "miss_messages": [
        "It skids past you in a spray of rust."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 1.8,
    "special_attack_messages": [
        "The legionnaire blurs with speed, striking from an impossible angle!"
    ]
},

"rustbound_vanguard": {
    "name": "Rustbound Vanguard",
    "health": 30,
    "hit_chance": 70,
    "damage": 9,
    "xp": 250,
    "attack_messages": [
        "The vanguard shoots a volley of corroded projectiles!"
    ],
    "miss_messages": [
        "Its shots clang off nearby debris."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.2,
    "special_attack_messages": [
        "a barrage of rusted shrapnel erupts toward you!"
    ]
},

# ---------------- DRONES & ADVANCED UNITS ----------------

"perimeter_drone": {
    "name": "Perimeter Drone",
    "health": 18,
    "hit_chance": 75,
    "damage": 4,
    "xp": 25,
    "description": "A hovering security drone equipped with light weaponry and surveillance gear.",
    "attack_messages": [
        "The drone fires a precise energy shot!"
    ],
    "miss_messages": [
        "The shot streaks past your shoulder."
    ],
    "special_attack_chance": 0.3,
    "special_attack_multiplier": 1.6,
    "special_attack_messages": [
        "The drone scans you — then fires with lethal accuracy!"
    ]
},

"iron_legionnaire": {
    "name": "Iron Legionnaire",
    "health": 35,
    "hit_chance": 65,
    "damage": 6,
    "xp": 60,
    "description": "A heavily armored robotsoldier from a bygone era, its mechanical frame built for relentless combat.",
    "attack_messages": [
        "The legionnaire advances, striking with military precision!"
    ],
    "miss_messages": [
        "Its blade whistles past you."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "Armor plates lock as it delivers a devastating blow!"
    ]
},

"vanguard_mk2": {
    "name": "Vanguard Mk-II",
    "health": 28,
    "hit_chance": 80,
    "damage": 8,
    "xp": 80,
    "description": "A sleek combat drone equipped with advanced targeting systems and heavy weaponry.",
    "attack_messages": [
        "The Vanguard fires with chilling precision!"
    ],
    "miss_messages": [
        "The shot narrowly misses your head."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 2.1,
    "special_attack_messages": [
        "Targeting systems recalibrate — critical strike!"
    ]
},
"steel_plated_guardian": {
    "name": "Steel-Plated Guardian",
    "health": 45,
    "hit_chance": 70,
    "damage": 10,
    "xp": 200,
    "description": "A massive robot built for heavy defense, its steel plating nearly impervious to damage.",
    "attack_messages": [
        "The guardian slams its steel fist down!"
    ],
    "miss_messages": [
        "The ground trembles as its fist crashes beside you."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.3,
    "special_attack_messages": [
        "Its core glows fiercely as it unleashes a powerful shockwave!"
    ]
},

# ---------------- HORROR CYBORGS ----------------
"cyborg_horror": {
    "name": "Cyborg Horror",
    "health": 28,
    "hit_chance": 68,
    "damage": 6,
    "xp": 90,
    "description": "A nightmarish fusion of flesh and machine, its form twisted and grotesque.\n"
    "a twitching red light emanates from a implanted device.",
    "attack_messages": ["The cyborg lunges with razor-sharp limbs!"],
    "miss_messages": ["something inside him make it esitate and miss."],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "The cyborg emits a horrifying screech as it attacks ferociously!"
    ]
},
"weeping_cyborg": {
    "name": "Weeping Cyborg",
    "health": 30,
    "hit_chance": 70,
    "damage": 7,
    "xp": 75,

    "attack_messages": [
        "The cyborg attacks through sobbing static!"
    ],
    "miss_messages": [
        "he hesitates and misses, humanity inside him still struggling."
    ],
    "special_attack_chance": 0.3,
    "special_attack_multiplier": 2.3,
    "special_attack_messages": [
        "It screams, systems overwrite, and tears into you!"
    ]
},

"echoframe": {
    "name": "Echoframe",
    "health": 22,
    "hit_chance": 75,
    "damage": 5,
    "xp": 45,
    "description": "An advanced humanoid cyborg that emits unsettling echoes of past conversations.",
    "attack_messages": [
        "The machine strikes while whispering broken words!"
    ],
    "miss_messages": [
        "Its limbs twitch past you harmlessly."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 1.9,
    "special_attack_messages": [
        "A psychic pulse disorients you as it attacks!"
    ]
},

# ---------------- SPORE INFECTED ----------------

"sporebound_automaton": {
    "name": "Sporebound Automaton",
    "health": 26,
    "hit_chance": 65,
    "damage": 6,
    "xp": 65,
    "description": "A rusted robot overrun by fungal growths, its look like it has a mind of its own.",
    "attack_messages": [
        "The fungus-covered machine lurches forward!"
    ],
    "miss_messages": [
        "Spores burst as it misses its strike."
    ],
    "special_attack_chance": 0.25,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "A cloud of spores erupts as it slams into you!"
    ]
},

"sporebound_slave": {
    "name": "Sporebound Slave",
    "health": 14,
    "hit_chance": 70,
    "damage": 4,
    "xp": 30,
    "description": "A humanoid figure, its body twisted and controlled by invasive fungal growths.",
    "attack_messages": [
        "The man lunges, coughing spores!"
    ],
    "miss_messages": [
        "It stumbles, barely missing you."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 1.7,
    "special_attack_messages": [
        "It convulses violently, striking with unnatural strength!"
    ]
},

# ---------------- PLANT ENEMIES ----------------

"carnivorous_trap_plant": {
    "name": "Carnivorous Trap Plant",
    "health": 15,   
    "hit_chance": 60,
    "damage": 5,
    "xp": 80,
    "description": "A large, stationary plant with a beautiful flower and hidden thorns, waiting to snap shut on prey.",
    "attack_messages": [
        "The trap plant snaps its thorny vines toward you!"
    ],
    "miss_messages": [
        "The plant's vines lash out but miss you."
    ],
    "special_attack_chance": 0.2,
    "special_attack_multiplier": 2.0,
    "special_attack_messages": [
        "The plant's vines slash you through from an unexpected angle!"
    ],
},


}