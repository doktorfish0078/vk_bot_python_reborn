import datetime
import json
import os

fin = "Шмотки в ранец и домой"
aft = "Не пожрал = посасал, пиздуй на пары (домой)"
fin_time_dist = 2
couples_dict_buffer = None

def schedule():
    global couples_dict_buffer
    if couples_dict_buffer is None:
        couples_dict_buffer = json.loads(str(open(r'commands/couples.json', "rb").read().decode('utf-8-sig')))
    return couples_dict_buffer

def time_between(curr_time, start, finish):
    return start <= curr_time < finish

def to_minutes(hours, minutes):
    return hours * 60 + minutes

def check_couple(curr_time, start, finish, num):
    if time_between(curr_time, start, finish):
        time_dist = finish - curr_time
        return str(num) + '-я пара ' + ('(пиздец)' if num == 1 else '') + ' до конца: {0}ch {1}m'.format(time_dist//60, time_dist%60) if time_dist > fin_time_dist else fin
    return False

def couple(how_week):
    izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    curr_time = izhevsk_utc_date.hour * 60 + izhevsk_utc_date.minute

    times = [to_minutes(8, 30), to_minutes(10, 0), to_minutes(11, 40), to_minutes(12, 20), to_minutes(13, 50), to_minutes(15, 30), to_minutes(17, 10), to_minutes(18, 50)]

    for i in range(len(times) - 1):
        buf = check_couple(curr_time, times[i], times[i + 1], i + 1)
        if buf:
            shed = schedule()
            j = 0 if how_week else 1
            while j < len(shed):
                if shed[j].get('Pair') == str(i + 1):
                    buf += ('\n' + (shed[j].get('Info') if not (shed[j].get('Info') is None) else 'Пар по расписанию нету :)'))
                    return buf
                j += 2
    return 'Какая бля пара, дура4ёк?)?)?)? Пар нет, универ адыхает, иди домой.'
