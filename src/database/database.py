import sqlite3
import os


class DB:
    def __init__(self, DB_PATH):
        self.DB_PATH = DB_PATH
        self.con = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cur = self.con.cursor()

    def init_db(self):
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    light REAL,
                    temp REAL,
                    pressure REAL,
                    humidity REAL
                )
            """)

        self.con.commit()

    def save_reading(self, data):
        self.cur.execute(
            "INSERT INTO readings (light, temp, pressure, humidity) VALUES (?, ?, ?, ?)",
            (
                data.get("light", 0.00),
                data.get("temp", 0.00),
                data.get("pressure", 0.00),
                data.get("humidity", 0.00),
            ),
        )

        self.con.commit()

    def cleanup_old_readings(self):
        self.cur.execute("""
            DELETE FROM readings
            WHERE id NOT IN (
                SELECT id FROM readings
                ORDER BY timestamp DESC
                LIMIT 3600
            )
            """)

        self.con.commit()

    def get_readings(self):
        self.cur.execute("""
                SELECT * FROM readings
                ORDER BY timestamp
                DESC LIMIT 3600
            """)
        r = self.cur.fetchall()

        return r


DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "database", "flowerpi.db")
)
db = DB(DB_PATH)
db.init_db()
