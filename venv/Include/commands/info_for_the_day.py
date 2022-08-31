import os
import sys
import datetime

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from commands.weather import weather
from commands.how_week import how_week
from commands.info_about_lesson import info_about_lessons

def info_for_the_day(tomorrow = False):
    izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)

    if tomorrow:
        timedelta = datetime.timedelta(days=1)
        return "📅Завтра {0}📅,\n{1},\n\n{2}\n\n{3}\n".format(izhevsk_utc_date.date() + timedelta, how_week(tomorrow=True), info_about_lessons(tomorrow=True), weather(tomorrow=True)[0])
    else:
        return "📅Сегодня {0}📅,\n{1},\n\n{2}\n\n{3}\n".format(izhevsk_utc_date.date(), how_week(),info_about_lessons(), weather()[0])
