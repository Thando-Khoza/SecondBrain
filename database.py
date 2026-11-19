
import sqlite3

def create_database():
    connection = sqlite3.connect("second_brain.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_note(title, content, category, tags):
    connection = sqlite3.connect("second_brain.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO notes (title, content, category, tags)
        VALUES (?, ?, ?, ?)
    """, (title, content, category, tags))

    connection.commit()
    connection.close()


def get_notes():
    connection = sqlite3.connect("second_brain.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()

    connection.close()
    return notes


def search_notes(keyword):
    connection = sqlite3.connect("second_brain.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM notes
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY created_at DESC
    """, (f"%{keyword}%", f"%{keyword}%"))

    notes = cursor.fetchall()

    connection.close()
    return notes


def update_note(note_id, title, content, category, tags):
    connection = sqlite3.connect("second_brain.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE notes
        SET title = ?, content = ?, category = ?, tags = ?
        WHERE id = ?
    """, (title, content, category, tags, note_id))

    connection.commit()
    connection.close()


def delete_note(note_id):
    connection = sqlite3.connect("second_brain.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Second Brain database is ready.")

