import os
import sys
import threading
import datetime
import time

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint

from commands.weather import weather
from commands.animes import get_top
from commands.info_for_the_day import info_for_the_day

token = 'e94dbd6b9db4af4afd0cde9f0f7be84922aa1d01a34734a533a878650f493d596459b2d87cef2c7128110'
group_id = '198707501'

def main():
    global vk_session
    global vk_api
    vk_session = VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, group_id, wait=10)
    vk_api = vk_session.get_api()
    try:
        while True:
            print('Bot started')
            for event in longpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    sender_id = event.message['from_id']
                    if event.message['text'][0] == '/':
                        parse_msg(event)
                    elif event.message['attachments'] and event.message['attachments'][0]['type'] == 'audio_message':
                            pass

    except BaseException as error:
        print(error)


def parse_msg(event):
    msg_text = event.message['text']
    if msg_text == '/погода':
        send_msg_tochat(vk_session, event.chat_id, weather()[0])
    if msg_text == '/аниме':
        send_msg_tochat(vk_session, event.chat_id, get_top())
    if msg_text == '/день':
        send_msg_tochat(vk_session, event.chat_id, info_for_the_day())


def send_msg_tochat(vk_session, chat_id, message):
    """
    Отправка сообщения через метод messages.send
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    # vk_session.method('messages.send',
    #                   {'chat_id': chat_id, 'message': message, 'random_id': randint(0, 2048)})\
    vk_api.messages.send(chat_id= chat_id, message= message, random_id= randint(0, 2048))


def wait_time():
    print("wait timer started")
    offset = datetime.timedelta(hours=4)
    now_date_izh = datetime.datetime.utcnow() + offset
    
    list_ids_chats_for_spam = [5]
    while True:
        print(datetime.datetime.utcnow())
        print(now_date_izh.now())
        if(now_date_izh.now().hour == 8 and now_date_izh.now().minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(vk_session, id, info_for_the_day())
        elif(now_date_izh.now().hour == 20 and now_date_izh.now().minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(vk_session, id, info_for_the_day(tomorrow=True))
        time.sleep(60)


if __name__ == '__main__':
    listener_thread = threading.Thread(target=main)
    waiter_thread = threading.Thread(target=wait_time)

    listener_thread.start()
    waiter_thread.start()