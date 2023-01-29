import datetime


class Study_day(object):
    def __init__(self, day_of_the_week):
        self.day_of_the_week = day_of_the_week
        self.lessons = []

class Lesson(object):
    def __init__(self, week, num, type, name, teacher, room):
        self.week = week
        self.num = num
        self.type = type
        self.name = name
        self.teacher = teacher
        self.room = room

week_types = {
    1: 'over',
    2: 'both',
    3: 'under'
}

lesson_type = {
    1: 'Лекция',
    2: 'Практика',
    3: 'Л/р'
}

WEEK = [
    Study_day('понедельник'),
    Study_day('вторник'),
    Study_day('среда'),
    Study_day('четверг'),
    Study_day('пятница')
]

WEEK[0].lessons = [
]

WEEK[1].lessons = [
    Lesson(week_types[1], 4, lesson_type[1], 'Защита информации', 'Стулакина Е.Ф.', '3-7'),
    Lesson(week_types[2], 5, lesson_type[3], 'Программирование мобильных приложений', 'Исупов Н.С.', '3-603а'),
    Lesson(week_types[2], 6, lesson_type[3], 'Программирование мобильных приложений', 'Исупов Н.С.', '3-603а'),
]

WEEK[2].lessons = [
    Lesson(week_types[2], 2, lesson_type[1], 'Проектирование АСОиУ', 'Соболева Н.В.', '3-8'),
    Lesson(week_types[2], 3, lesson_type[1], 'Программирование мобильных приложений', 'Исупов Н.С.', '3-2'),
    Lesson(week_types[1], 4, lesson_type[2], 'НИР', 'Телегина М.В.', '3-609'),
    Lesson(week_types[3], 4, lesson_type[3], 'Защита информации', 'Стулакина Е.Ф.', '7-518'),
    Lesson(week_types[3], 5, lesson_type[3], 'Защита информации', 'Стулакина Е.Ф.', '7-518'),
]

WEEK[3].lessons = [
    Lesson(week_types[2], 1, lesson_type[3], 'Проектирование АСОиУ', 'Соболева Н.В.', '3-603а'),
    Lesson(week_types[2], 2, lesson_type[3], 'Проектирование АСОиУ', 'Соболева Н.В.', '3-603а'),
    Lesson(week_types[2], 3, lesson_type[2], 'Защита информации', 'Стулакина Е.Ф.', '7-518'),

]

WEEK[4].lessons = [
    Lesson(week_types[2], 4, lesson_type[2], 'Проектирование АСОиУ', 'Соболева Н.В.', '3-603'),
    Lesson(week_types[2], 5, lesson_type[2], 'Программирование мобильных приложений', 'Исупов Н.С.', '3-609а'),
]

def info_about_lessons(tomorrow=False, any_day=False):
    izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    result = 'Пары на сегодня:\n'
    if tomorrow:
        izhevsk_utc_date += datetime.timedelta(days=1)
        result = 'Пары на завтра:\n'

    num_day = (int)(izhevsk_utc_date.strftime('%w')) - 1 # потом что 0 - воскресение,а 6 - суббота.
    num_week = izhevsk_utc_date.strftime('%W')

    week = 'under' if ((int)(num_week) % 2 == 0) else 'over'

    if num_day >= 0 and num_day <= 4:
        if len(WEEK[num_day].lessons) == 0:
            return "Пар нет, кайфуулли"

        for lesson in WEEK[num_day].lessons:
            if(lesson.week == week or lesson.week == 'both'):
                result += "Пара №{} {} | {} | {} | {}\n".format(lesson.num, lesson.type, lesson.name, lesson.teacher, lesson.room)
        return result
    else:
        return "Пар нет, кайфуулли"
