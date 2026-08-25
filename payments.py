from datetime import datetime

if __package__:
    from .storage import save_data
    from .diary import write_diary
else:
    from storage import save_data
    from diary import write_diary


def find_member(data, member_id):
    """Find a member using their ID."""
    for member in data["members"]:
        if member["id"] == member_id:
            return member

    return None


def record_payment(data, member_id, amount, month):
    """Record a payment made by a member."""
    member = find_member(data, member_id)

    if member is None:
        return False, "Member not found."

    try:
        amount = float(amount)
    except ValueError:
        return False, "Amount must be a valid number."

    if amount <= 0:
        return False, "Amount must be greater than zero."

    month = month.strip()

    if not month:
        return False, "Month cannot be empty."

    payment = {
        "member_id": member_id,
        "amount": amount,
        "month": month,
        "recorded_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data["payments"].append(payment)

    save_data(data)

    write_diary(
        f"Payment recorded: {member['name']} | "
        f"Amount: ₦{amount:.2f} | Month: {month}"
    )

    return True, "Payment recorded successfully."


def show_payment_history(data, member_id):
    """Display everything a member has ever paid."""
    member = find_member(data, member_id)

    if member is None:
        print("Member not found.")
        return

    print(f"\nPAYMENT HISTORY FOR {member['name']}")
    print("-" * 50)

    history = [
        payment
        for payment in data["payments"]
        if payment["member_id"] == member_id
    ]

    if not history:
        print("No payments recorded for this member.")
        return

    total = 0

    for payment in history:
        print(
            f"Month: {payment['month']} | "
            f"Amount: ₦{payment['amount']:.2f} | "
            f"Recorded on: {payment['recorded_on']}"
        )

        total += payment["amount"]

    print("-" * 50)
    print(f"Total paid: ₦{total:.2f}")


def show_dues_status(data):
    """Show who has paid up and who is owing."""
    monthly_due = data["monthly_due"]

    if not data["members"]:
        print("No members have been registered yet.")
        return

    print("\nDUES STATUS")
    print("-" * 60)

    for member in data["members"]:
        member_payments = [
            payment
            for payment in data["payments"]
            if payment["member_id"] == member["id"]
        ]

        total_paid = sum(
            payment["amount"]
            for payment in member_payments
        )

        if total_paid >= monthly_due:
            status = "PAID UP"
            owing = 0
        else:
            status = "OWING"
            owing = monthly_due - total_paid

        print(
            f"{member['name']} | "
            f"Paid: ₦{total_paid:.2f} | "
            f"Owing: ₦{owing:.2f} | "
            f"{status}"
        )


def show_owing_members(data):
    """Display every member who currently owes money."""
    monthly_due = data["monthly_due"]

    if not data["members"]:
        print("No members have been registered yet.")
        return

    owing_list = []

    for member in data["members"]:
        member_payments = [
            payment
            for payment in data["payments"]
            if payment["member_id"] == member["id"]
        ]

        total_paid = sum(payment["amount"] for payment in member_payments)

        if total_paid < monthly_due:
            owing = monthly_due - total_paid
            owing_list.append((member, owing))

    if not owing_list:
        print("\nNo members are currently owing. Everyone is paid up!")
        return

    print("\nMEMBERS CURRENTLY OWING")
    print("-" * 50)

    for member, owing in owing_list:
        print(f"ID: {member['id']} | Name: {member['name']} | Owing: ₦{owing:.2f}")

    print("-" * 50)
    print(f"Total members owing: {len(owing_list)}")