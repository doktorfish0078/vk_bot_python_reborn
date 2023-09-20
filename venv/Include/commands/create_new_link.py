from rest_db import add_new_link, get_all_links, delete_link

def create_new_link(chat_id, title, link, password):
    try:
        add_new_link(chat_id, title, link, password)
        return 1
    except BaseException as error:
        print(error)
        return None

def delete_link(chat_id, index_link):
    try:
        links = get_all_links(chat_id)
        if links != -1:
            ids = list(links.keys())
            link_id = ids[index_link]
            delete_link(chat_id, link_id)
        else:
            return None
        return 1
    except BaseException as error:
        print(error)
        return None