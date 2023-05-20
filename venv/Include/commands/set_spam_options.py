import Include.rest_db as rest_db

def set_spam_options(chat_id, weather, week, schedule):
    try:
        rest_db.set_spam_options(chat_id, weather, week, schedule)
        return 1
    except BaseException as error:
        print(error)
        return None