import Include.rest_db as rest_db

def create_new_course(chat_id, title, link, password):
    try:
        rest_db.add_new_course(chat_id, title, link, password)
        return 1
    except BaseException as error:
        print(error)
        return None