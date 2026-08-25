CHAIRMAN ADE'S MONEY BOOK
==========================

WHAT THIS IS
------------
A program for the chairman of a housing estate residents' association
to register members, record their monthly dues payments, see who is
paid up and who is owing, and look up any member's full payment
history. Everything is saved to disk automatically, so closing the
program and reopening it the next day does not lose anything.


FOLDER STRUCTURE
-----------------
Estate-due-tracker/
|
|-- main.py                          <- RUN THIS FILE. Shows the menu,
|                                        nothing else.
|-- README.txt                        <- this file
|-- README.md                         <- same information, in Markdown
|
|-- Backend_first_official_project/    <- the package. All real logic
      |                                   lives here.
      |-- __init__.py                 marks the folder as a package and
      |                                re-exports the functions main.py
      |                                needs
      |-- storage.py                  reads/writes money_book_data.json,
      |                                handles a missing or corrupted
      |                                data file safely, and creates
      |                                dated backups
      |-- members.py                  registering members, looking
      |                                members up, displaying the list
      |-- payments.py                 recording payments, working out
      |                                who owes what, who is paid up,
      |                                and who is currently owing
      |-- diary.py                    writes the plain-text diary the
      |                                chairman can read himself - one
      |                                line per event
      |-- import_members.py           bulk-imports members from a text
                                       file, skipping badly formatted
                                       lines rather than crashing

Created automatically the first time you run the program (not included
to begin with):
  - money_book_data.json               the actual saved records
  - money_book_diary.txt               the plain-text diary
  - money_book_backup_*.json           dated snapshots (option 6)
  - money_book_corrupt_*.json          only appears if the data file is
                                        ever found damaged - the broken
                                        copy is preserved here rather
                                        than thrown away


HOW TO RUN IT
-------------
Open a terminal in the Estate-due-tracker folder (the one this file is
in - the same folder as main.py) and run:

    python main.py

That's it. Do not run any of the files inside
Backend_first_official_project/ directly - they are building blocks for
main.py, not programs on their own.

The very first time you run it, there is no data file yet - the
program notices this itself and starts with an empty money book.
Nothing needs to be set up beforehand.


THE MENU
--------
1. Register new member
2. View members
3. Record payment
4. View member payment history
5. View dues status
6. Backup records
7. View members owing
8. Import members
9. Exit


WHAT HAPPENS IF THE DATA FILE GETS DAMAGED
--------------------------------------------
If money_book_data.json is ever edited by hand, corrupted, or otherwise
unreadable, the program will NOT crash. It will:
  1. Rename the damaged file to money_book_corrupt_<timestamp>.json so
     nothing is silently thrown away.
  2. Print a plain-language explanation of what happened.
  3. Start up normally with a fresh, empty money book.


MONTHLY DUES
------------
The monthly due amount is currently fixed at NGN 50,000, set in
storage.py's create_new_data(). A member is considered "paid up" once
their total recorded payments reach this amount.


IMPORTING MEMBERS IN BULK
---------------------------
From the menu, choose "8. Import members" and give it the name of a
text file with one member per line, in this format:

    Name | Phone

For example:

    Abigail | 09060461720
    Ibrahim Musa | 08122223333

Lines that are missing a name, missing a phone number, or duplicate a
phone number that's already registered are skipped and counted,
without stopping the rest of the import.


DESIGN NOTES
------------
main.py contains no business logic - it only imports functions from
the package and calls them from the menu loop. All the real work
(saving, loading, dues calculations, diary writing) lives inside
Backend_first_official_project/.

storage.py is the only module that opens money_book_data.json
directly. Every other module works with the same in-memory `data`
dictionary that main.py loads once at startup and passes around,
which keeps file-handling and corruption recovery in exactly one
place.