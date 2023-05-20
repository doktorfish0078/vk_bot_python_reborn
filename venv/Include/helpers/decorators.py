import traceback
import time

from Include.helpers.server_notification import print_report


def trying_decorator(func): # стоит перенести куда-то отдельно как инструмент
	count_retries = 2
	def wrapper(*args, **kwargs):
		for attempt_no in range(count_retries):
			try:
				res = func(*args, **kwargs)
				return res
			except Exception as error:
				print_report(f'REST func-{func.__name__} error in attempt №{attempt_no}: {error}', traceback=traceback.format_exc())
				time.sleep(0.1)
				continue
		return None  # Хз что возвращать лучше,если не получилась
	return wrapper