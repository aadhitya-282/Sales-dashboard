import sqlite3
from pathlib import Path

db_path = Path(r"F:\python\sales-dashboard\sales.db")

print("Database path:", db_path.resolve())
print("File exists:", db_path.exists())

if db_path.exists():
    print("File size:", db_path.stat().st_size, "bytes")

    try:
        with sqlite3.connect(db_path) as conn:
            result = conn.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            print("Integrity check:", result)

            tables = conn.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
            """).fetchall()

            print("Tables:", tables)

    except sqlite3.DatabaseError as error:
        print("Database error:", error)
