import os
import sys
import datetime

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from commands.weather import weather
from commands.how_week import how_week

def info_for_the_day(tomorrow = False):
    offset = datetime.timedelta(hours=4)
    now_date_izh = datetime.datetime.utcnow() + offset

    if tomorrow:
        timedelta = datetime.timedelta(days=1)
        return "📅Завтра {0}📅,\n{1},\n{2}".format(now_date_izh.date() + timedelta, how_week(tomorrow=True), weather(tomorrow=True)[0])
    else:
        return "📅Сегодня {0}📅,\n{1},\n{2}".format(now_date_izh.date(), how_week(), weather()[0])

