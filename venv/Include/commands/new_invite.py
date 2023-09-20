from helpers import send_msg
from commands import help_faq
from rest_db import get_all_chats_id, create_new_chat

def new_invite(vk_api, peer_id):
    """
    Приветствие со списком функционала
    Добавления шаблона настроек чата в БД(С проверкой на то, существует ли уже такой чат БД, если да,то не стоит наверное настройки ему пересоздавать
    Информация о необходимости предоставления админ прав боту
    :param vk_api:
    :param peer_id:
    :return:
    """

    send_msg(vk_api, peer_id, "Всех приветствую, рад познакомиться!")
    send_msg(vk_api, peer_id, help_faq())
    all_chats_ids = get_all_chats_id()
    if peer_id not in all_chats_ids:
        create_new_chat(peer_id)
        send_msg(vk_api, peer_id, "Чтобы я мог полноценно функционировать в вашей беседе, пожалуйста, выдайте мне права администратора беседы")