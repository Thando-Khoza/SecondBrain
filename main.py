
import database


def test_second_brain():

    # 1. Create a new note
    database.add_note(
        "Second Brain Test",
        "Testing all database operations.",
        "Programming",
        "Python, SQLite"
    )

    print("\n1. CREATE: Note added successfully.")

    # 2. Read all notes
    notes = database.get_notes()

    print("\n2. READ: Retrieving notes.")

    for note in notes:
        print(note)

    # Get the ID of the latest test note
    test_note = next(
        note for note in notes
        if note[1] == "Second Brain Test"
    )

    note_id = test_note[0]

    # 3. Search for a note
    results = database.search_notes("Second Brain Test")

    print("\n3. SEARCH: Search completed.")

    for note in results:
        print(note)

    # 4. Update the note
    database.update_note(
        note_id,
        "Updated Second Brain Test",
        "Testing Python, SQL and database management.",
        "Software Development",
        "Python, SQL"
    )

    print("\n4. UPDATE: Note updated successfully.")

    updated_notes = database.get_notes()

    for note in updated_notes:
        if note[0] == note_id:
            print(note)

    # 5. Delete the test note
    database.delete_note(note_id)

    print("\n5. DELETE: Test note deleted successfully.")

    print("\nAll database operations completed.")


if __name__ == "__main__":
    database.create_database()
    test_second_brain()
