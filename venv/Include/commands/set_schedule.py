from rest_db import set_schedule as set_schedule_db

def set_schedule(chat_id, schedule):
    try:
        set_schedule_db(chat_id, schedule)
        return 1
    except BaseException as error:
        print(error)
        return None