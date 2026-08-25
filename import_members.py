if __package__:
    from .storage import save_data
    from .diary import write_diary
else:
    from storage import save_data
    from diary import write_diary


def import_members(data, filename):
    """
    Import members from one-member-per-line text file.

    Expected format chosen for this project:
    Name | Phone

    Example:
    Abigail | 09060461720
    """
    imported = 0
    skipped = 0

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

    except FileNotFoundError:
        return 0, 0, f"{filename} was not found."

    for line in lines:
        line = line.strip()

        if not line:
            continue

        parts = line.split("|")

        if len(parts) != 2:
            skipped += 1
            continue

        name = parts[0].strip()
        phone = parts[1].strip()

        if not name or not phone:
            skipped += 1
            continue

        duplicate = any(
            member["phone"] == phone
            for member in data["members"]
        )

        if duplicate:
            skipped += 1
            continue

        member_id = len(data["members"]) + 1

        member = {
            "id": member_id,
            "name": name,
            "phone": phone
        }

        data["members"].append(member)

        write_diary(
            f"Member imported: {name} | Phone: {phone}"
        )

        imported += 1

    save_data(data)

    return imported, skipped, "Import completed."