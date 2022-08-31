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
    Study_day('Понедельник'),
    Study_day('Вторник'),
    Study_day('Среда'),
    Study_day('Четверг'),
    Study_day('Пятница'),
    Study_day('Суббота'),
    Study_day('Воскресение')
]

WEEK[0].lessons = [
    Lesson(week_types[3], 2, lesson_type[3], 'Программирование 1С', 'Соловьёва А.Н.', '3-602'),
    Lesson(week_types[1], 3, lesson_type[1], 'Программирование 1С', 'Соловьёва А.Н.', '3-3'),
    Lesson(week_types[3], 3, lesson_type[3], 'Программирование 1С', 'Соловьёва А.Н.', '3-602'),
    Lesson(week_types[3], 4, lesson_type[1], 'Тестирование ПО', 'Шибанова Ю.В.', '3-2'),
    Lesson(week_types[2], 5, lesson_type[1], 'БЖД', 'Николаева Л.С.', '3-1'),
    Lesson(week_types[2], 6, lesson_type[1], 'Основы системного анализа', 'Касаткина Е.В.', '3-216'),
    Lesson(week_types[1], 7, lesson_type[2], 'Основы системного анализа', 'Касаткина Е.В.', '3-603'),
]

WEEK[1].lessons = [
    Lesson(week_types[3], 2, lesson_type[3], 'Цифровая обратобка изображений', 'Севрюгин В.Р.', '3-513б'),
    Lesson(week_types[3], 3, lesson_type[3], 'Цифровая обратобка изображений', 'Севрюгин В.Р.', '3-513б'),
    Lesson(week_types[1], 5, lesson_type[1], 'Цифровая обратобка изображений', 'Севрюгин В.Р.', '3-3'),
    Lesson(week_types[1], 6, lesson_type[2], 'Формальные языки и трансляторы', 'Касимов Д.Р.', '3-609а'),
]

WEEK[2].lessons = [
    Lesson(week_types[1], 3, lesson_type[3], 'Тестирование ПО', 'Шибанова Ю.В.', '3-804'),
    Lesson(week_types[3], 3, lesson_type[2], 'БЖД', 'Николаева Л.С.', '3-705'),
    Lesson(week_types[1], 4, lesson_type[3], 'Тестирование ПО', 'Шибанова Ю.В.', '3-804'),
    Lesson(week_types[3], 4, lesson_type[2], 'Тестирование ПО', 'Шибанова Ю.В.', '3-609'),
    Lesson(week_types[3], 5, lesson_type[3], 'Программирование 1С', 'Соловьёва А.Н.', '3-804'),
    Lesson(week_types[3], 6, lesson_type[3], 'Программирование 1С', 'Соловьёва А.Н.', '3-804'),

]

WEEK[3].lessons = [
    Lesson(week_types[1], 3, lesson_type[1], 'Программирование 1С', 'Соловьёва А.Н.', '3-3'),
    Lesson(week_types[3], 3, lesson_type[2], 'Системы ИИ', 'Мокроусов М.Н.', '3-609а'),
    Lesson(week_types[1], 4, lesson_type[1], 'Системы ИИ', 'Мокроусов М.Н.', '3-3'),
    Lesson(week_types[1], 5, lesson_type[3], 'Формальные языки и трансляторы', 'Касимов Д.Р.', '3-603а'),
]

WEEK[4].lessons = [
    Lesson(week_types[2], 3, lesson_type[1], 'Формальные языки и трансляторы', 'Касимов Д.Р.', '3-216'),
    Lesson(week_types[3], 4, lesson_type[3], 'Системы ИИ', 'Мокроусов М.Н.', '3-505'),
    Lesson(week_types[3], 5, lesson_type[3], 'Системы ИИ', 'Мокроусов М.Н.', '3-505'),
]

def info_about_lessons(tomorrow=False):
    izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    if tomorrow:
        izhevsk_utc_date += datetime.timedelta(days=1)
    num_day = (int)(izhevsk_utc_date.strftime('%w'))
    num_week = izhevsk_utc_date.strftime('%W')

    week = 'under' if ((int)(num_week) % 2 == 0) else 'over'

    result = ''

    for lesson in WEEK[num_day].lessons:
        if(lesson.week == week or lesson.week == 'both'):
            result += "Пара №{} {} | {} | {} | {}\n".format(lesson.num, lesson.type, lesson.name, lesson.teacher, lesson.room)

    return result if result else "Пар нет, кайфуулли"
