# database.py
import sqlite3
import os

DB_PATH = "logs/files.db"

def init_db():
    os.makedirs("logs", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filetype TEXT,
        hash TEXT,
        status TEXT,
        user_id INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def log_scan(filename, filetype, filehash, status, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO scans (filename, filetype, hash, status, user_id) VALUES (?, ?, ?, ?, ?)",
              (filename, filetype, filehash, status, user_id))
    conn.commit()
    conn.close()
