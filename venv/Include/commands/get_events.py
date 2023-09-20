from rest_db import get_all_events

def get_events(peer_id, enumerate_list=False):
    events = get_all_events(peer_id)

    result = ''
    if type(events) != dict:
        return "Мероприятий не найдено"

    if not enumerate_list:
        for key, event in events.items():
            result += f'Мероприятие "{event["event_name"]}" запланированное на {event["date"]} , которое состоится в {event["time"]}\n'
    else:
        counter = 1
        for key, event in events.items():
            result += f'{counter}. Мероприятие "{event["event_name"]}" запланированное на {event["date"]} , которое состоится в {event["time"]}\n'
            counter += 1

    return result
