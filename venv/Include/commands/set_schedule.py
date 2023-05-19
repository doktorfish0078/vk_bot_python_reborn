import rest_db as rest_db

def set_schedule(chat_id, schedule):
    try:
        rest_db.set_schedule(chat_id, schedule)
        return 1
    except BaseException as error:
        print(error)
        return None