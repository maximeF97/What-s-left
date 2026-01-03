# character_setup.py
# Ask for player name and let the player distribute 10 skill points among stats.
# Returns a dict: {"name": str, "stats": {...}}

BASE_STATS = {
    "stealth": 1,
    "perception": 1,
    "scavenging": 1,
    "lockpicking": 1,
    "intelligence": 1,
    "stamina": 1,
    "luck": 1,
    "charisma": 1
}
POINTS_TO_DISTRIBUTE = 10

# Short descriptions drawn from README (shown to player during allocation)
SKILL_DESCRIPTIONS = {
    "stealth": "Move unseen through the wasteland.",
    "perception": "Notice details you shouldn’t miss… or things you were never meant to see.",
    "scavenging": "Find what you need before someone else does.",
    "lockpicking": "Take what doesn’t belong to you (open locked containers/doors).",
    "intelligence": "Understand alien tech and learn faster.",
    "stamina": "Endure injuries, exhaustion, and fear (increases HP).",
    "luck": "The difference between survival… and sudden death.",
    "charisma": "Talk your way out of situations where bullets won’t help."
}


def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter a non-empty value.")


def ask_name() -> str:
    name = input("Enter your character's name (or press Enter for 'Player'): ").strip()
    if not name:
        name = "Player"
    return name


def _print_all_skill_descriptions():
    print("\nSkill descriptions:")
    for k in BASE_STATS.keys():
        print(f"  {k.capitalize():12} — {SKILL_DESCRIPTIONS.get(k, '')}")
    print()


def allocate_points() -> dict:
    while True:
        remaining = POINTS_TO_DISTRIBUTE
        allocations = {k: 0 for k in BASE_STATS.keys()}

        print(f"\nYou have {POINTS_TO_DISTRIBUTE} skill points to distribute among:")
        print("  " + ", ".join(BASE_STATS.keys()) + ".")
        print("\nTips:")
        print("  - Type a number to assign points to the current stat.")
        print("  - Press Enter to assign 0.")
        print("  - Type 'd' to see all skill descriptions.")
        print("  - Type 's' to see a summary of current allocations.")
        print("  - Type 'r' to restart allocation from the beginning.\n")

        stats_in_order = list(BASE_STATS.keys())
        i = 0
        while i < len(stats_in_order):
            stat = stats_in_order[i]
            desc = SKILL_DESCRIPTIONS.get(stat, "")
            print(f"--- {stat.capitalize()} ---")
            print(desc)
            print(f"Base {stat}: {BASE_STATS[stat]}")
            print(f"Remaining points: {remaining}")
            raw = input(f"Add points to {stat} (0-{remaining}, 'd' descriptions, 's' summary, 'r' restart): ").strip().lower()

            if raw == "d":
                _print_all_skill_descriptions()
                continue
            if raw == "s":
                print("\nCurrent allocations:")
                for k in stats_in_order:
                    print(f"  {k.capitalize():12} = {BASE_STATS[k]} + {allocations[k]} (total {BASE_STATS[k] + allocations[k]})")
                print(f"  Remaining: {remaining}\n")
                continue
            if raw == "r":
                print("Restarting allocation...\n")
                remaining = POINTS_TO_DISTRIBUTE
                allocations = {k: 0 for k in BASE_STATS.keys()}
                i = 0
                continue
            if raw == "":
                val = 0
            else:
                if not raw.isdigit():
                    print("Please enter a non-negative integer, or 'd'/'s'/'r'.\n")
                    continue
                val = int(raw)

            if val < 0:
                print("Enter 0 or a positive number.\n")
                continue
            if val > remaining:
                print(f"You only have {remaining} points left. Try a smaller number.\n")
                continue

            allocations[stat] = val
            remaining -= val
            i += 1  # move to next stat

        # If points remain, auto-assign them to stamina by default
        if remaining > 0:
            print(f"\nYou have {remaining} unassigned points. They will be added to stamina by default.")
            allocations["stamina"] += remaining
            remaining = 0

        # Build final stats
        final = {}
        for stat, base in BASE_STATS.items():
            final[stat] = base + allocations.get(stat, 0)

        # Compute health from stamina
        final["max_health"] = 5 + final.get("stamina", 0) * 5
        final["health"] = final["max_health"]

        # Show final results with descriptions
        print("\nFinal stats:")
        for k in stats_in_order:
            print(f"  {k.capitalize():12} {final[k]:>3}  — {SKILL_DESCRIPTIONS.get(k, '')}")
        print(f"  {'Max Health':12} {final['max_health']:>3}")
        print(f"  {'Health':12} {final['health']:>3}\n")

        # Confirm
        while True:
            conf = input("Confirm these stats? (y/n): ").strip().lower()
            if conf in ("y", "yes"):
                return final
            if conf in ("n", "no"):
                print("\nLet's re-distribute your points.\n")
                break  # restart outer loop
            print("Enter 'y' or 'n'.")


def choose_name_and_stats() -> dict:
    print("=== Character Creation ===")
    name = ask_name()
    stats = allocate_points()
    return {"name": name, "stats": stats}