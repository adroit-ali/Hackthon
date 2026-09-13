"""
Persistent JSON storage module for HackOps.
Automatically seeds default participants once and persists all additions, deletions, and match results across sessions.
"""

import json
import os
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
        "selected_team_idx": 0
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
    """Load current persistent state from JSON file."""
    return ensure_storage_initialized()


def save_storage(data: Dict[str, Any]) -> None:
    """Save state dictionary to JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def reset_storage() -> Dict[str, Any]:
    """Reset persistent storage back to the clean initial seed data."""
    seed = get_default_seed()
    save_storage(seed)
    return seed
