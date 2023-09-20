from rest_db import get_all_courses, delete_course, add_new_course

def create_new_course(chat_id, title, link, password):
    try:
        add_new_course(chat_id, title, link, password)
        return 1
    except BaseException as error:
        print(error)
        return None

def delete_course_func(chat_id, index_course):
    try:
        courses = get_all_courses(chat_id)
        if courses != -1:
            ids = list(courses.keys())
            course_id = ids[index_course]
            delete_course(chat_id, course_id)
        else:
            return None
        return 1
    except BaseException as error:
        print(error)
        return None