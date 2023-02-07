from helpers.server_notification import print_report
from helpers.messages import send_msg_touser

def settings_session(vk_api, chat_id, user_sender_id):
    chat_id = 2000000000 + chat_id

    if not check_user_for_admin_rights(vk_api, chat_id, user_sender_id):
        send_msg_touser(vk_api, user_sender_id, "Вы не имеете прав администратора в этой беседе")
        return 0

    chat_obj = vk_api.messages.getConversationsById(peer_ids=chat_id)
    chat_title = chat_obj['items'][0]['chat_settings']['title']
    hello_msg = "Здравствуйте, мы подтвердили, что Вы являетесь администратором беседы - \"{}\" c id - \"{}\"\n" \
                "Вы можете произвести настройку бота под вашу беседу при помощи следующих команд, отправленных в этот диалог:\n" \
                "/добавить курс [id беседы] [название курса] [ссылка на курс] [кодовое слово]".format(chat_title, chat_id)
    send_msg_touser(vk_api, user_sender_id, hello_msg)


def check_user_for_admin_rights(vk_api, chat_id, user_id):
    members_chat = vk_api.messages.getConversationMembers(peer_id=chat_id)
    for i in range(0, members_chat['count']):
        member = members_chat['items'][i]
        if member['member_id'] == user_id and member['is_admin'] == True:
            return True
    return False