import sqlite3


class DB:
    def __init__(self, DB_PATH):
        self.DB_PATH = DB_PATH

    def init_db(self):
        with sqlite3.connect(self.DB_PATH) as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    light REAL,
                    temp REAL
                )
            """)
            con.commit()

    def save_reading(self, data):
        with sqlite3.connect(self.DB_PATH) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO readings (light, temp) VALUES (?, ?)",
                (data.get("light", 0.00), data.get("temp", 0.00)),
            )
            con.commit()
