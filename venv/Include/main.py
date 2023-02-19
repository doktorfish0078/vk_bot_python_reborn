import os
import sys
import threading
import time
import re
import traceback


from commands.welcome import welcome_msg
from commands.weather import weather
from commands.animes import get_top
from commands.how_week import how_week
from commands.info_for_the_day import info_for_the_day
from commands.schedule_bus import get_byte_screen_schedule_bus
from commands.upload_bin_img_on_vk import get_attachment
from commands.help_faq import help_faq
from commands.skirmish import skirmish
from commands.punish import punish
from commands.couple import couple
from commands.get_courses import get_courses
from commands.get_zoom_links import get_zoom_links
from commands.info_about_lesson import info_about_lessons
from commands.setting_bot import settings_session
from commands.create_new_course import create_new_course
from commands.create_new_link import create_new_link
from commands.new_invite import new_invite

from helpers.regional_datetime import regional_datetime
from helpers.messages import send_msg, send_msg
from helpers.server_notification import print_report

import rest_db as rest_db


from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


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

    elif request in ['пары']:
        if 'завтра' in words_message:
            send_msg(vk_api, peer_id, message=info_about_lessons(peer_id, tomorrow=True))
        else:
            send_msg(vk_api, peer_id, message=info_about_lessons(peer_id))

    elif request in ['настройка']:
        settings_session(vk_api=vk_api, chat_id=peer_id, user_sender_id=event.message.from_id)
    else:
        send_msg(vk_api, peer_id,
                        message='Такой команды не найдено :( Попробуйте на писать /help для того, чтобы ознакомится со списком команд')


def parse_settings_msg(event, peer_id):
    # Форма сообщения /КОМАНДА ID_CHAT PARAMS
    words_message = re.split("[, \-!?:]+", event.message['text'][1:])  #all words[] without first char /
    request = words_message[0]  # first word after /
    if request in ['добавить']:
        if 'курс' in words_message:
            finded_params = re.findall(r'.* (\d{10}) (.+) (.+) (.+)', event.message['text']) # Нужно сделать регулярку лучше
            if finded_params:
                chat_id, title, link, password = finded_params[0]
                res = create_new_course(chat_id, title, link, password)
                if res:
                    send_msg(vk_api, peer_id, "Ваш курс успешно сохранён")
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")

        if 'ссылку' in words_message:
            finded_params = re.findall(r'.* (\d{10}) (.+) (.+) (.+)', event.message['text']) # Нужно сделать регулярку лучше
            if finded_params:
                chat_id, title, link, password = finded_params[0]
                create_new_link(chat_id, title, link, password)
            else:
                send_msg(vk_api, peer_id, "Извините,вы где-то ошиблись")

    elif request in ['расписание']:
        pass
    elif request in ['задать']:
        if 'неделю' in words_message:
            pass

def wait_time():
    print_report("Временной таймер для спама запущен")
    ids_chats = rest_db.get_all_chats_id()
    while True:
        izh_date = regional_datetime(delta_hours=4)
        current_time = f'{izh_date.hour}:{izh_date.minute}'
        # current_time = f'{izh_date.minute}'
        # times_for_spam = ['8:0','20:0']
        # if current_time in times_for_spam:
        #     send_msg(vk_api, "2000000005", info_for_the_day("2000000005"))
        if current_time == '8:0':
            for id in ids_chats:
                send_msg(vk_api, id, info_for_the_day(id))
        elif current_time == '20:0':
            for id in ids_chats:
                send_msg(vk_api, id, info_for_the_day(id, tomorrow=True))

        time.sleep(60)


if __name__ == '__main__':
    listener_thread = threading.Thread(target=main)
    waiter_thread = threading.Thread(target=wait_time)

    listener_thread.start()
    time.sleep(3)
    waiter_thread.start()



