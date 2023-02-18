import firebase_admin
from firebase_admin import credentials, db, firestore
import json
import traceback

from helpers.server_notification import print_report


def init_app():
	if not firebase_admin._apps:
		cred = credentials.Certificate("serviceAccountKey.json")
		app = firebase_admin.initialize_app(cred, {
			'databaseURL': "https://studingbot-cf957-default-rtdb.europe-west1.firebasedatabase.app/"
		})

def create_new_chat(chat_id):
	try:
		ref = db.reference("/Chats")

		ref.update({
			chat_id: {
				"settings": {
					"schedule": -1,
					"links": -1,
					"courses": -1,
					"time_delta": 4
				}
			}
		})
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		create_new_chat(chat_id)

def get_all_chats():
	try:
		return db.reference("/Chats").get()
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		get_all_chats()

def add_new_course(chat_id, title, link, password):
	try:
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
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		add_new_course(chat_id, title, link, password)

def delete_course(chat_id, course_id=None, delete_all=False):
	"""
	:param chat_id:
	:param course_id: если нужно удалить конкретный курс ( по умолчанию неопределенно )
	:param delete_all: если нужно удалить все ( по умолчанию False )
	:return:
	"""
	try:
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
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		delete_course(chat_id, course_id=None, delete_all=False)

def get_all_courses(chat_id):
	try:
		ref = db.reference("/Chats/{}".format(chat_id))
		if ref.get():
			ref_courses = ref.child('settings').child('courses')
			courses = ref_courses.get()
			# for key, value in courses.items():
			# 	print(key, value)
			return courses
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		get_all_courses(chat_id)

def update_course(chat_id, course_id, title, link, password):
	try:
		ref = db.reference("/Chats/{}".format(chat_id))
		if ref.get():
			cur_course = ref.child('settings/courses/' + course_id)
			if cur_course.get():
				cur_course.update({
				"title": title,
				"link": link,
				"password": password
			})
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		update_course(chat_id, course_id, title, link, password)


def add_new_link(chat_id, title, link, password):
	try:
		ref = db.reference("/Chats/{}".format(chat_id))
		if ref.get():
			ref_courses = ref.child('settings/links/')

			ref_courses.push({
				"title": title,
				"link": link,
				"password": password
			})
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		add_new_link(chat_id, title, link, password)


def delete_link(chat_id, link_id=None, delete_all=False):
	"""
	:param chat_id:
	:param link_id: если нужно удалить конкретную ссылку ( по умолчанию неопределенно )
	:param delete_all: если нужно удалить все ( по умолчанию False )
	:return:
	"""
	try:
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
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		delete_link(chat_id, link_id, delete_all)

def get_all_links(chat_id):
	try:
		ref = db.reference("/Chats/{}".format(chat_id))
		if ref.get():
			ref_courses = ref.child('settings/links')
			courses = ref_courses.get()
			# for key, value in courses.items():
			# 	print(key, value)
			return courses
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		get_all_links(chat_id)

def update_link(chat_id, link_id, title, link, password):
	try:
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
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		update_link(chat_id, link_id, title, link, password)

def set_time_delta(chat_id, value):
	try:
		ref = db.reference("/Chats/{}".format(chat_id))
		if ref.get():
			time_delta = ref.child("settings/time_delta")
			time_delta.set(value)
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		set_time_delta(chat_id, value)

def set_schedule(chat_id, schedule):
	try:
		ref = db.reference("/Chats/{}".format(chat_id))
		if ref.get():
			schedule_ref = ref.child("settings/schedule")
			schedule_ref.set(schedule)
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		set_schedule(chat_id, schedule)


def get_pairs_on_day(chat_id, weekday, week_type):
	"""
	:param chat_id: 
	:param weekday: день недели, на русском, с большой буквы (Понедельник)
	:param week_type: тип недели, на русском, с малой буквы (под, над)
	:return: Список пар, если пар нет или на такой день нет расписания вернёт None
	"""
	try:
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
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		get_pairs_on_day(chat_id, weekday, week_type)

def get_all_chats_id():
	try:
		ref = db.reference("/Chats")
		if ref.get():
			return list(ref.get().keys())

		return []
	except Exception as error:
		print_report(error, traceback=traceback.format_exc())
		init_app()
		get_all_chats_id()


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

# add_new_link("2000000005", "НИР", "https://ee.istu.ru/course/view.php?id=5807", "ПрактикаНИР_АСОИУ")
# add_new_link("2000000005", "ПМП", "https://ee.istu.ru/course/view.php?id=4572", "-")
# delete_link("2000000005", delete_all=True)
# update_link("2000000005", "-NNqHsFDdlRHbXr1_UpN", "Научная исследовательская работа", "https://ee.istu.ru/course/view.php?id=5807", "НИР_АСОИУ")

# get_all_chats()
# print(get_all_chats_id())
