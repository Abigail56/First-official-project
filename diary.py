from datetime import datetime


DIARY_FILE = "money_book_diary.txt"


def write_diary(message):
    """Add one timestamped event to the diary."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DIARY_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")