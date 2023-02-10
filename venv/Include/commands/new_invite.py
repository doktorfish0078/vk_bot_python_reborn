from Include.helpers.messages import send_msg_tochat
from Include.commands.help_faq import help_faq
import Include.rest_db as rest_db

def new_invite(vk_api, chat_id):
    """
    Приветствие со списком функционала
    Добавления шаблона настроек чата в БД(С проверкой на то, существует ли уже такой чат БД, если да,то не стоит наверное настройки ему пересоздавать
    Информация о необходимости предоставления админ прав боту
    :param vk_api:
    :param chat_id: < 100000000, event.chat_id возвращает не полный id чата, а урезанный. Полный это 2000000000 + event.chat_id
    :return:
    """

    send_msg_tochat(vk_api, chat_id, "Всех приветствую, рад познакомиться!")
    send_msg_tochat(vk_api, chat_id, help_faq())
    all_chats = rest_db.get_all_chats()
    full_chat_id = str(2000000000 + chat_id)
    if full_chat_id not in all_chats:
        rest_db.create_new_chat(full_chat_id)
        send_msg_tochat(vk_api, chat_id, "Чтобы я мог полноценно функционировать в вашей беседе, пожалуйста, выдайте мне права администратора беседы")