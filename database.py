import sqlite3

DB_PATH = "expenses.db"

def init_db(db_path: str = DB_PATH) -> None:
    """Create the expenses table if it doesn't exist yet."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        amount INTEGER,
        category TEXT,
        confidence TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )"""

    cursor.execute(sql)

    conn.commit()
    conn.close()

def save_expense(description: str, amount: int, category: str, confidence: str, db_path: str = DB_PATH) -> None:
    """Insert one expense record into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """INSERT INTO expenses(description, amount, category, confidence)
    VALUES (?, ?, ?, ?)"""

    cursor.execute(sql, (description, amount, category, confidence))

    conn.commit()
    conn.close()

def get_all_expenses(db_path: str = DB_PATH) -> list[tuple]:
    """Return all expense records."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = "SELECT * FROM expenses"
    cursor.execute(sql)
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_total_by_category(category: str, db_path: str = DB_PATH) -> int:
    """Return the sum of amount for a given category."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """SELECT SUM(amount)
    FROM expenses
    WHERE category = ?"""
    
    cursor.execute(sql, (category,))
    row = cursor.fetchone()
    total = row[0]
    if total is None:
        total = 0

    conn.close()
    return total

def delete_expense(id: int, db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """DELETE FROM expenses
    WHERE id = ?"""

    cursor.execute(sql,(id,))

    conn.commit()
    conn.close()

def update_expense(id:str, category:str, db_path:str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """UPDATE expenses
    SET category = ?
    WHERE id = ?"""

    cursor.execute(sql, (category, id))

    conn.commit()
    conn.close()