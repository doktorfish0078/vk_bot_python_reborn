import os
import sys
import datetime

from Include.commands.how_week import how_week
from Include.commands.info_about_lesson import info_about_lessons
from Include.commands.weather import weather

from Include.helpers import regional_datetime

import Include.rest_db as rest_db


def info_for_the_day(peer_id, tomorrow = False, spam_options=None):
    izhevsk_utc_date = regional_datetime(4)
    timedelta = datetime.timedelta(days=1)
    if spam_options:
        if tomorrow:
            output_string = "📅Завтра {0}📅,\n".format(izhevsk_utc_date.date() + timedelta)
            if spam_options['week']:
                output_string += "{0}\n".format(how_week(tomorrow=True))
            if spam_options['schedule']:
                output_string += "\n{0}\n".format(info_about_lessons(peer_id, tomorrow=True))
            if spam_options['weather']:
                output_string += "\n{0}\n".format(weather(tomorrow=True)[0])

            return output_string
        else:
            output_string = "📅Сегодня {0}📅,\n".format(izhevsk_utc_date.date())
            if spam_options['week']:
                output_string += "{0}\n".format(how_week())
            if spam_options['schedule']:
                output_string += "\n{0}\n".format(info_about_lessons(peer_id))
            if spam_options['weather']:
                output_string += "\n{0}\n".format(weather()[0])
            return output_string
    else:
        if tomorrow:
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
