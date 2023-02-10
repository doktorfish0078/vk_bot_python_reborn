import os
import sys
import datetime

from Include.commands.weather import weather
from Include.commands.how_week import how_week
from Include.commands.info_about_lesson import info_about_lessons

from Include.helpers.regional_datetime import regional_datetime

def info_for_the_day(tomorrow = False):
    izhevsk_utc_date = regional_datetime(4)

    if tomorrow:
        timedelta = datetime.timedelta(days=1)
        return "📅Завтра {0}📅,\n{1},\n\n{2}\n\n{3}\n".format(izhevsk_utc_date.date() + timedelta, how_week(tomorrow=True), info_about_lessons(tomorrow=True), weather(tomorrow=True)[0])
    else:
        return "📅Сегодня {0}📅,\n{1},\n\n{2}\n\n{3}\n".format(izhevsk_utc_date.date(), how_week(),info_about_lessons(), weather()[0])
