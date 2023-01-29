from helpers.regional_datetime import regional_datetime

def print_report(report, delta_hours = 4):
    print("{}: {}".format(regional_datetime(delta_hours=delta_hours), report))