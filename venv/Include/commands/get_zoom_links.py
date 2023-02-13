import rest_db as rest_db

def get_zoom_links(peer_id):
    links = rest_db.get_all_links(peer_id)

    result = ''
    if type(links) == dict:
        for key, value in links.items():
            result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(value['title'], value['link'], value['password'])

        return result
    else:
        return "Ссылок не найдено"
