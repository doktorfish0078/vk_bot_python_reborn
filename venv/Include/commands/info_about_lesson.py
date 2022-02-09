lessons = {
    'Понедельник' : {
        1:{
            'week':'under',
            'lesson': {
                'type':'Практика',
                'name':'МиМАПР',
                'teacher':'Исенбаева E.Н.',
                'room':'3-609a'
            }
        },
        2:{ 'week':'both',
            'lesson':{
                'type':'Лекция',
                'name':'СиТ',
                'teacher':'Коробейников А.А.',
                'room':'3-2'
            }
        },
        3:{
            'week':'over',
            'lesson':{
                'type':'Л/р',
                'name':'МиМАПР',
                'teacher':'Исупов Н.С.',
                'room':'3-602'
            }
        },
        4:{
            'week':'over',
            'lesson':{
                'type':'Л/р',
                'name':'МиМАПР',
                'teacher':'Исупов Н.С.',
                'room':'3-602'
            }
        },
    },
    'Вторник' : {
        1:{
            'week':'both',
            'lesson':{
                'type':'Лекция',
                'name':'СиТ',
                'teacher':'Коробейников А.А.',
                'room':'3-2'
        },
    },
    'Среда' : [

    ],
    'Четверг' : [

    ],
    'Пятница' : [

    ]
    }


def info_about_lessons(tomorrow=False):
    day = 'Понедельник'
    week= 'under'
    for key in lessons[day]:
        if(lessons[day][key]['week'] == week or lessons[day][key]['week'] == 'both'):
            print(lessons[day][key])

info_about_lessons()