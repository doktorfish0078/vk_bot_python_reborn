from rest_db import set_schedule

def set_schedule(chat_id, schedule):
    try:
        set_schedule(chat_id, schedule)
        return 1
    except BaseException as error:
        print(error)
        return None