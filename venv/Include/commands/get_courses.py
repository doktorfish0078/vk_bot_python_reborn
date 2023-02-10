import Include.rest_db as rest_db

def get_courses(chat_id):
    """
    :param chat_id: < 100000000, event.chat_id возвращает не полный id чата, а урезанный. Полный это 2000000000 + event.chat_id
    :return:
    """
    courses = rest_db.get_all_courses(2000000000 + chat_id)
    result = ''
    if type(courses) == dict:
        for key, value in courses.items():
            result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(value['title'],value['link'],value['password'])

        return result
    else:
        return "Курсов не найдено"
