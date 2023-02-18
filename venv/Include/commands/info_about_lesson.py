import datetime

import rest_db as rest_db
from helpers.regional_datetime import regional_datetime
from commands.how_week import how_week


lesson_type = {
    1: 'Лекция',
    2: 'Практика',
    3: 'Л/р'
}


WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

WEEKTYPES = {
    1: 'над',
    2: 'оба',
    3: 'под'
}

def info_about_lessons(peer_id, tomorrow=None, any_day=None):
    izhevsk_utc_date = regional_datetime(4)
    result = 'Пары на сегодня:\n'
    if tomorrow:
        izhevsk_utc_date += datetime.timedelta(days=1)
        result = 'Пары на завтра:\n'

    num_day = (int)(izhevsk_utc_date.strftime('%w')) - 1 # потому что у америконсов 0 - воскресенье,а 6 - суббота, а нам бы хотелось чтобы 0 - понедельник 6 -воскресенье.

    weekday = WEEKDAYS[num_day]
    week_type = 'под' if how_week(tomorrow=tomorrow, boolean=True) else 'над'

    schedule_on_day = rest_db.get_pairs_on_day(peer_id, weekday, week_type)

    if num_day >= 0 and num_day <= 4:
        if type(schedule_on_day) == list:

            for pair in schedule_on_day:
                result += "Пара №{} {} | {} | {} | {}\n".format(pair['num_pair'], pair['lesson_type'], pair['lesson_name'], pair['teacher'], pair['room'])
            return result
        else:
            return "В расписании нет пар"
    else:
        return "Пар нет, выходные, выдыхай"
