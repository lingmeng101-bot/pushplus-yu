import sqlite3
import config

SCHEMA = """
    CREATE TABLE IF NOT EXISTS YU(
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    day TEXT,
    title TEXT NOT NULL,
    content TEXT,
    access_status TEXT DEFAULT 'normal',
    pushed INTEGER DEFAULT 0,
    UNIQUE(url))"""
def init_db():
    conn = sqlite3.connect(config.DB_NAME)
    c = conn.cursor()
    c.execute(SCHEMA)
    conn.commit()
    return conn

def link_exists(conn: sqlite3.Connection, url: str) -> bool:
    c = conn.cursor()

    c.execute(
        "SELECT 1 FROM YU WHERE url=? AND access_status NOT IN (?, ?) LIMIT 1",
        (url, 'malformed', 'no_content')
    )
    exists = c.fetchone() is not None
    return exists

def save_yu(conn: sqlite3.Connection,
            url: str,
            day: str,
            title: str,
            content: str,
            access_status: str) -> None:
    c = conn.cursor()

    c.execute("""
        INSERT INTO YU (url, day, title, content, access_status) 
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            content = excluded.content,
            access_status = excluded.access_status,
            day = excluded.day,
            title = excluded.title
    """, (url, day, title, content, access_status))

def get_unpushed(conn):

    c = conn.cursor()
    c.execute("""
        SELECT id, title, url, day FROM YU
        WHERE access_status IN ('normal', 'restricted')
          AND pushed = 0
        ORDER BY id DESC
    """)
    return c.fetchall()

def mark_pushed(conn, notice_id):

    c = conn.cursor()
    c.execute("UPDATE YU SET pushed = 1 WHERE id = ?", (notice_id,))
    conn.commit()

def commit_db(conn: sqlite3.Connection) -> None:
    conn.commit()
