import datetime
#even - under/ odd - over line
def how_week(tomorrow = False):
    offset = datetime.timedelta(hours=4)
    datetime.timezone(offset=offset)
    current_date = datetime.datetime.now(datetime.timezone.utc) + offset
    if tomorrow:
        current_date += datetime.timedelta(days=1)
    num_week = current_date.strftime('%W')
    
    return '👇Неделя под чертой👇' if ((int)(num_week) % 2 == 0) else '☝Неделя над чертой☝'
