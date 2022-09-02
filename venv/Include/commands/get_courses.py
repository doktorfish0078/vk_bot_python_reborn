

def get_courses():
    courses = [
        {
            'object':'ФЯиТ',
            'link': 'https://ee.istu.ru/course/view.php?id=413',
            'password':'LINGVA'
        },
        {
            'object': 'СИИ',
            'link': 'https://ee.istu.ru/course/view.php?id=424',
            'password': 'Б19-782-2'
        },
        {
            'object': '1С',
            'link': 'https://vk.com/asoiu_b782_2_2019',
            'password': '-'
        },
    ]

    result = ''
    for course in courses:
        result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(course['object'],course['link'],course['password'])

    return result
