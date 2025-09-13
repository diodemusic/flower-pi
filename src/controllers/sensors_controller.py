from src.database.database import db


def read_sensors():
    r = db.get_readings()

    return r
