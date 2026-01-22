EQUIPMENT = {
    #headgear
    "cowboy_hat": {
        "slot": "head",
        "bonuses": {
            "luck": 2,
            "damage_reduction": 1
        },
        "description": "A pristine cowboy hat. Somehow untouched by the wasteland."
    },
    "tactical_helmet": {
        "slot": "head",
        "bonuses": {
            "endurance": 3,
            "damage_reduction": 3
        },
        "description": " Helmet designed for precision work and durability"
    },
    "respirator": {
       "slot": "head",
    "bonuses": {
        "stamina": 2,
        "perception": 1
    },
    "flags": {
        "can_breathe_in_alien_environments": True
    },
    "description": (
        "A respirator that filters out harmful airborne particles, "
        "improving endurance and awareness."
    ) },
    #dody gear
    "alien_scientist_suit": {
        "slot": "body",
        "bonuses": {
            "stamina": 3,
            "damage_reduction": 2
        },
        "description": (
            "A broken suit stitched from unknown materials.\n"
            "Smells faintly of antiseptic and ozone."
        )
    },
    "shielded_jacket": {
        "slot": "body",
        "bonuses": {
            "damage_reduction": 4,
            "stamina": 3,   
            "charisma": 1,
        },
        "description": "A jacket reinforced with makeshift shielding, offering enhanced protection."
    },
    #hand gear
    "tactical_gloves": {
        "slot": "hand",
        "bonuses": {
            "damage_reduction": 1,
            "lockpicking": 2,
            "scavenging": 1
        },
        "description": "Gloves designed for precision work and durability."
    },
    #feet gear
    "weary_boots": {
        "slot": "feet",
        "bonuses": {
            "stamina": 1,
            "luck": 1
        },
        "description": "Worn boots that have seen better days but still offer some protection and comfort."
    },
    "tactical_boots": {
        "slot": "feet",
        "bonuses": {
            "stamina": 2,
            "damage_reduction": 2,
        },
        "description": "Boots designed for precision work and durability "
    },
    #IMPLENTS
    "neural_implant": {
        "slot": "implant",
        "bonuses": {
            "intelligence": 3,},
        "description": (
            "A cybernetic implant that enhances cognitive functions,\n"
            "boosting intelligence and problem-solving abilities.\n"
            "give you the ability to understand alien technology better"
        ),
        "flags": {
            "understand_alien_language": True   
        }
    },
    #exoskeleton
    "old_exoskeleton": {
    "name": "Old Exoskeleton",
    "slot": "body",

    "bonuses": {
        "max_hp": 10,
        "strength": 1,
        "perception": 1,
        "endurance": 1,
        "intelligence": 1,
        "stealth": 1,
        "stamina": 2,
    },

    "flags": {
        "damage_reduction_percent": 5,
        "occupies_hands": True,
        "occupies_feet": True
    },

    "description": (
        "A battered military exoskeleton, its servos whining with age.\n"
        "It reinforces your entire body, enhancing every movement —\n"
        "but it feels heavy, like wearing the past itself."
    )
}

}