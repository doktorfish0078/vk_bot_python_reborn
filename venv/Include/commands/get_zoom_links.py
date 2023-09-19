import Include.rest_db as rest_db

def get_zoom_links(peer_id, enumerate_list=False):
    links = rest_db.get_all_links(peer_id)

    result = ''
    if type(links) != dict:
        return "Ссылок не найдено"

    if not enumerate_list:
        for key, value in links.items():
            result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(value['title'], value['link'], value['password'])
    else:
        counter = 1
        for key, value in links.items():
            result += '{}. {}\nСсылка: {}\nПароль: {}\n'.format(counter, value['title'], value['link'], value['password'])
            counter += 1

    return result
