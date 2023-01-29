import os
import sys
import threading
import datetime
import time
import re
import requests

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


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

from helpers.regional_datetime import regional_datetime
from helpers.messages import send_msg_tochat
from helpers.server_notification import print_report

token = 'e94dbd6b9db4af4afd0cde9f0f7be84922aa1d01a34734a533a878650f493d596459b2d87cef2c7128110'
group_id = '198707501'


class MyVkLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('error', e)

def main():
    global vk_session
    global vk_api
    try:
        vk_session = VkApi(token=token)
        longpoll = MyVkLongPoll(vk_session, group_id, wait=25)
        vk_api = vk_session.get_api()
        while True:
            print_report("Прослушивание запущено")
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    print_report(event)
                    chat_id = event.chat_id
                    sender_id = event.message['from_id']
                if event.message['text'] != '' and event.message['text'][0] == '/':
                    parse_msg(event)

    except Exception as e:
        print_report(e)
        time.sleep(3)


def parse_msg(event):
    msg_text = event.message['text'].lower()
    words_message = re.split("[, \-!?:]+", msg_text[1:])  #all words[] without first char /
    request = words_message[0]  # first word after /
    if request in ['help','помощь']:
        send_msg_tochat(vk_api, event.chat_id, help_faq())
    elif request in ['погода']:
        if 'завтра' in words_message:
            send_msg_tochat(vk_api, event.chat_id, weather(tomorrow=True)[0])
        elif 'неделю' in words_message:
            send_msg_tochat(vk_api, event.chat_id, weather(week=True)[0])
        else:
            send_msg_tochat(vk_api, event.chat_id, weather()[0])

    elif request in ['неделя']:
        if 'завтра' in words_message:
            send_msg_tochat(vk_api, event.chat_id, how_week(tomorrow=True))
        else:
            send_msg_tochat(vk_api, event.chat_id, how_week())


    elif request in ['автобус']:
        send_msg_tochat(vk_api, event.chat_id, message="Ищем расписание вашего автобуса, ожидайте...")
        byte_screen = get_byte_screen_schedule_bus(msg_text[1:])
        if not byte_screen is None:
            attachment = get_attachment(vk_api, byte_screen)
            if not attachment is None:
                send_msg_tochat(vk_api, event.chat_id, attachment=attachment)
        else:
            send_msg_tochat(vk_api, event.chat_id, message='Не получилось получить информацию о вашем автобусе, не расстраивайтесь :)')

    elif request in ['ссылки']:
        send_msg_tochat(vk_api, event.chat_id, message=get_zoom_links())

    elif request in ['курсы']:
        send_msg_tochat(vk_api, event.chat_id, message=get_courses())

    elif request in ['пары']:
        if 'завтра' in words_message:
            send_msg_tochat(vk_api, event.chat_id, message=info_about_lessons(tomorrow=True))
        else:
            send_msg_tochat(vk_api, event.chat_id, message=info_about_lessons())

    else:
        send_msg_tochat(vk_api,event.chat_id,
                        message='Такой команды не найдено :( Попробуйте на писать /help для того, чтобы ознакомится со списком команд')


def wait_time():
    print_report("Временной таймер для спама запущен")
    list_ids_chats_for_spam = [2,5]
    while True:
        izhevsk_utc_date = regional_datetime(delta_hours=4)
        if(izhevsk_utc_date.hour == 8 and izhevsk_utc_date.minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(vk_api, id, info_for_the_day())
        elif(izhevsk_utc_date.hour == 20 and izhevsk_utc_date.minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(vk_api, id, info_for_the_day(tomorrow=True))
        time.sleep(60)


if __name__ == '__main__':
    listener_thread = threading.Thread(target=main)
    waiter_thread = threading.Thread(target=wait_time)

    listener_thread.start()
    time.sleep(5)
    waiter_thread.start()


