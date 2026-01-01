import json
import os

SAVE_FILE = "savegame.json"


def save_game(player):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(player, f, indent=4)
        print("💾 Game saved successfully.")
    except Exception as e:
        print(f"❌ Failed to save game: {e}")


def load_game():
    if not os.path.exists(SAVE_FILE):
        print("❌ No save file found.")
        return None

    try:
        with open(SAVE_FILE, "r") as f:
            player = json.load(f)
        print("📂 Game loaded successfully.")
        return player
    except Exception as e:
        print(f"❌ Failed to load game: {e}")
        return None
