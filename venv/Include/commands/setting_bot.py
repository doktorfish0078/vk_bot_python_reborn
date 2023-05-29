from Include.helpers import print_report
from Include.helpers import send_msg_touser
from Include.helpers import trying_decorator

def settings_session(vk_api, peer_id, user_sender_id):
    if not check_user_for_admin_rights(vk_api, peer_id, user_sender_id):
        send_msg_touser(vk_api, user_sender_id, "Вы не имеете прав администратора в этой беседе")
        return 0

    chat_obj = vk_api.messages.getConversationsById(peer_ids=peer_id)
    chat_id = int(peer_id) - 2000000000
    chat_title = chat_obj['items'][0]['chat_settings']['title']
    hello_msg = f"Здравствуйте, мы подтвердили, что Вы являетесь администратором беседы - \"{chat_title}\" c id - \"{chat_id}\"\n" \
                "Вы можете произвести настройку бота под вашу беседу при помощи следующих команд, отправленных в этот диалог:\n" \
                f"👉/настроить часовой пояс {chat_id} <значение>\n" \
                f"👉/настроить город {chat_id} <город>\n" \
                f"👉/настроить рассылку {chat_id} погода=<да/нет> неделя=<да/нет> расписание=<да/нет>\n" \
                f"👉/настроить расписание {chat_id} <приложите файл с расписанием>\n" \
                f"👉/добавить курс {chat_id} <название курса> <ссылка на курс> <кодовое слово>\n" \
                f"👉/добавить ссылку {chat_id} <название видеоконференции> <ссылка> <пароль>\n"
    send_msg_touser(vk_api, user_sender_id, hello_msg)

@trying_decorator
def check_user_for_admin_rights(vk_api, peer_id, user_id):
    members_chat = vk_api.messages.getConversationMembers(peer_id=peer_id)
    for i in range(0, members_chat['count']):
        member = members_chat['items'][i]
        if member['member_id'] == user_id:
            if "is_admin" in member:
                return member['is_admin']
    return False