import os
import sys
import threading
import time
import re
import traceback
import requests
import json


# Получаем путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем путь к папке 'Include'
include_path = os.path.join(current_dir)

# Добавляем путь к папке 'Include' в sys.path
sys.path.append(include_path)


from commands import create_new_course, delete_course
from commands import create_new_link, delete_link
from commands import get_courses
from commands import get_zoom_links
from commands import help_faq
from commands import how_week
from commands import info_about_lessons
from commands import info_for_the_day
from commands import new_invite
from commands import get_byte_screen_schedule_bus
from commands import weather
from commands import get_top
from commands import get_attachment
from commands import skirmish
from commands import punish
from commands import couple
from commands import settings_session
from commands import set_time_delta
from commands import set_town
from commands import set_spam_options
from commands import set_schedule
from commands import create_new_event, delete_event
from commands import get_events

from helpers import regional_datetime
from helpers import send_msg
from helpers import print_report

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import rest_db as rest_db


class MyVkLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print_report(f'Longpool: {e}', traceback=traceback.format_exc())

def init_session():
    token = 'e94dbd6b9db4af4afd0cde9f0f7be84922aa1d01a34734a533a878650f493d596459b2d87cef2c7128110'
    group_id = '198707501'

    vk_session = VkApi(token=token)
    longpoll = MyVkLongPoll(vk_session, group_id, wait=25)
    vk_api = vk_session.get_api()

    return vk_api, longpoll

def main():
    while True:
        try:
            global vk_api
            vk_api, longpoll = init_session()

            print_report("Прослушивание запущено")
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    peer_id = event.message['peer_id'] # откуда получено сообщение
                    print_report(event)
                    if event.from_chat:
                        if 'action' in event.message:
                            if (event.message['action']['type'] == 'chat_invite_user'
                            and event.message['action']['member_id'] == -198707501):
                                new_invite(vk_api, peer_id)

                        if event.message['text'] != '' and event.message['text'][0] == '/':
                            parse_chat_msg(event, peer_id)

                    elif event.from_user:
                        parse_settings_msg(event, peer_id)
        except Exception as error:
            print_report(f'Main Thread: {error}', traceback=traceback.format_exc())
            time.sleep(0.3)
            continue


def parse_chat_msg(event, peer_id):
    msg_text = event.message['text'].lower()
    words_message = re.split("[, \-!?:]+", msg_text[1:])  #all words[] without first char /
    request = words_message[0]  # first word after /
    if request in ['help','помощь']:
        send_msg(vk_api, peer_id, help_faq())
    elif request in ['погода']:
        if 'завтра' in words_message:
            send_msg(vk_api, peer_id, weather(tomorrow=True)[0])
        elif 'неделю' in words_message:
            send_msg(vk_api, peer_id, weather(week=True)[0])
        else:
            send_msg(vk_api, peer_id, weather()[0])

    elif request in ['неделя']:
        if 'завтра' in words_message:
            send_msg(vk_api, peer_id, how_week(tomorrow=True))
        else:
            send_msg(vk_api, peer_id, how_week())

    elif request in ['автобус']:
        send_msg(vk_api, peer_id, message="Ищем расписание вашего автобуса, ожидайте...")
        byte_screen = get_byte_screen_schedule_bus(msg_text[1:])
        if not byte_screen is None:
            attachment = get_attachment(vk_api, byte_screen)
            if not attachment is None:
                send_msg(vk_api, peer_id, attachment=attachment)
        else:
            send_msg(vk_api, peer_id, message='Не получилось получить информацию о вашем автобусе, не расстраивайтесь :)')

    elif request in ['ссылки']:
        send_msg(vk_api, peer_id, message=get_zoom_links(peer_id))

    elif request in ['курсы']:
        send_msg(vk_api, peer_id, message=get_courses(peer_id))

    elif request in ['расписание']:
        if 'завтра' in words_message:
            send_msg(vk_api, peer_id, message=info_about_lessons(peer_id, tomorrow=True))
        else:
            send_msg(vk_api, peer_id, message=info_about_lessons(peer_id))

    elif request in ['настройка']:
        settings_session(vk_api=vk_api, peer_id=peer_id, user_sender_id=event.message.from_id)

    elif request in ['добавить']:
        if 'мероприятие' in event.message['text']:
            finded_params = re.findall(r'.* (\d{1,2}\.\d{1,2}\.\d{4}) (\d{1,2}:\d{1,2}) "(.*)"', event.message['text'])
            if finded_params:
                date, time, event_name = finded_params[0]
                res = create_new_event(peer_id, date, time, event_name)
                if res:
                    send_msg(vk_api, peer_id, f"Ваше мероприятие {event_name} на {date} в {time} добавлено")
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
    else:
        send_msg(vk_api, peer_id,
                        message='Такой команды не найдено :( Попробуйте на писать /help для того, чтобы ознакомится со списком команд')


