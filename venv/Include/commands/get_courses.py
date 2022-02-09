

def get_courses():
    courses = [
        {
            'object':'Физра',
            'link': 'https://ee.istu.ru/course/view.php?id=5357',
            'password':'123'
        },
        {
            'object': 'ГИС',
            'link': 'https://ee.istu.ru/course/view.php?id=4727',
            'password': 'ГИС2022'
        },
        {
            'object': 'ИСи',
            'link': 'https://ee.istu.ru/enrol/index.php?id=409',
            'password': 'Не требуется'
        },
        {
            'object': 'МиМАПР',
            'link': 'https://ee.istu.ru/enrol/index.php?id=181',
            'password': 'MIMAPR16'
        }
    ]

    result = ''
    for course in courses:
        result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(course['object'],course['link'],course['password'])

    return result
