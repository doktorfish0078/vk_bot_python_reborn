import Include.rest_db as rest_db

def create_new_event(chat_id, date, time, event_name):
    try:
        rest_db.add_new_event(chat_id, date, time, event_name)
        return 1
    except BaseException as error:
        print(error)
        return None