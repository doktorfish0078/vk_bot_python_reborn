import Include.rest_db as rest_db

def create_new_link(chat_id, title, link, password):
    try:
        rest_db.add_new_link(chat_id, title, link, password)
        return 1
    except BaseException as error:
        print(error)
        return None

def delete_link(chat_id, index_link):
    try:
        links = rest_db.get_all_links(chat_id)
        if links != -1:
            ids = list(links.keys())
            link_id = ids[index_link]
            rest_db.delete_link(chat_id, link_id)
        else:
            return None
        return 1
    except BaseException as error:
        print(error)
        return None