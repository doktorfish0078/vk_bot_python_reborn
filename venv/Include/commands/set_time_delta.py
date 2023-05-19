import rest_db as rest_db


def set_time_delta(chat_id, time_delta):
    try:
        rest_db.set_time_delta(chat_id, time_delta)
        return 1
    except BaseException as error:
        print(error)
        return None
