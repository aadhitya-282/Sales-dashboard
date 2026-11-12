from pathlib import Path
import sqlite3

db_path = Path(r"F:\python\sales-dashboard\sales.db")

# Create a brand-new SQLite database
with sqlite3.connect(db_path) as conn:
    conn.execute("""
        CREATE TABLE sales (
            order_id INTEGER PRIMARY KEY,
            order_date TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            region TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            unit_cost REAL NOT NULL
        )
    """)

    print("SUCCESS: New SQLite database created!")
    print("Tables:", conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall())

print("Database file:", db_path)