def parse_settings_msg(event, peer_id):
    # Форма сообщения /КОМАНДА ID_CHAT PARAMS
    words_message = re.split("[, \-!?:]+", event.message['text'][1:])  #all words[] without first char /
    request = words_message[0]  # first word after /
    if request in ['настроить']:
        if 'часовой пояс' in event.message['text']:
            finded_params = re.findall(r'.* (\d+) ([-+]?\d+)', event.message['text'])

            if finded_params:
                chat_id, time_delta = finded_params[0]
                res = set_time_delta(int(chat_id) + 2000000000, int(time_delta))
                if res:
                    send_msg(vk_api, peer_id, f"Часовой пояс настроен на UTC {time_delta}")
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
        elif 'город' in event.message['text']:
            finded_params = re.findall(r'.* (\d+) (.+)', event.message['text'])
            if finded_params:
                chat_id, town = finded_params[0]
                res = set_town(int(chat_id) + 2000000000, town)
                if res:
                    send_msg(vk_api, peer_id, f'Город настроен на "{town}"')
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
        elif 'рассылку' in event.message['text']:
            finded_params = re.findall(r'.* (\d+) погода=(да|нет) неделя=(да|нет) расписание=(да|нет)', event.message['text'])
            if finded_params:

                chat_id, weather, week, schedule = finded_params[0]
                weather = weather == 'да' if True else False;
                week = week == 'да' if True else False;
                schedule = schedule == 'да' if True else False;
                res = set_spam_options(int(chat_id) + 2000000000, weather, week, schedule)
                if res:
                    send_msg(vk_api, peer_id, "Рассылка настроена")
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
        elif 'расписание' in event.message['text']:
            finded_params = re.findall(r'.* (\d+)', event.message['text'])
            if finded_params:
                chat_id = finded_params[0]
            if event.message.attachments != []:
                url = event.message.attachments[0]['doc']['url']
                response = requests.get(url)
                decoded_data = response.content.decode('utf-8')  # декодируем байтовую строку в строку
                schedule_data = json.loads(decoded_data)  # декодируем строку в формат JSON
                res = set_schedule(int(chat_id) + 2000000000, schedule_data)
                if res:
                    send_msg(vk_api, peer_id, "Расписание настроено")
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")

    elif request in ['добавить']:
        if 'курс' in words_message:
            finded_params = re.findall(r'.* (\d+) (.+) (.+) (.+)', event.message['text']) # Нужно сделать регулярку лучше
            if finded_params:
                chat_id, title, link, password = finded_params[0]
                res = create_new_course(int(chat_id) + 2000000000, title, link, password)
                if res:
                    send_msg(vk_api, peer_id, f'Ваш курс "{title}" добавлен')
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")

        elif 'ссылку' in words_message:
            finded_params = re.findall(r'.* (\d+) (.+) (.+) (.+)', event.message['text']) # Нужно сделать регулярку лучше
            if finded_params:
                chat_id, title, link, password = finded_params[0]
                res = create_new_link(int(chat_id) + 2000000000, title, link, password)
                if res:
                    send_msg(vk_api, peer_id, f'Ваша ссылка на видеоконференцию {title} добавлена')
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
    elif request in ['удалить']:
        if 'курс' in words_message:
            finded_params = re.findall(r'.* (\d+) (\d+)', event.message['text'])
            if finded_params:
                chat_id, index_course = finded_params[0]
                res = delete_course(int(chat_id) + 2000000000, int(index_course) - 1)
                if res:
                    send_msg(vk_api, peer_id, f'Ваш курс удалён')
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
        elif 'ссылку' in words_message:
            finded_params = re.findall(r'.* (\d+) (\d+)', event.message['text'])
            if finded_params:
                chat_id, index_link = finded_params[0]
                res = delete_link(int(chat_id) + 2000000000, int(index_link) - 1)
                if res:
                    send_msg(vk_api, peer_id, f'Ваша ссылка удалёна')
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
        elif 'мероприятие' in words_message:
            finded_params = re.findall(r'.* (\d+) (\d+)', event.message['text'])
            if finded_params:
                chat_id, index_event = finded_params[0]
                res = delete_event(int(chat_id) + 2000000000, int(index_event) - 1)
                if res:
                    send_msg(vk_api, peer_id, f'Ваше мероприятие удалёно')
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")

    elif request in ['список']:
        if 'курсов' in words_message:
            finded_params = re.findall(r'.* (\d+)', event.message['text'])
            if finded_params:
                chat_id = finded_params[0]
                send_msg(vk_api, peer_id, get_courses(int(chat_id) + 2000000000, enumerate_list=True))
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")

        elif 'ссылок' in words_message:
            finded_params = re.findall(r'.* (\d+)', event.message['text'])
            if finded_params:
                chat_id = finded_params[0]
                send_msg(vk_api, peer_id, get_zoom_links(int(chat_id) + 2000000000, enumerate_list=True))
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")
        elif 'мероприятий' in words_message:
            finded_params = re.findall(r'.* (\d+)', event.message['text'])
            if finded_params:
                chat_id = finded_params[0]
                send_msg(vk_api, peer_id, get_events(int(chat_id) + 2000000000, enumerate_list=True))
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")


    elif request in ['задать']:
        if 'неделю' in words_message:
            pass

