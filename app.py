
import sqlite3
import streamlit as st
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Second Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = Path(__file__).parent / "second_brain.db"


# ==========================================
# 2. BLACK AND WHITE DESIGN
# ==========================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #000000 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #000000 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #000000 !important;
}

/* Navigation */
[data-testid="stSidebar"] [role="radiogroup"] label {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
}

/* Dropdowns */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-color: #000000 !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 6px !important;
}

.stButton button p,
.stFormSubmitButton button p {
    color: #FFFFFF !important;
}

/* Statistics */
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 8px;
    padding: 18px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #000000 !important;
}

/* Note cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 8px;
}

/* Dividers */
hr {
    border-color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. DATABASE FUNCTIONS
# ==========================================

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_note(title, content, category, tags):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO notes (title, content, category, tags)
            VALUES (?, ?, ?, ?)
        """, (title, content, category, tags))


def get_notes():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, title, content, category, tags, created_at
            FROM notes
            ORDER BY id DESC
        """).fetchall()


def update_note(note_id, title, content, category, tags):
    with get_connection() as conn:
        conn.execute("""
            UPDATE notes
            SET title = ?,
                content = ?,
                category = ?,
                tags = ?
            WHERE id = ?
        """, (title, content, category, tags, note_id))


def delete_note(note_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,)
        )


# ==========================================
# 4. INITIALISE DATABASE
# ==========================================

create_table()


# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.title("🧠 Second Brain")

    st.caption("YOUR PERSONAL KNOWLEDGE SPACE")

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "My Notes",
            "Create Note",
            "Edit Note"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.caption("PERSONAL KNOWLEDGE MANAGEMENT")

    st.write(
        "Organise your thoughts. "
        "Capture your ideas. "
        "Keep learning."
    )


# ==========================================
# 6. LOAD DATA
# ==========================================

notes = get_notes()

total_notes = len(notes)

category_counts = {}

for note in notes:
    category = note[3] or "Uncategorised"

    category_counts[category] = (
        category_counts.get(category, 0) + 1
    )

total_categories = len(category_counts)


# ==========================================
# 7. DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("Good to see you.")

    st.caption(
        "Welcome to your personal knowledge management workspace."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Notes", total_notes)

    with col2:
        st.metric("Categories", total_categories)

    with col3:
        latest_note = notes[0][1] if notes else "None"
        st.metric("Latest Note", latest_note)

    st.write("")

    st.subheader("Recently Added")

    if notes:

        for note in notes[:5]:

            note_id, title, content, category, tags, created_at = note

            with st.container(border=True):

                st.subheader(title)

                st.caption(
                    f"{category or 'Uncategorised'} | {created_at}"
                )

                preview = content[:200]

                if len(content) > 200:
                    preview += "..."

                st.write(preview)

                if tags:
                    st.caption(f"Tags: {tags}")

    else:

        st.info("Your workspace is empty. Create your first note!")

    st.divider()

    st.subheader("Your Categories")

    if category_counts:

        columns = st.columns(min(len(category_counts), 3))

        for index, (category, count) in enumerate(
            category_counts.items()
        ):

            with columns[index % len(columns)]:
                st.metric(category, f"{count} notes")

    else:

        st.caption("Your categories will appear here.")


# ==========================================
# 8. MY NOTES
# ==========================================

elif page == "My Notes":

    st.title("My Notes")

    st.caption("All your knowledge, organised in one place.")

    st.divider()

    search = st.text_input(
        "Search your notes",
        placeholder="Search titles, content, categories or tags..."
    )

    available_categories = sorted(category_counts.keys())

    selected_category = st.selectbox(
        "Filter by category",
        ["All Categories"] + available_categories
    )

    filtered_notes = []

    for note in notes:

        searchable_text = " ".join(
            str(value or "") for value in note
        ).lower()

        matches_search = search.lower() in searchable_text

        note_category = note[3] or "Uncategorised"

        matches_category = (
            selected_category == "All Categories"
            or note_category == selected_category
        )

        if matches_search and matches_category:
            filtered_notes.append(note)

    st.caption(
        f"Showing {len(filtered_notes)} of {total_notes} notes"
    )

    if not filtered_notes:
        st.info("No notes found.")

    for note in filtered_notes:

        note_id, title, content, category, tags, created_at = note

        with st.container(border=True):

            st.subheader(title)

            st.caption(
                f"{category or 'Uncategorised'} | {created_at}"
            )

            st.write(content)

            if tags:
                st.caption(f"Tags: {tags}")

            if st.button("Delete Note", key=f"delete_{note_id}"):

                delete_note(note_id)

                st.success("Note deleted successfully.")

                st.rerun()


# ==========================================
# 9. CREATE NOTE
# ==========================================

elif page == "Create Note":

    st.title("Create a Note")

    st.caption(
        "Capture an idea, save something you learned "
        "or record an important thought."
    )

    st.divider()

    with st.form("create_note_form"):

        title = st.text_input(
            "Note Title",
            placeholder="Give your note a title..."
        )

        content = st.text_area(
            "Note Content",
            placeholder="Start writing your thoughts...",
            height=220
        )

        category = st.selectbox(
            "Category",
            [
                "Learning",
                "Programming",
                "Ideas",
                "Personal",
                "Work",
                "Other"
            ]
        )

        tags = st.text_input(
            "Tags",
            placeholder="Python, SQL, Learning"
        )

        submitted = st.form_submit_button(
            "Save Note",
            use_container_width=True
        )

        if submitted:

            if title.strip() and content.strip():

                add_note(
                    title.strip(),
                    content.strip(),
                    category,
                    tags.strip()
                )

                st.success("Your note has been saved!")

                st.rerun()

            else:

                st.error("Please enter both a title and content.")


# ==========================================
# 10. EDIT NOTE
# ==========================================

elif page == "Edit Note":

    st.title("Edit a Note")

    st.caption("Update your existing notes.")

    st.divider()

    if not notes:

        st.info("You don't have any notes to edit.")

    else:

        note_options = {
            f"{note[1]} (ID: {note[0]})": note
            for note in notes
        }

        selected_note = st.selectbox(
            "Choose a note",
            list(note_options.keys())
        )

        note = note_options[selected_note]

        with st.form("edit_note_form"):

            title = st.text_input(
                "Note Title",
                value=note[1]
            )

            content = st.text_area(
                "Note Content",
                value=note[2],
                height=220
            )

            category = st.text_input(
                "Category",
                value=note[3] or ""
            )

            tags = st.text_input(
                "Tags",
                value=note[4] or ""
            )

            submitted = st.form_submit_button(
                "Update Note",
                use_container_width=True
            )

            if submitted:

                if title.strip() and content.strip():

                    update_note(
                        note[0],
                        title.strip(),
                        content.strip(),
                        category.strip(),
                        tags.strip()
                    )

                    st.success("Note updated successfully!")

                    st.rerun()

                else:

                    st.error(
                        "Title and content cannot be empty."
                    )

import sqlite3
import streamlit as st
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Second Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = Path(__file__).parent / "second_brain.db"


# ==========================================
# 2. BLACK AND WHITE DESIGN
# ==========================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #000000 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #000000 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #000000 !important;
}

