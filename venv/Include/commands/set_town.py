import rest_db as rest_db

def set_town(chat_id, town):
    try:
        rest_db.set_town(chat_id, town)
        return 1
    except BaseException as error:
        print(error)
        return None