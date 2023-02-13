from random import randint

from helpers.server_notification import print_report

def send_msg(vk_api, peer_id, message=None, attachment=None):
    """
    Отправка сообщения через метод messages.send
    :param vk_api
    :param peer_id:
    :param message: содержимое отправляемого письма
    :return: None
    """

    #('Connection aborted.', ConnectionResetError(10054, 'Удаленный хост принудительно разорвал существующее подключение', None, 10054, None))
    count_retries = 2  # Для повторной отправки сообщения,в случае разрыва соединения хостом
    for attempt_no in range(count_retries):
        try:
            response = vk_api.messages.send(peer_id=peer_id, message=message,attachment=attachment, random_id= randint(0, 2048))
            return response
        except Exception as error:
            print_report(error)
            continue
    return error # Хз что возвращать лучше,если не получилась отправка

def send_msg_tochat(vk_api, chat_id, message=None, attachment=None): # LEGACY
    """
    Отправка сообщения через метод messages.send
    :param vk_api
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """

    #('Connection aborted.', ConnectionResetError(10054, 'Удаленный хост принудительно разорвал существующее подключение', None, 10054, None))
    count_retries = 2  # Для повторной отправки сообщения,в случае разрыва соединения хостом
    for attempt_no in range(count_retries):
        try:
            response = vk_api.messages.send(chat_id=chat_id, message=message,attachment=attachment, random_id= randint(0, 2048))
            return response
        except Exception as error:
            print_report(error)
            continue
    return error # Хз что возвращать лучше,если не получилась отправка


def send_msg_touser(vk_api, user_id, message=None, attachment=None):  # LEGACY
    """
    Отправка сообщения через метод messages.send
    :param vk_api
    :param user_id: id пользователя, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    count_retries = 2  # Для повторной отправки сообщения,в случае разрыва соединения хостом
    for attempt_no in range(count_retries):
        try:
            response = vk_api.messages.send(user_id=user_id, message=message,attachment=attachment, random_id= randint(0, 2048))
            return response
        except Exception as error:
            print_report(error)
            continue
    return error # Хз что возвращать лучше,если не получилась отправка
