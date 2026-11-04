import sqlite3

conn = sqlite3.connect(
    "career.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS analysis(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT
)
""")

conn.commit()


def save_result(result):

    cursor.execute(
        "INSERT INTO analysis(result) VALUES(?)",
        (result,)
    )

    conn.commit()


def save_chat(question, answer):

    cursor.execute(
        """
        INSERT INTO chat_history(
            question,
            answer
        )
        VALUES(?,?)
        """,
        (question, answer)
    )

    conn.commit()


def get_chat_history():

    cursor.execute(
        """
        SELECT question, answer
        FROM chat_history
        ORDER BY id DESC
        LIMIT 10
        """
    )

    return cursor.fetchall()