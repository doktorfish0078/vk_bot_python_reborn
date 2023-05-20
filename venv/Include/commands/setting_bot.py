from Include.helpers import print_report
from Include.helpers import send_msg_touser
from Include.helpers import trying_decorator

def settings_session(vk_api, chat_id, user_sender_id):
    if not check_user_for_admin_rights(vk_api, chat_id, user_sender_id):
        send_msg_touser(vk_api, user_sender_id, "Вы не имеете прав администратора в этой беседе")
        return 0

    chat_obj = vk_api.messages.getConversationsById(peer_ids=chat_id)
    chat_title = chat_obj['items'][0]['chat_settings']['title']
    hello_msg = "Здравствуйте, мы подтвердили, что Вы являетесь администратором беседы - \"{0}\" c id - \"{1}\"\n" \
                "Вы можете произвести настройку бота под вашу беседу при помощи следующих команд, отправленных в этот диалог:\n" \
                "👉/настроить часовой пояс {1} [значение]\n" \
                "👉/настроить город {1} [город]\n" \
                "👉/настроить рассылку {1} погода=[да/нет] неделя=[да/нет] расписание=[да/нет]\n" \
                "👉/настроить расписание {1} [приложите файл с расписанием]\n" \
                "👉/добавить курс {1} [название курса] [ссылка на курс] [кодовое слово]\n" \
                "👉/добавить ссылку {1} [название видеоконференции] [ссылка] [пароль]\n".format(chat_title, chat_id)
    send_msg_touser(vk_api, user_sender_id, hello_msg)

@trying_decorator
def check_user_for_admin_rights(vk_api, chat_id, user_id):
    members_chat = vk_api.messages.getConversationMembers(peer_id=chat_id)
    for i in range(0, members_chat['count']):
        member = members_chat['items'][i]
        if member['member_id'] == user_id:
            if "is_admin" in member:
                return member['is_admin']
    return False