import os
import sys
import threading
import datetime
import time
import re
import requests

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint

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
                try:
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                        print_report(event)
                        sender_id = event.message['from_id']
                    if event.message['text'] != '':
                        if event.message['text'][0] == '/':
                            parse_msg(event)
                        elif event.message['attachments'] and event.message['attachments'][0]['type'] == 'audio_message':
                                pass
                except requests.exceptions.ReadTimeout:
                    print_report("Порвалось соединение")

                #valentine
                # if event.type == VkBotEventType.MESSAGE_NEW and (not event.from_group and not event.from_chat ):
                #     text = event.message['text']
                #     splt = text.split(' ')
                #     try :
                #         if (splt[0] == 'валентинка') or (splt[0] == 'valentine'):
                #             author = 'Валентино4ка от vk.com/id' + str(event.message.from_id) + '\n'
                #             target_id_or_name = (splt[1]).split('vk.com/')[1]
                #             target_id = vk_api.users.get(user_ids = target_id_or_name, fields = 'city')[0]['id']
                #             # print(target_id)
                #             attachs = [str(i['type'])+str(i[i['type']]['owner_id'])+'_'+str(i[i['type']]['id'])+('_'+str(i[i['type']]['access_key']) if 'access_key' in i[i['type']] else '' ) for i in  event.message['attachments']]
                #             print(event)
                #             vk_api.messages.send(user_id= target_id, attachment = ','.join(attachs), message= author+' '.join(splt[2:]), random_id= randint(0, 2048))
                #     except BaseException as error:
                #         print(error)
                #         vk_api.messages.send(user_id= event.message['from_id'], message= 'Иди нахуй клоун', random_id= randint(0, 2048))



    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)


def parse_msg(event):
    msg_text = event.message['text'].lower()
    words_message = re.split("[, \-!?:]+", msg_text[1:])  #all words[] without first char /
    request = words_message[0]  # first word atref /
    if request in ['help','помощь']:
        send_msg_tochat(event.chat_id, help_faq())
    elif request in ['погода']:
        if 'завтра' in words_message:
            send_msg_tochat(event.chat_id, weather(tomorrow=True)[0])
        elif 'неделю' in words_message:
            send_msg_tochat(event.chat_id, weather(week=True)[0])
        else:
            send_msg_tochat(event.chat_id, weather()[0])

    elif request in ['неделя']:
        if 'завтра' in words_message:
            send_msg_tochat(event.chat_id, how_week(tomorrow=True))
        else:
            send_msg_tochat(event.chat_id, how_week())

    # elif request in ['день']:
    #     send_msg_tochat(event.chat_id, info_for_the_day())

    elif request in ['автобус']:
        send_msg_tochat(event.chat_id, message="Ищем расписание вашего автобуса, ожидайте...")
        byte_screen = get_byte_screen_schedule_bus(msg_text[1:])
        if not byte_screen is None:
            attachment = get_attachment(vk_api, byte_screen)
            if not attachment is None:
                send_msg_tochat(event.chat_id, attachment=attachment)
        else:
            send_msg_tochat(event.chat_id, message='Не получилось получить информацию о вашем автобусе, не расстраивайтесь :)')
            
    elif request in ['skirmish', 'перестрелка', "🔫", 'bang', 'маслина']:
        send_msg_tochat(event.chat_id,
                        message=skirmish(vk_api=vk_api,
                                         event=event,
                                         words_message=words_message))
    elif request in ['punish', 'наказать', "наказание"]:
        if len(words_message) > 1:
            send_msg_tochat(event.chat_id, punish(vk_api=vk_api,
                                                  event=event,
                                                  words_message=words_message)
                            )
    elif request in ['пара', 'похуй', 'couple']:
        if len(words_message) == 1:
            send_msg_tochat(event.chat_id, message=couple(how_week(boolean = True)))

    elif request in ['ссылки']:
        send_msg_tochat(event.chat_id, message=get_zoom_links())

    elif request in ['курсы']:
        send_msg_tochat(event.chat_id, message=get_courses())

    elif request in ['пары']:
        if 'завтра' in words_message:
            send_msg_tochat(event.chat_id, message=info_about_lessons(tomorrow=True))
        else:
            send_msg_tochat(event.chat_id, message=info_about_lessons())

    elif request in ['ev']:
        if event.message.from_id not in [135224919, 169026012]:
            send_msg_tochat(event.chat_id, "не(")
        else:
            try:
                eval(event.message['text'][3:])
            except Exception as e:
                send_msg_tochat(event.chat_id, "хуйню написал подмойся: "+str(e))

    else:
        send_msg_tochat(event.chat_id,
                        message='Такой команды не найдено :( Попробуйте на писать /help для того, чтобы ознакомится со списком команд')



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


def spam(takes, chat_id, message=None, attachment=None):
    for i in range(takes):
        send_msg_tochat(chat_id, message, attachment)


def wait_time():
    print("wait timer started")
    list_ids_chats_for_spam = [2,5]
    # send_msg_tochat(2, welcome_msg())
    while True:
        izhevsk_utc_date = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        if(izhevsk_utc_date.hour == 8 and izhevsk_utc_date.minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(id, info_for_the_day())
        elif(izhevsk_utc_date.hour == 20 and izhevsk_utc_date.minute == 0):
            for id in list_ids_chats_for_spam:
                send_msg_tochat(id, info_for_the_day(tomorrow=True))
        time.sleep(60)


def print_report(report):
	print("{}: {}".format(datetime.datetime.utcnow() + datetime.timedelta(hours=4), report))

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
    time.sleep(5)
    waiter_thread.start()
