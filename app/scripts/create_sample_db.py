import sqlite3
from pathlib import Path


DATABASE = Path("data/sample.db")

DATABASE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

connection = sqlite3.connect(DATABASE)

connection.execute(
    """
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        region TEXT NOT NULL,
        product TEXT NOT NULL,
        revenue REAL NOT NULL
    )
    """
)

connection.execute(
    "DELETE FROM sales"
)

rows = [
    ("West", "Platform", 125000),
    ("East", "Platform", 98000),
    ("South", "Analytics", 76000),
    ("West", "Analytics", 88000),
    ("North", "Platform", 67000),
    ("East", "Analytics", 92000),
]

connection.executemany(
    """
    INSERT INTO sales (
        region,
        product,
        revenue
    )
    VALUES (?, ?, ?)
    """,
    rows,
)

connection.commit()
connection.close()

print(
    f"Created sample database: {DATABASE}"
)
