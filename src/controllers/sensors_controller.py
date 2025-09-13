from src.database.database import DB

db = DB()


def read_sensors():
    r = db.get_readings()

    return r
