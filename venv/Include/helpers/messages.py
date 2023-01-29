from random import randint

from helpers.server_notification import print_report

def send_msg_tochat(vk_api, chat_id, message=None, attachment=None):
    """
    Отправка сообщения через метод messages.send
    :param vk_api
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    # vk_session.method('messages.send',
    #                   {'chat_id': chat_id, 'message': message, 'random_id': randint(0, 2048)})\
    response = vk_api.messages.send(chat_id= chat_id, message= message,attachment=attachment, random_id= randint(0, 2048))
    print_report(response)
    return response


