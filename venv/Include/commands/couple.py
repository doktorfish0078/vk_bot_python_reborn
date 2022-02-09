import datetime

def time_between(curr_time, start, finish):
    return start <= curr_time < finish

def to_minutes(hours, minutes):
    return hours * 60 + minutes

def couple():
    izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    curr_time = izhevsk_utc_date.hour * 60 + izhevsk_utc_date.minute
    fin = "Шмотки в ранец и домой"
    aft = "Не пожрал = посасал, пиздуй на пары (домой)"
    fin_time_dist = 2
    if time_between(curr_time, to_minutes(8, 30), to_minutes(10, 0)):
        time_dist = to_minutes(10, 0) - curr_time
        return '1-я пара (пиздец) до конца: {0}ch {1}m'.format(time_dist//60, time_dist%60) if time_dist > fin_time_dist else fin

    elif time_between(curr_time, to_minutes(10, 10), to_minutes(11, 40)):
        time_dist = to_minutes(11, 40) - curr_time
        return '2-я пара до конца: {0}ch {1}m'.format(time_dist//60, time_dist%60) if time_dist > fin_time_dist else fin

    elif time_between(curr_time, to_minutes(11, 40), to_minutes(12, 20)):
        time_dist = to_minutes(12, 20) - curr_time
        return 'Приятного аппетита, до конца обеда: {0}ch {1}m'.format(time_dist//60, time_dist%60)  if time_dist > fin_time_dist else aft

    elif time_between(curr_time, to_minutes(12, 20), to_minutes(13, 50)):
        time_dist = to_minutes(13, 50) - curr_time
        return '3-я пара до конца: {0}ch {1}m'.format(time_dist//60, time_dist%60) if time_dist > fin_time_dist else fin

    elif time_between(curr_time, to_minutes(14, 0), to_minutes(15, 30)):
        time_dist = to_minutes(15, 30) - curr_time
        return '4-я пара до конца: {0}ch {1}m'.format(time_dist//60, time_dist%60) if time_dist > fin_time_dist else fin

    elif time_between(curr_time, to_minutes(15, 40), to_minutes(17, 10)):
        time_dist = to_minutes(17, 10) - curr_time
        return '5-я пара до конца: {0}ch {1}m'.format(time_dist//60, time_dist%60) if time_dist > fin_time_dist else fin

    elif time_between(curr_time, to_minutes(17, 20), to_minutes(18, 50)):
        time_dist = to_minutes(18, 50) - curr_time
        return '6-я пара (дембель) до конца: {0}ch {1}m'.format(time_dist//60, time_dist%60) if time_dist > fin_time_dist else fin

    else :
        return 'Какая бля пара, дура4ёк?)?)?)? Пар нет, универ адыхает, иди домой.'