/* Navigation */
[data-testid="stSidebar"] [role="radiogroup"] label {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
}

/* Dropdowns */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-color: #000000 !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 6px !important;
}

.stButton button p,
.stFormSubmitButton button p {
    color: #FFFFFF !important;
}

/* Statistics */
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 8px;
    padding: 18px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #000000 !important;
}

/* Note cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 8px;
}

/* Dividers */
hr {
    border-color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. DATABASE FUNCTIONS
# ==========================================

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_note(title, content, category, tags):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO notes (title, content, category, tags)
            VALUES (?, ?, ?, ?)
        """, (title, content, category, tags))


def get_notes():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, title, content, category, tags, created_at
            FROM notes
            ORDER BY id DESC
        """).fetchall()


def update_note(note_id, title, content, category, tags):
    with get_connection() as conn:
        conn.execute("""
            UPDATE notes
            SET title = ?,
                content = ?,
                category = ?,
                tags = ?
            WHERE id = ?
        """, (title, content, category, tags, note_id))


def delete_note(note_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,)
        )


# ==========================================
# 4. INITIALISE DATABASE
# ==========================================

create_table()


# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.title("🧠 Second Brain")

    st.caption("YOUR PERSONAL KNOWLEDGE SPACE")

    st.divider()

    page = st.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "My Notes",
        "Create Note",
        "Edit Note"
    ],
    key="workspace_navigation",
    label_visibility="visible"
)

    st.divider()

    st.caption("PERSONAL KNOWLEDGE MANAGEMENT")

    st.write(
        "Organise your thoughts. "
        "Capture your ideas. "
        "Keep learning."
    )


# ==========================================
# 6. LOAD DATA
# ==========================================

notes = get_notes()

total_notes = len(notes)

category_counts = {}

for note in notes:
    category = note[3] or "Uncategorised"

    category_counts[category] = (
        category_counts.get(category, 0) + 1
    )

total_categories = len(category_counts)


