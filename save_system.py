import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

SAVE_DIR = "saves"                 # Directory for multiple save files
QUICK_SAVE_FILE = "savegame.json"  # Back-compat: single quick-save file
LAST_SELECTED_FILE = os.path.join(SAVE_DIR, ".last_selected.json")


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _atomic_write_json(path: str, data: Dict[str, Any]) -> None:
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    os.replace(tmp_path, path)  # atomic on POSIX and Windows


def _read_json(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _save_path(save_id: str) -> str:
    return os.path.join(SAVE_DIR, f"{save_id}.json")


def _load_last_selected() -> Optional[str]:
    data = _read_json(LAST_SELECTED_FILE)
    if data and isinstance(data.get("save_id"), str):
        return data["save_id"]
    return None


def _persist_last_selected(save_id: str) -> None:
    _ensure_dir(SAVE_DIR)
    _atomic_write_json(LAST_SELECTED_FILE, {"save_id": save_id, "updated_at": _now_iso()})


def save_game(player: Dict[str, Any], save_id: Optional[str] = None) -> str:
    """
    Save the game state to saves/<save_id>.json with metadata.
    If save_id is None, a timestamp-based ID is generated.
    Returns the save_id.
    """
    try:
        _ensure_dir(SAVE_DIR)
        if save_id is None:
            save_id = datetime.now().strftime("save-%Y%m%d-%H%M%S")

        data = {
            "meta": {
                "save_id": save_id,
                "updated_at": _now_iso(),
                # Optional metadata pulled from player if present:
                "scene": player.get("scene"),
                "position": player.get("position"),
                "playtime": player.get("playtime"),
            },
            "player": player,
        }
        path = _save_path(save_id)
        _atomic_write_json(path, data)
        print(f"💾 Game saved successfully: {path}")
        # Set this as last selected
        _persist_last_selected(save_id)
        return save_id
    except Exception as e:
        print(f"❌ Failed to save game: {e}")
        raise


def quick_save(player: Dict[str, Any]) -> None:
    """
    Back-compat quick save to a single file (savegame.json).
    """
    try:
        with open(QUICK_SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(player, f, indent=4)
        print(f"💾 Quick-saved to {QUICK_SAVE_FILE}.")
    except Exception as e:
        print(f"❌ Failed to quick-save game: {e}")


def list_saves() -> List[Dict[str, Any]]:
    """
    Returns a list of saves sorted by updated_at descending.
    Each entry: {"path": str, "save_id": str, "updated_at": str, "meta": dict}
    """
    _ensure_dir(SAVE_DIR)
    saves: List[Dict[str, Any]] = []
    for name in os.listdir(SAVE_DIR):
        if not name.endswith(".json"):
            continue
        if name == os.path.basename(LAST_SELECTED_FILE):
            continue
        path = os.path.join(SAVE_DIR, name)
        data = _read_json(path)
        if not data or "meta" not in data or "player" not in data:
            continue
        meta = data["meta"]
        save_id = meta.get("save_id") or name[:-5]
        updated_at = meta.get("updated_at") or "1970-01-01T00:00:00Z"
        saves.append({"path": path, "save_id": save_id, "updated_at": updated_at, "meta": meta})
    # Sort latest first
    saves.sort(key=lambda s: s["updated_at"], reverse=True)
    return saves


def get_latest_save() -> Optional[Dict[str, Any]]:
    saves = list_saves()
    return saves[0] if saves else None


def load_game(save_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Loads a save by ID. If save_id is None, tries:
      1) last-selected save
      2) latest save by timestamp
      3) fallback to quick-save (savegame.json) if present
    Returns the player dict or None.
    """
    try:
        chosen_id = save_id or _load_last_selected()
        if chosen_id:
            path = _save_path(chosen_id)
            if os.path.exists(path):
                data = _read_json(path)
                if data and "player" in data:
                    print(f"📂 Loaded save '{chosen_id}'.")
                    _persist_last_selected(chosen_id)
                    return data["player"]
                else:
                    print(f"❌ Save file corrupted: {path}")

        latest = get_latest_save()
        if latest:
            data = _read_json(latest["path"])
            if data and "player" in data:
                print(f"📂 Loaded latest save '{latest['save_id']}'.")
                _persist_last_selected(latest["save_id"])
                return data["player"]

        # Fallback to quick-save
        if os.path.exists(QUICK_SAVE_FILE):
            with open(QUICK_SAVE_FILE, "r", encoding="utf-8") as f:
                player = json.load(f)
            print("📂 Loaded quick-save.")
            return player

        print("❌ No save file found.")
        return None
    except Exception as e:
        print(f"❌ Failed to load game: {e}")
        return None


def load_menu_interactive(default_to_last_selected: bool = True) -> Optional[Dict[str, Any]]:
    """
    Interactive terminal load menu that:
      - Lists all saves sorted by latest
      - Preselects last-selected if available, otherwise latest
      - Press Enter to load the preselected item
      - Or type the number to select another save
      - 'q' to cancel

    Returns the loaded player dict or None.
    """
    saves = list_saves()
    if not saves:
        print("❌ No saves found.")
        return None

    last_selected = _load_last_selected() if default_to_last_selected else None

    # Find initial index
    initial_idx = 0
    if last_selected:
        for i, s in enumerate(saves):
            if s["save_id"] == last_selected:
                initial_idx = i
                break

    print("\n=== Load Game ===")
    for idx, s in enumerate(saves):
        marker = "▶" if idx == initial_idx else " "
        scene = s["meta"].get("scene") or "-"
        when = s["updated_at"]
        print(f"{marker} [{idx+1}] {s['save_id']}  ({when})  scene={scene}")

    print("\nPress Enter to load the preselected save, number to choose, or 'q' to cancel.")
    choice = input("> ").strip()

    if choice.lower() == "q":
        print("Cancelled.")
        return None

    if choice == "":
        chosen = saves[initial_idx]
    else:
        if not choice.isdigit():
            print("Invalid input.")
            return None
        idx = int(choice) - 1
        if not (0 <= idx < len(saves)):
            print("Invalid selection.")
            return None
        chosen = saves[idx]

    _persist_last_selected(chosen["save_id"])
    data = _read_json(chosen["path"])
    if not data or "player" not in data:
        print("❌ Selected save is corrupted.")
        return None

    print(f"📂 Loaded save '{chosen['save_id']}'.")
    return data["player"]


# Optional: demo usage when running directly
if __name__ == "__main__":
    # Example player object; include optional metadata like scene/position if you have it
    example_player = {
        "name": "Hero",
        "level": 7,
        "hp": 42,
        "scene": "ForestEntrance",
        "position": {"x": 12.3, "y": 0.0, "z": -4.5},
        "playtime": 3600,
    }

    cmd = sys.argv[1] if len(sys.argv) > 1 else "menu"
    if cmd == "save":
        save_id = sys.argv[2] if len(sys.argv) > 2 else None
        save_game(example_player, save_id=save_id)
    elif cmd == "load":
        save_id = sys.argv[2] if len(sys.argv) > 2 else None
        player = load_game(save_id=save_id)
        print("Player:", player)
    elif cmd == "quick-save":
        quick_save(example_player)
    else:
        # Default: launch interactive load menu
        player = load_menu_interactive()
        print("Player:", player)