import datetime

def regional_datetime(delta_hours = 0):
    return datetime.datetime.utcnow() + datetime.timedelta(hours=delta_hours)