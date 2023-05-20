from Include.helpers.regional_datetime import regional_datetime

def print_report(report, traceback=None, delta_hours = 4):
    if traceback:
        print("{}:{}\n{}".format(regional_datetime(delta_hours=delta_hours), report, traceback))
    else:
        print("{}:{}".format(regional_datetime(delta_hours=delta_hours), report))