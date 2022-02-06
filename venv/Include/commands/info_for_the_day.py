import os
import sys
import datetime

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from commands.weather import weather
from commands.how_week import how_week

def info_for_the_day(tomorrow = False):
    izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)

    if tomorrow:
        timedelta = datetime.timedelta(days=1)
        return "📅Завтра {0}📅,\n{1},\n{2}".format(izhevsk_utc_date.date() + timedelta, how_week(tomorrow=True), weather(tomorrow=True)[0])
    else:
        return "📅Сегодня {0}📅,\n{1},\n{2}".format(izhevsk_utc_date.date(), how_week(), weather()[0])
