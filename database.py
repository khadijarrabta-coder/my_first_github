import sqlite3

DB_NAME = "langue_qcm.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        score INTEGER DEFAULT 0,
        question_index INTEGER DEFAULT 0,
        niveau TEXT DEFAULT 'A1'
    );

    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        niveau TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS choices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        texte TEXT,
        correct INTEGER,
        FOREIGN KEY(question_id) REFERENCES questions(id)
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Base de données créée")

if __name__ == "__main__":
    init_db()

