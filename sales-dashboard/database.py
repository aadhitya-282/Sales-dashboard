import sqlite3
from pathlib import Path
import pandas as pd

# Store the database in the same folder as this Python file
DB_PATH = Path(__file__).with_name("sales.db")


def initialize_database():
    """Create the sales table and insert sample data if empty."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sales (
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

        count = conn.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        if count == 0:
            sample_data = [
                (1001, "2025-01-05", "Asha", "Laptop",
                 "Electronics", "South", 1, 65000, 52000),

                (1002, "2025-01-12", "Rahul", "Headphones",
                 "Electronics", "West", 2, 2500, 1500),

                (1003, "2025-01-20", "Meera", "Office Chair",
                 "Furniture", "South", 3, 7000, 4800),

                (1004, "2025-02-03", "Arjun", "Desk",
                 "Furniture", "North", 2, 12000, 8500),

                (1005, "2025-02-15", "Asha", "Keyboard",
                 "Electronics", "South", 4, 1800, 900),

                (1006, "2025-02-22", "Priya", "Notebook",
                 "Stationery", "East", 20, 80, 35),

                (1007, "2025-03-02", "Rahul", "Monitor",
                 "Electronics", "West", 2, 15000, 12000),

                (1008, "2025-03-10", "Meera", "Bookshelf",
                 "Furniture", "North", 1, 9000, 6500),

                (1009, "2025-03-18", "Priya", "Pen Set",
                 "Stationery", "East", 15, 150, 60),

                (1010, "2025-04-05", "Arjun", "Laptop",
                 "Electronics", "North", 2, 65000, 52000),

                (1011, "2025-04-14", "Asha", "Desk",
                 "Furniture", "South", 1, 12000, 8500),

                (1012, "2025-04-25", "Rahul", "Notebook",
                 "Stationery", "West", 30, 80, 35)
            ]

            conn.executemany("""
                INSERT INTO sales (
                    order_id, order_date, customer_name,
                    product_name, category, region,
                    quantity, unit_price, unit_cost
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sample_data)


def load_sales():
    """Load sales data and calculate revenue, cost, and profit."""

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM sales ORDER BY order_date",
            conn
        )

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["cost"] = df["quantity"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]

    return df
