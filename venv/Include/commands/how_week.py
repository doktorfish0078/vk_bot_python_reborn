import datetime
#even - under / odd - over line
def how_week(tomorrow = False, boolean = False):
    izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    if tomorrow:
        izhevsk_utc_date += datetime.timedelta(days=1)
    num_week = izhevsk_utc_date.strftime('%W')

    if boolean:
        return int(num_week) % 2 == 0
        #up line
    
    return '👇Неделя под чертой👇' if ((int)(num_week) % 2 == 0) else '☝Неделя над чертой☝'
