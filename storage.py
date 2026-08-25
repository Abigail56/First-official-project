import json
import os
from datetime import datetime


DATA_FILE = "money_book_data.json"


def create_new_data():
    """Create a fresh empty money book."""
    return {
        "monthly_due": 50000,
        "members": [],
        "payments": []
    }


def validate_data(data):
    """Check whether saved data has the expected structure."""
    if not isinstance(data, dict):
        return False

    if "monthly_due" not in data:
        return False

    if "members" not in data or not isinstance(data["members"], list):
        return False

    if "payments" not in data or not isinstance(data["payments"], list):
        return False

    return True


def load_data():
    """
    Load saved records.

    If no record exists, start with a fresh money book.
    If the file is corrupted, preserve it and start safely.
    """
    if not os.path.exists(DATA_FILE):
        return create_new_data(), "new"

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not validate_data(data):
            raise ValueError("Invalid data structure.")

        return data, "loaded"

    except (json.JSONDecodeError, ValueError, OSError):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        damaged_file = f"money_book_corrupt_{timestamp}.json"

        try:
            os.rename(DATA_FILE, damaged_file)
        except OSError:
            pass

        return create_new_data(), "corrupt"


def save_data(data):
    """Save the money book to disk."""
    temporary_file = DATA_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    os.replace(temporary_file, DATA_FILE)


def backup_data(data):
    """Create a dated copy of the current records."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"money_book_backup_{timestamp}.json"

    with open(backup_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return backup_file