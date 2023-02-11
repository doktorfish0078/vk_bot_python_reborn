from Include.helpers.messages import send_msg_tochat
from Include.commands.help_faq import help_faq
import Include.rest_db as rest_db

def new_invite(vk_api, peer_id):
    """
    Приветствие со списком функционала
    Добавления шаблона настроек чата в БД(С проверкой на то, существует ли уже такой чат БД, если да,то не стоит наверное настройки ему пересоздавать
    Информация о необходимости предоставления админ прав боту
    :param vk_api:
    :param peer_id:
    :return:
    """

    send_msg_tochat(vk_api, peer_id, "Всех приветствую, рад познакомиться!")
    send_msg_tochat(vk_api, peer_id, help_faq())
    all_chats = rest_db.get_all_chats()
    if peer_id not in all_chats:
        rest_db.create_new_chat(full_chat_id)
        send_msg_tochat(vk_api, peer_id, "Чтобы я мог полноценно функционировать в вашей беседе, пожалуйста, выдайте мне права администратора беседы")