from random import randint


def punish(vk_api, event, words_message):
    # if is_god:
    #     enemy_id = to_punish
    # else:
    #     enemy_id = sender_id
    try:
        enemy_id = int(words_message[1].split('|')[0][3:])
        enemy = vk_api.users.get(user_ids=enemy_id, fields='sex')[0]
        enemy_name_case_gen = vk_api.users.get(user_ids=enemy_id, fields='sex', name_case='gen')[0]

        enemy_sex = enemy['sex']
        enemy_first_name = enemy['first_name']
    
        punishment_options_man = {
            0: 'Пососи, попущенный под столиком грязный пасынок собаки @id{}({})'.format(enemy_id, enemy_first_name),
            1: 'Ты -- тупая сука, @id{}({}), мои sicario будут трахать тебя перед тем как вырезать все твои органы, '
               'чтобы просто съесть их'.format(enemy_id, enemy_first_name),
            2: 'Черный воронок едет за вами, @id{}({}) 🚗🚗🚗 Готовься к лагерю, а точнее, к месту у параши'.format(enemy_id,
                                                                                                                    enemy_first_name),
            3: 'Однажды меня спросили: "@id{}({}) сосёт?".\nЯ не ответил, ведь, как оказалось, это был не вопрос'.format(enemy_id,
                                                                                                                         enemy_first_name),
            4: 'Ты думаешь это шутка? Нет, @id{}({}), шутка это твоя жизнь блять, при этом не очень удачная'.format(enemy_id,
                                                                                                                    enemy_first_name),
            5: 'Я ебал жену @id{0}({1})!\nМне сасала дочь @id{0}({1})!\nКак тебе рифма?'.format(enemy_id,
                                                                                                enemy_name_case_gen['first_name']),
            6: '@id{}({}) угрожающе размахивает клешнями, начинает набирать борзоми для гадзы, '
               'но подскальзывается на птичьем кале и падает прямо ртом на письку оппонента'.format(
                enemy_id, enemy_first_name),
            7: '@id{}({}) кинул предъяву в сторону пажилой мафии, за что высшие силы были вынуждены его моментально потушить'.format(
                enemy_id, enemy_first_name)
        }
    
        punishment_options_woman = {
            0: 'Пососи, собакоподобная пакость, не становись ортомом, @id{}({})'.format(enemy_id, enemy_first_name),
            1: 'Женщина -- лучший друг человека, но ты, @id{}({}), явно лучший друг ортёма (фу)'.format(enemy_id, enemy_first_name),
            2: 'Пажилая сперма капает на твоё личико, @id{}({}), подобное поведение явно стало твоей ошибкой'.format(
                enemy_id, enemy_first_name),
            3: 'Кто волки, кто овцы... А ты, @id{}({}) -- просто конченная овца'.format(enemy_id, enemy_first_name),
            4: 'Девачка па кличке @id{}({}) решила, что может изливать свою грязь публично)))) Иди подмойся дурашка..'.format(enemy_id, enemy_first_name),
            5: '@id{}({}) сладкая как такос с гавном и красивая как фото с ортёмом'.format(enemy_id, enemy_first_name)
        }
    
        punishment_options_not_god = {
            0: '@id{}({}), пат столик быстра'.format(enemy_id, enemy_first_name),
            1: 'А чё ещё тебе сделать, @id{}({})? Пасаси лучше'.format(enemy_id, enemy_first_name),
            2: '@id{}({}), лучше извинись'.format(enemy_id, enemy_first_name),
            3: 'Фейспалм... @id{}(Ты) в муте, клоwн'.format(enemy_id)
    
        }

        if enemy_sex == 2:
            return punishment_options_man[randint(0, len(punishment_options_man) - 1)]
        return punishment_options_woman[randint(0, len(punishment_options_woman) - 1)]

    except BaseException as error:
        print(error)
        return 'Чот не могу придумать как унизить...'