# ==========================================
# 7. DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("Good to see you.")

    st.caption(
        "Welcome to your personal knowledge management workspace."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Notes", total_notes)

    with col2:
        st.metric("Categories", total_categories)

    with col3:
        latest_note = notes[0][1] if notes else "None"
        st.metric("Latest Note", latest_note)

    st.write("")

    st.subheader("Recently Added")

    if notes:

        for note in notes[:5]:

            note_id, title, content, category, tags, created_at = note

            with st.container(border=True):

                st.subheader(title)

                st.caption(
                    f"{category or 'Uncategorised'} | {created_at}"
                )

                preview = content[:200]

                if len(content) > 200:
                    preview += "..."

                st.write(preview)

                if tags:
                    st.caption(f"Tags: {tags}")

    else:

        st.info("Your workspace is empty. Create your first note!")

    st.divider()

    st.subheader("Your Categories")

    if category_counts:

        columns = st.columns(min(len(category_counts), 3))

        for index, (category, count) in enumerate(
            category_counts.items()
        ):

            with columns[index % len(columns)]:
                st.metric(category, f"{count} notes")

    else:

        st.caption("Your categories will appear here.")


# ==========================================
# 8. MY NOTES
# ==========================================

elif page == "My Notes":

    st.title("My Notes")

    st.caption("All your knowledge, organised in one place.")

    st.divider()

    search = st.text_input(
        "Search your notes",
        placeholder="Search titles, content, categories or tags..."
    )

    available_categories = sorted(category_counts.keys())

    selected_category = st.selectbox(
        "Filter by category",
        ["All Categories"] + available_categories
    )

    filtered_notes = []

    for note in notes:

        searchable_text = " ".join(
            str(value or "") for value in note
        ).lower()

        matches_search = search.lower() in searchable_text

        note_category = note[3] or "Uncategorised"

        matches_category = (
            selected_category == "All Categories"
            or note_category == selected_category
        )

        if matches_search and matches_category:
            filtered_notes.append(note)

    st.caption(
        f"Showing {len(filtered_notes)} of {total_notes} notes"
    )

    if not filtered_notes:
        st.info("No notes found.")

    for note in filtered_notes:

        note_id, title, content, category, tags, created_at = note

        with st.container(border=True):

            st.subheader(title)

            st.caption(
                f"{category or 'Uncategorised'} | {created_at}"
            )

            st.write(content)

            if tags:
                st.caption(f"Tags: {tags}")

            if st.button("Delete Note", key=f"delete_{note_id}"):

                delete_note(note_id)

                st.success("Note deleted successfully.")

                st.rerun()


# ==========================================
# 9. CREATE NOTE
# ==========================================

elif page == "Create Note":

    st.title("Create a Note")

    st.caption(
        "Capture an idea, save something you learned "
        "or record an important thought."
    )

    st.divider()

    with st.form("create_note_form"):

        title = st.text_input(
            "Note Title",
            placeholder="Give your note a title..."
        )

        content = st.text_area(
            "Note Content",
            placeholder="Start writing your thoughts...",
            height=220
        )

        category = st.selectbox(
            "Category",
            [
                "Learning",
                "Programming",
                "Ideas",
                "Personal",
                "Work",
                "Other"
            ]
        )

        tags = st.text_input(
            "Tags",
            placeholder="Python, SQL, Learning"
        )

        submitted = st.form_submit_button(
            "Save Note",
            use_container_width=True
        )

        if submitted:

            if title.strip() and content.strip():

                add_note(
                    title.strip(),
                    content.strip(),
                    category,
                    tags.strip()
                )

                st.success("Your note has been saved!")

                st.rerun()

            else:

                st.error("Please enter both a title and content.")


# ==========================================
# 10. EDIT NOTE
# ==========================================

elif page == "Edit Note":

    st.title("Edit a Note")

    st.caption("Update your existing notes.")

    st.divider()

    if not notes:

        st.info("You don't have any notes to edit.")

    else:

        note_options = {
            f"{note[1]} (ID: {note[0]})": note
            for note in notes
        }

        selected_note = st.selectbox(
            "Choose a note",
            list(note_options.keys())
        )

        note = note_options[selected_note]

        with st.form("edit_note_form"):

            title = st.text_input(
                "Note Title",
                value=note[1]
            )

            content = st.text_area(
                "Note Content",
                value=note[2],
                height=220
            )

            category = st.text_input(
                "Category",
                value=note[3] or ""
            )

            tags = st.text_input(
                "Tags",
                value=note[4] or ""
            )

            submitted = st.form_submit_button(
                "Update Note",
                use_container_width=True
            )

            if submitted:

                if title.strip() and content.strip():

                    update_note(
                        note[0],
                        title.strip(),
                        content.strip(),
                        category.strip(),
                        tags.strip()
                    )

                    st.success("Note updated successfully!")

                    st.rerun()

                else:

                    st.error(
                        "Title and content cannot be empty."
                    )

