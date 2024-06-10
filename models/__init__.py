import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        author_id INTEGER,
        magazine_id INTEGER,
        title TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors (id),
        FOREIGN KEY (magazine_id) REFERENCES magazines (id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
