import os
import sys
import datetime

from commands.weather import weather
from commands.how_week import how_week
from commands.info_about_lesson import info_about_lessons

from helpers.regional_datetime import regional_datetime

import rest_db as rest_db


def info_for_the_day(peer_id, tomorrow = False):
    izhevsk_utc_date = regional_datetime(4)

    if tomorrow:
        timedelta = datetime.timedelta(days=1)
        return "📅Завтра {0}📅,\n{1},\n\n{2}\n\n{3}\n".format(
            izhevsk_utc_date.date() + timedelta,
            how_week(tomorrow=True),
            info_about_lessons(peer_id, tomorrow=True),
            weather(tomorrow=True)[0]
        )
    else:
        return "📅Сегодня {0}📅,\n{1},\n\n{2}\n\n{3}\n".format(
            izhevsk_utc_date.date(),
            how_week(),
            info_about_lessons(peer_id),
            weather()[0]
        )
