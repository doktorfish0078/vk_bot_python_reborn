import datetime

from helpers import regional_datetime


#чётн - над / нечётн - под
def how_week(tomorrow = False, boolean = False):
    """

    :param tomorrow: если нужно определить неделю на завтра
    :param boolean: если нужно вернуть в виде bool, true=над, false=под
    :return: текст с описанием какая неделя
    """
    izhevsk_utc_date = regional_datetime(4)


    if tomorrow:
        izhevsk_utc_date += datetime.timedelta(days=1)
    num_week = izhevsk_utc_date.strftime('%W')

    if boolean:
        return int(num_week) % 2 == 0


    if ((int)(num_week) % 2 != 0):
        #Если нечётная
        return '👇Неделя под чертой👇'
    else:
        # Если чётная
        return '☝Неделя над чертой☝'
