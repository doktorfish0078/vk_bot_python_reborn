import Include.rest_db as rest_db

def get_courses(peer_id):
    """
    :param peer_id:
    :return:
    """
    courses = rest_db.get_all_courses(peer_id)
    result = ''
    if type(courses) == dict:
        for key, value in courses.items():
            result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(value['title'],value['link'],value['password'])

        return result
    else:
        return "Курсов не найдено"
