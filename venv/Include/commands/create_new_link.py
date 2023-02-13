import rest_db as rest_db

def create_new_link(chat_id, title, link, password):
    rest_db.add_new_link(chat_id, title, link, password)