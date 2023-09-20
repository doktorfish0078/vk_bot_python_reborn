from rest_db import get_all_courses

def get_courses(peer_id, enumerate_list=False):
    """
    :param peer_id:
    :return:
    """
    courses = rest_db.get_all_courses(peer_id)
    result = ''
    if type(courses) != dict:
        return "Курсов не найдено"

    if not enumerate_list:
        for key, value in courses.items():
            result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(value['title'], value['link'], value['password'])
    else:
        counter = 1
        for key, value in courses.items():
            result += '{}. {}\nСсылка: {}\nПароль: {}\n'.format(counter, value['title'], value['link'], value['password'])
            counter += 1

    return result
