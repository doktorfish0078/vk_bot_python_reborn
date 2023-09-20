import random

def skirmish(vk_api, event, words_message, gm=False):
    if len(words_message) >= 2:
        try:
            second_warrior_id = int(words_message[1].split('|')[0][3:])
            player1 = vk_api.users.get(user_ids='{}'.format(event.message['from_id']))[0]
            player2 = vk_api.users.get(user_ids='{}'.format(second_warrior_id))[0]

            if not gm:
                roll = random.randint(0, 1)
            if player1['id'] == player2['id']:
                return 'Нельзя в себя стрелять, а то зароскомнадзоришься'
            if roll == 0:
                return ('Победитель, палучаица, @id{0}({1})'.format(player1['id'], player1['first_name']))
            else:
                return ('Победитель, палучаица, @id{0}({1})'.format(player2['id'], player2['first_name']))
        except BaseException as error:
            print(error)
            return 'Чот не вышло :('         
    else:
        return 'А по кому стрелять то? По воробьям?'
