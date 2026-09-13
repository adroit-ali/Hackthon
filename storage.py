"""
Persistent JSON storage module for HackOps.
Provides real-time file-based shared state across multiple concurrent users and sessions.
"""

import json
import os
import time
from typing import Any, Dict, List, Optional
from mock_data import MOCK_PARTICIPANTS, MOCK_PROJECT

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "hackops_storage.json")


def get_default_seed() -> Dict[str, Any]:
    """Create initial seed data from mock data with 1 Leader and multiple Members."""
    participants = []
    for i, p in enumerate(MOCK_PARTICIPANTS):
        item = dict(p)
        if i == 0:
            item["role"] = "leader"
            item["project_idea"] = MOCK_PROJECT.strip()
        else:
            item["role"] = "member"
        participants.append(item)

    return {
        "participants": participants,
        "result": None,
        "step": 1,
        "selected_team_idx": 0,
        "last_updated": time.time()
    }


def ensure_storage_initialized() -> Dict[str, Any]:
    """Ensure data directory and JSON file exist, seeding once if missing."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        seed = get_default_seed()
        save_storage(seed)
        return seed

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or "participants" not in data:
                seed = get_default_seed()
                save_storage(seed)
                return seed
            return data
    except Exception as e:
        print(f"Error loading storage file ({e}), re-seeding default data.")
        seed = get_default_seed()
        save_storage(seed)
        return seed


def load_storage() -> Dict[str, Any]:
    """Load latest shared persistent state directly from JSON file."""
    return ensure_storage_initialized()


def save_storage(data: Dict[str, Any]) -> None:
    """Save state dictionary to JSON file with atomic-like write and timestamp."""
    os.makedirs(DATA_DIR, exist_ok=True)
    data["last_updated"] = time.time()
    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    if os.path.exists(DATA_FILE):
        try:
            os.replace(temp_file, DATA_FILE)
        except Exception:
            os.remove(DATA_FILE)
            os.rename(temp_file, DATA_FILE)
    else:
        os.rename(temp_file, DATA_FILE)


def add_participant_to_storage(participant: Dict[str, Any]) -> Dict[str, Any]:
    """Add a participant directly to shared persistent storage."""
    data = load_storage()
    data.setdefault("participants", []).append(participant)
    save_storage(data)
    return data


def remove_participant_from_storage(index: int) -> Dict[str, Any]:
    """Remove a participant by index directly from shared persistent storage."""
    data = load_storage()
    participants = data.get("participants", [])
    if 0 <= index < len(participants):
        participants.pop(index)
        data["participants"] = participants
        save_storage(data)
    return data


def save_result_to_storage(result: Any, step: int = 2) -> Dict[str, Any]:
    """Save AI matching result to shared persistent storage."""
    data = load_storage()
    data["result"] = result
    data["step"] = step
    save_storage(data)
    return data


def reset_storage() -> Dict[str, Any]:
    """Reset persistent storage back to clean initial seed data."""
    seed = get_default_seed()
    save_storage(seed)
    return seed


def get_storage_last_modified() -> float:
    """Return the last modified timestamp of the storage file."""
    if os.path.exists(DATA_FILE):
        return os.path.getmtime(DATA_FILE)
    return 0.0
