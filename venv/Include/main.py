import os
import sys
import threading
import datetime
import time
import re

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint

from commands.weather import weather
from commands.animes import get_top
from commands.info_for_the_day import info_for_the_day
from commands.schedule_bus import get_byte_screen_schedule_bus
from commands.upload_bin_img_on_vk import get_attachment

token = 'e94dbd6b9db4af4afd0cde9f0f7be84922aa1d01a34734a533a878650f493d596459b2d87cef2c7128110'
group_id = '198707501'

def main():
    global vk_session
    global vk_api
    try:
        vk_session = VkApi(token=token)
        longpoll = MyVkLongPoll(vk_session, group_id, wait=10)
        vk_api = vk_session.get_api()
        while True:
            print('Bot started')
            for event in longpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    sender_id = event.message['from_id']
                    if event.message['text'][0] == '/':
                        parse_msg(event)
                    elif event.message['attachments'] and event.message['attachments'][0]['type'] == 'audio_message':
                            pass

    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)


def parse_msg(event):
    msg_text = event.message['text'].lower()
    words_message = re.split("[, \-!?:]+", msg_text[1:])
    request = words_message[0]

    if request in ['погода']:
        send_msg_tochat(event.chat_id, weather()[0])
    elif request in ['аниме']:
        send_msg_tochat(event.chat_id, get_top())
    elif request in ['день']:
        send_msg_tochat(event.chat_id, info_for_the_day())
    elif request in ['автобус']:
        send_msg_tochat(event.chat_id, message="Ищем расписание вашего автобуса, ожидайте...")
        byte_screen = get_byte_screen_schedule_bus(msg_text[1:])
        if not byte_screen is None:
            attachment = get_attachment(vk_api, byte_screen)
            if not attachment is None:
                send_msg_tochat(event.chat_id, attachment=attachment)
        else:
            send_msg_tochat(event.chat_id, message='Не получилось получить информацию о вашем автобусе, не расстраивайтесь :)')



def send_msg_tochat(chat_id, message=None, attachment=None):
    """
    Отправка сообщения через метод messages.send
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    # vk_session.method('messages.send',
    #                   {'chat_id': chat_id, 'message': message, 'random_id': randint(0, 2048)})\
    vk_api.messages.send(chat_id= chat_id, message= message,attachment=attachment, random_id= randint(0, 2048))


def wait_time():
    print("wait timer started")
    list_ids_chats_for_spam = [5]
    while True:
        izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        if(izhevsk_utc_date.hour == 8 and izhevsk_utc_date.minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(vk_session, id, info_for_the_day())
        elif(izhevsk_utc_date.hour == 20 and izhevsk_utc_date.minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(vk_session, id, info_for_the_day(tomorrow=True))
        time.sleep(60)


class MyVkLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('error', e)

if __name__ == '__main__':
    listener_thread = threading.Thread(target=main)
    waiter_thread = threading.Thread(target=wait_time)

    listener_thread.start()
    waiter_thread.start()