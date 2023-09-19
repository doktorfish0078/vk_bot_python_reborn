import Include.rest_db as rest_db

def create_new_course(chat_id, title, link, password):
    try:
        rest_db.add_new_course(chat_id, title, link, password)
        return 1
    except BaseException as error:
        print(error)
        return None

def delete_course(chat_id, index_course):
    try:
        courses = rest_db.get_all_courses(chat_id)
        if courses != -1:
            ids = list(courses.keys())
            course_id = ids[index_course]
            rest_db.delete_course(chat_id, course_id)
        else:
            return None
        return 1
    except BaseException as error:
        print(error)
        return None