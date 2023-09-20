from rest_db import add_new_event, get_all_events, delete_event

def create_new_event(chat_id, date, time, event_name):
    try:
        add_new_event(chat_id, date, time, event_name)
        return 1
    except BaseException as error:
        print(error)
        return None

def delete_event(chat_id, index_event):
    try:
        events = get_all_events(chat_id)
        if events != -1:
            ids = list(events.keys())
            event_id = ids[index_event]
            delete_event(chat_id, event_id)
        else:
            return None
        return 1
    except BaseException as error:
        print(error)
        return None