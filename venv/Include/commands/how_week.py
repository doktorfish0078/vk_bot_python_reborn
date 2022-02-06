import datetime
#even - under/ odd - over line
def how_week(tomorrow = False):
    offset = datetime.timedelta(hours=4)
    current_date = datetime.datetime.utcnow() + offset
    if tomorrow:
        current_date += datetime.timedelta(days=1)
    num_week = current_date.strftime('%W')
    
    return '👇Неделя под чертой👇' if ((int)(num_week) % 2 == 0) else '☝Неделя над чертой☝'