def wait_time():
    print_report("Временной таймер для спама запущен")
    while True:
        ids_chats = rest_db.get_all_chats_id()
        izh_date = regional_datetime(delta_hours=4)
        curr_date = izh_date.strftime('%d.%m.%Y')
        curr_time = izh_date.strftime('%H:%M')
        for peer_id in ids_chats:
            spam_options = rest_db.get_spam_options(peer_id)
            if spam_options:
                if spam_options['schedule'] or spam_options['week'] or spam_options['weather']:
                    if curr_time == '08:00':
                        res = send_msg(vk_api, peer_id, info_for_the_day(peer_id, spam_options=spam_options))
                        if res:
                            print_report(f"Сообщение отправлено в чат {peer_id}")
                    elif curr_time == '20:00':
                        res = send_msg(vk_api, peer_id, info_for_the_day(peer_id, tomorrow=True, spam_options=spam_options))
                        if res:
                            print_report(f"Сообщение отправлено в чат {peer_id}")
            events = rest_db.get_all_events(peer_id)
            if events:
                for event_id, event in events.items():
                    if event['date'] == curr_date and event['time'] == curr_time:
                        res = send_msg(vk_api, peer_id, f'Напоминаю о запланированном на {event["date"]} мероприятии "{event["event_name"]}", которое состоится в {event["time"]}')
                        if res is not None:
                            print_report(f"Сообщение о мероприятии отправлено в чат {peer_id}")
                            rest_db.delete_event(peer_id, event_id)
        time.sleep(60)


if __name__ == '__main__':
    listener_thread = threading.Thread(target=main)
    waiter_thread = threading.Thread(target=wait_time)

    listener_thread.start()
    time.sleep(1)
    waiter_thread.start()



