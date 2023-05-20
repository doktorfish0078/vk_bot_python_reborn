import firebase_admin
from firebase_admin import credentials, db, firestore
import json
import traceback
import time

from Include.helpers import print_report

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
				init_app()
				continue
		return None  # Хз что возвращать лучше,если не получилась
	return wrapper

def init_app():
	if not firebase_admin._apps:
		cred = credentials.Certificate("serviceAccountKey.json")
		app = firebase_admin.initialize_app(cred, {
			'databaseURL': "https://studingbot-cf957-default-rtdb.europe-west1.firebasedatabase.app/"
		})

@trying_decorator
def create_new_chat(chat_id):
	ref = db.reference("/Chats")

	ref.update({
		chat_id: {
			"settings": {
				"schedule": -1,
				"links": -1,
				"courses": -1,
				"time_delta": 4,
				"spam_options":{
					"schedule": False,
					"weather": False,
					"week": False
				},
				"town":"Ижевск"
			}
		}
	})


@trying_decorator
def get_all_chats():
	return db.reference("/Chats").get()


@trying_decorator
def add_new_course(chat_id, title, link, password):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		ref_courses = ref.child('settings').child('courses')

		ref_courses.push({
			"title": title,
			"link": link,
			"password": password
		})
	else:
		print("Чат не найден")


@trying_decorator
def delete_course(chat_id, course_id=None, delete_all=False):
	"""
	:param chat_id:
	:param course_id: если нужно удалить конкретный курс ( по умолчанию неопределенно )
	:param delete_all: если нужно удалить все ( по умолчанию False )
	:return:
	"""
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		ref_courses = ref.child('settings/courses/')
		if delete_all:
			ref_courses.set(-1)
		elif course_id:
			cur_course = ref.child('settings/courses/' + course_id)
			if cur_course.get():
				cur_course.delete()
			else:
				print("Указанный курс не был найден по id")
		else:
			print("Нужно добавить параметр course_id или delete_all")


@trying_decorator
def get_all_courses(chat_id):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		ref_courses = ref.child('settings').child('courses')
		courses = ref_courses.get()
		# for key, value in courses.items():
		# 	print(key, value)
		return courses


@trying_decorator
def update_course(chat_id, course_id, title, link, password):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		cur_course = ref.child('settings/courses/' + course_id)
		if cur_course.get():
			cur_course.update({
			"title": title,
			"link": link,
			"password": password
		})


@trying_decorator
def add_new_link(chat_id, title, link, password):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		ref_courses = ref.child('settings/links/')

		ref_courses.push({
			"title": title,
			"link": link,
			"password": password
		})


@trying_decorator
def delete_link(chat_id, link_id=None, delete_all=False):
	"""
	:param chat_id:
	:param link_id: если нужно удалить конкретную ссылку ( по умолчанию неопределенно )
	:param delete_all: если нужно удалить все ( по умолчанию False )
	:return:
	"""
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		ref_courses = ref.child('settings/links/')
		if delete_all:
			ref_courses.set(-1)
		elif link_id:
			cur_link = ref.child('settings/links/' + link_id)
			if cur_link.get():
				cur_link.delete()
			else:
				print("Указанная ссылка не была найден по id")
		else:
			print("Нужно добавить параметр link_id или delete_all")


@trying_decorator
def get_all_links(chat_id):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		ref_courses = ref.child('settings/links')
		courses = ref_courses.get()
		# for key, value in courses.items():
		# 	print(key, value)
		return courses


@trying_decorator
def update_link(chat_id, link_id, title, link, password):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		cur_link = ref.child('settings/links/' + link_id)
		if cur_link.get():
			cur_link.update({
			"title": title,
			"link": link,
			"password": password
			})
		else:
			print("Указанная ссылка не была найден по id")


@trying_decorator
def set_time_delta(chat_id, value):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		time_delta = ref.child("settings/time_delta")
		time_delta.set(value)

@trying_decorator
def set_town(chat_id, town):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		town_ref = ref.child("settings/town")
		town_ref.set(town)

@trying_decorator
def set_schedule(chat_id, schedule):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		schedule_ref = ref.child("settings/schedule")
		schedule_ref.set(schedule)

@trying_decorator
def set_spam_options(chat_id, weather, week, schedule):
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		spam_options_ref = ref.child("settings/spam_options")
		spam_options_ref.set({"weather": weather, "week":week, "schedule":schedule})

@trying_decorator
def get_pairs_on_day(chat_id, weekday, week_type):
	"""
	:param chat_id: 
	:param weekday: день недели, на русском, с большой буквы (Понедельник)
	:param week_type: тип недели, на русском, с малой буквы (под, над)
	:return: Список пар, если пар нет или на такой день нет расписания вернёт None
	"""
	ref = db.reference("/Chats/{}".format(chat_id))
	if ref.get():
		schedule_ref = ref.child("settings/schedule")
		if schedule_ref.get():
			pairs_day_ref = schedule_ref.child(weekday)
			if pairs_day_ref.get():
				pairs = filter(lambda x: x['week_type'] == week_type or x['week_type'] == "оба", pairs_day_ref.get())
				sorted_pairs = sorted(list(pairs), key=lambda x: x['num_pair'])
				return sorted_pairs
	return None


@trying_decorator
def get_all_chats_id():
	ref = db.reference("/Chats")
	if ref.get():
		return list(ref.get().keys())

	return []



init_app()

# create_new_chat("2000000002")
# add_new_course("2000000005", "НИР", "https://ee.istu.ru/course/view.php?id=5807", "ПрактикаНИР_АСОИУ")
# add_new_course("2000000005", "ПМП", "https://ee.istu.ru/course/view.php?id=4572", "-")
# delete_course("2000000005", delete_all=True)
# update_course("2000000005", "NNml2IdbVUtMje_t-Du", "Научная исследовательская работа", "https://ee.istu.ru/course/view.php?id=5807", "НИР_АСОИУ")
# set_time_delta("2000000005", 5)
#
# with open("schedule.json", "r", encoding="utf8") as f:
# 	file_contents = json.load(f)
# set_schedule("2000000002", schedule=file_contents)
# print(get_pairs_on_day("2000000005", "Понедельник", "под"))
# print(get_pairs_on_day("2000000005", "Вторник", "под"))
# print(get_pairs_on_day("2000000005", "Среда", "под"))
# print(get_pairs_on_day("2000000005", "Четверг", "под"))
# print(get_pairs_on_day("2000000005", "Пятница", "под"))
#
# add_new_link("2000000005", "НИР", "https://ee.istu.ru/course/view.php?id=5807", "ПрактикаНИР_АСОИУ")
# add_new_link("2000000005", "ПМП", "https://ee.istu.ru/course/view.php?id=4572", "-")
# delete_link("2000000005", delete_all=True)
# update_link("2000000005", "-NNqHsFDdlRHbXr1_UpN", "Научная исследовательская работа", "https://ee.istu.ru/course/view.php?id=5807", "НИР_АСОИУ")
#
# get_all_chats()
# print(get_all_chats_id())
