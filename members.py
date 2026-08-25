if __package__:
    from .storage import save_data
    from .diary import write_diary
else:
    from storage import save_data
    from diary import write_diary


def register_member(data, name, phone):
    """Register a new estate member."""
    name = name.strip()
    phone = phone.strip()

    if not name:
        return False, ("Member name cannot be empty.")

    if any(char.isdigit() for char in name):
        return False, "You cannot enter a number, enter a name."

    if not any(char.isalpha() for char in name):
        return False, "You cannot enter a number, enter a name."

    if not phone:
        return False, ("Phone number cannot be empty.")

    for member in data["members"]:
        if member["phone"] == phone:
            return False, "A member with that phone number already exists, please try again."

    new_id = len(data["members"]) + 1

    member = {
        "id": new_id,
        "name": name,
        "phone": phone
    }

    data["members"].append(member)

    save_data(data)

    write_diary(
        f"New member registered: {name} | Phone: {phone}"
    )

    return True, f"{name} registered successfully. Member ID: {new_id}"


def display_members(data):
    """Display all registered members."""
    if not data["members"]:
        print("No members have been registered yet.")
        return

    print("\nREGISTERED MEMBERS")
    print("-" * 50)

    for member in data["members"]:
        print(
            f"ID: {member['id']} | "
            f"Name: {member['name']} | "
            f"Phone: {member['phone']}"
        )