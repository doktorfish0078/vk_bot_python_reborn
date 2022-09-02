

def get_zoom_links():
    links = [
        # {
        #     'object':'МиМАПР',
        #     'link': 'https://us04web.zoom.us/j/120200433?pwd=bEtxYzVoZTRrdFpPdjF3UTJ5TjB2Zz09',
        #     'password':'9EByKr'
        # },
    ]

    result = ''
    for link in links:
        result += '😶{}\nСсылка: {}\nПароль: {}\n'.format(link['object'],link['link'],link['password'])

    return result if result else "Нет актуальных ссылок"
