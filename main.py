if __package__:
    from .members import register_member, display_members
    from .payments import record_payment, show_payment_history, show_dues_status, show_owing_members
    from .import_members import import_members
    from . import storage

else:
    from members import register_member, display_members
    from payments import record_payment, show_payment_history, show_dues_status, show_owing_members
    from import_members import import_members
    import storage


data, status = storage.load_data()

if status == "new":
    print("Welcome! No previous records were found.")
    print("A new money book has been started.")

elif status == "corrupt":
    print("Sorry, the saved records appear to be damaged.")
    print("The damaged file has been preserved.")
    print("A fresh money book has been started.")


while True:
    print("\n" + "=" * 70)
    print("       CHAIRMAN ADE'S MONEY BOOK")
    print("=" * 70)
    print("1. Register new member")
    print("2. View members")
    print("3. Record payment")
    print("4. View member payment history")
    print("5. View dues status")
    print("6. Backup records")
    print("7. View members owing")
    print("8. Import members")
    print("9. Exit")
    print("=" * 70)

    choice = input("Choose an option: ").strip()

    if choice == "1":
        name = input("Enter member name: ")
        phone = input("Enter phone number: ")

        success, message = register_member(
            data,
            name,
            phone
        )

        print(message)

    elif choice == "2":
        display_members(data)

    elif choice == "3":
        try:
            member_id = int(input("Enter member ID: "))
        except ValueError:
            print("Please enter a valid member ID.")
            continue

        amount = input("Enter amount paid: ₦")
        month = input("Enter month paid for: ")

        success, message = record_payment(
            data,
            member_id,
            amount,
            month
        )

        print(message)

    elif choice == "4":
        try:
            member_id = int(input("Enter member ID: "))
        except ValueError:
            print("Please enter a valid member ID.")
            continue

        show_payment_history(data, member_id)

    elif choice == "5":
        show_dues_status(data)

    elif choice == "6":
        backup_file = storage.backup_data(data)
        print(f"Backup created: {backup_file}")

    elif choice == "7":
        show_owing_members(data)

    elif choice == "8":
        filename = input(
            "Enter filename (e.g. new_members.txt): "
        ).strip()

        imported, skipped, message = import_members(
            data,
            filename
        )

        print(message)
        print(f"Imported: {imported}")
        print(f"Skipped: {skipped}")

    elif choice == "9":
        print("Goodbye, Chairman Ade!")
        break

    else:
        print("Invalid choice. Please select 1-9.")