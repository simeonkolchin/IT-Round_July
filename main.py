import telebot
import dbworker
import config
import qrcode
from telebot import types
from config import TOKEN

allclaims = {}


claim1 = {}
claim1s = {}
claim2 = {}
claim2s = {}

bot = telebot.TeleBot(TOKEN)

joinedFile = open('joined.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

adminFile = open('admin.txt', 'r')
adminUsers = set()
for line in adminFile:
    adminUsers.add(line.strip())
adminFile.close()

@bot.message_handler(commands=['start'])
def start(message):
# ДОБАВЛЯЕМ ID ПОЛЬЗОВАТЕЛЯ В СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ БОТА
    id = message.chat.id
    if not str(message.chat.id) in joinedUsers:
        if message.chat.id != 1647407069 and message.chat.id != 490371324:
            joinedFile = open('joined.txt', 'a')
            joinedFile.write(str(message.chat.id) + '\n')
            joinedUsers.add(message.chat.id)

# ЧТОБЫ СДЕЛАТЬ КОМАНДЫ ДЛЯ АДМИНА, ПРОВЕРЯЕМ ЕСТЬ ЛИ В НАШЕМ ФАЙЛЕ АДМИНОВ АЙДИ ЭТОГО ЧЕЛОВЕКА. ЕСЛИ НЕТ ТО ВЫПОЛНЯЕТСЯ СЛЕДУЮЩАЯ ФУНКЦИЯ
    if not str(message.chat.id) in adminUsers:
        state = dbworker.get_current_state(message.chat.id)
        if state == config.States.S_USER.value:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='Мероприятия', callback_data='Events')
            b2 = types.InlineKeyboardButton(text='Мои заявки', callback_data='AllClaims')
            b3 = types.InlineKeyboardButton(text='Контакты', callback_data='Contacts')
            keyboard.add(b1, b2, b3)
            bot.send_message(id, 'Приветствуем в нашем боте!!!'
                                 '\nВо вкладке "Мероприятия" вы можете оставить заявку на одно из мероприятий Лицея «Сириус»'
                                 '\n\nВыберите тот вариант который вам нужен:', reply_markup=keyboard)
        else:
            dbworker.set_state(message.chat.id, config.States.S_START.value)
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='Мероприятия', callback_data='Events')
            b2 = types.InlineKeyboardButton(text='Мои заявки', callback_data='AllClaims')
            b3 = types.InlineKeyboardButton(text='Контакты', callback_data='Contacts')
            keyboard.add(b1, b2, b3)
            bot.send_message(id, 'Приветствуем в нашем боте!!!'
                                 '\nВо вкладке "Мероприятия" вы можете оставить заявку на одно из мероприятий Лицея «Сириус»'
                                 '\n\nВыберите тот вариант который вам нужен:', reply_markup=keyboard)
# ЕСЛИ ЕСТЬ, ТО ВЫВОДИМ МЕНЮ ДЛЯ АДМИНИСТРАТОРА
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton(text='Все заявки', callback_data='AllClaims')
        b2 = types.InlineKeyboardButton(text='Отправить сообщение 1 человеку', callback_data='SendMessageOne')
        b3 = types.InlineKeyboardButton(text='Отправить сообщение всем', callback_data='SendMessageAll')
        b4 = types.InlineKeyboardButton(text='Рекламное сообщение', callback_data='SendAdvertisement')
        b5 = types.InlineKeyboardButton(text='Создать мероприятие', callback_data='CreateEvent')
        b6 = types.InlineKeyboardButton(text='Другие функции', callback_data='StartAdmin')
        keyboard.add(b1, b2, b3, b4, b5, b6)
        bot.send_message(message.chat.id,
                         'Вот функции админа. Хотите посмотреть функции бота, нажмите «Другие функции»', reply_markup=keyboard)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME_1.value)
def user_name(message):
    name = message.text
    claim1s[message.chat.id, 'name'] = name
    bot.send_message(message.chat.id, "Приятно познакомиться! Теперь укажи, сколько нужно забронировать мест:")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_PEOPLE_1.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME_2.value)
def user_name(message):
    name = message.text
    claim2s[message.chat.id, 'name'] = name
    bot.send_message(message.chat.id, "Приятно познакомиться! Теперь укажи, сколько нужно забронировать мест:")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_PEOPLE_2.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_PEOPLE_1.value)
def user_age(message):
    people = message.text
    claim1s[message.chat.id, 'people'] = people
    for i in range(int(people)):
        claim1[len(claim1)] = len(claim1)
    bot.send_message(message.chat.id, "Мы забронировали эти места. Теперь введи номер телефона:")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NUMBER_1.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_PEOPLE_2.value)
def user_age(message):
    people = message.text
    claim2s[message.chat.id, 'people'] = people
    for i in range(int(people)):
        claim2[len(claim2)] = len(claim2)
    bot.send_message(message.chat.id, "Теперь введи номер телефона:")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NUMBER_2.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NUMBER_1.value)
def user_number(message):
    number = message.text
    claim1s[message.chat.id, 'number'] = number
    allclaims[message.chat.id, f'Claim №{len(allclaims)}'] = f"Мероприятие: Олимпиадная программа по биологии\nИмя: {claim1s[message.chat.id, 'name']}\nКоличесво человек: {claim1s[message.chat.id, 'people']}\nНомер телефона: {claim1s[message.chat.id, 'number']}\nВремя: 15:00\nДата: 1-24 сентября 2021 года"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text='Продолжить »', callback_data='Start')
    keyboard.add(b1)
    data = f"Мероприятие: Олимпиадная программа по биологии №{len(allclaims)}" \
           f"\nИмя: {claim1s[message.chat.id, 'name']}" \
           f"\nКоличесво человек: {claim1s[message.chat.id, 'people']}" \
           f"\nВремя: 15:00" \
           f"\nДата: 1-24 сентября 2021 года"
    filename = "qr1.png"
    img = qrcode.make(data)
    img.save(filename)
    file = open('qr1.png', 'rb')
    bot.send_photo(message.chat.id, file, f"\n\n{claim1s[message.chat.id, 'name']}, заявка №{int(len(allclaims)) - 1} успешно создана"
                                      f"\nВот ваш индивидуальный билет. В день мероприятия он вам понадобится на входе в Сириус",
                          reply_markup=keyboard)
    file.close()
    for user in adminUsers:
        file = open('qr1.png', 'rb')
        bot.send_photo(user, file, f"Заявка №{int(len(allclaims)) - 1} на мероприятие: Олимпиадная программа по биологии")
        file.close()
    dbworker.set_state(message.chat.id, config.States.S_START.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NUMBER_2.value)
def user_number(message):
    number = message.text
    claim2s[message.chat.id, 'number'] = number
    allclaims[message.chat.id, f'Claim №{len(allclaims)}'] = f"Мероприятие: Финансовая кибербезопасность 2.0\nИмя: {claim2s[message.chat.id, 'name']}\nКоличесво человек: {claim2s[message.chat.id, 'people']}\nНомер телефона: {claim2s[message.chat.id, 'number']}\nВремя: 17:00\nДата: 20-27 сентября 2021 года"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text='Продолжить »', callback_data='Start')
    keyboard.add(b1)
    data = f"Мероприятие: Олимпиадная программа по биологии №{len(allclaims)}" \
           f"\nИмя: {claim2s[message.chat.id, 'name']}" \
           f"\nКоличесво человек: {claim2s[message.chat.id, 'people']}" \
           f"\nВремя: 17:00" \
           f"\nДата: 20-27 сентября 2021 года"
    filename = "qr2.png"
    img = qrcode.make(data)
    img.save(filename)
    file = open('qr2.png', 'rb')
    bot.send_photo(message.chat.id, file, f"\n\n{claim2s[message.chat.id, 'name']}, заявка №{int(len(allclaims)) - 1} успешно создана"
                                      f"\nВот ваш индивидуальный билет. В день мероприятия он вам понадобится на входе в Сириус",
                          reply_markup=keyboard)
    file.close()
    for user in adminUsers:
        file = open('qr2.png', 'rb')
        bot.send_photo(user, file, f"Заявка №{int(len(allclaims)) - 1} на мероприятие: Финансовая кибербезопасность 2.0")
        file.close()
    dbworker.set_state(message.chat.id, config.States.S_START.value)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'Start':
        try:
            if not str(call.message.chat.id) in adminUsers:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                b1 = types.InlineKeyboardButton(text='Мероприятия', callback_data='Events')
                b2 = types.InlineKeyboardButton(text='Мои заявки', callback_data='AllClaims')
                b3 = types.InlineKeyboardButton(text='Контакты', callback_data='Contacts')
                keyboard.add(b1, b2, b3)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Приветствуем в нашем боте!!!'
                                           '\nВо вкладке "Мероприятия" вы можете оставить заявку на одно из мероприятий Лицея «Сириус»'
                                           '\n\nВыберите тот вариант который вам нужен:', reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                b1 = types.InlineKeyboardButton(text='Все заявки', callback_data='AllClaims')
                b2 = types.InlineKeyboardButton(text='Отправить сообщение 1 человеку', callback_data='SendMessageOne')
                b3 = types.InlineKeyboardButton(text='Отправить сообщение всем', callback_data='SendMessageAll')
                b4 = types.InlineKeyboardButton(text='Рекламное сообщение', callback_data='SendAdvertisement')
                b5 = types.InlineKeyboardButton(text='Другие функции', callback_data='StartAdmin')
                keyboard.add(b1, b2, b3, b4, b5)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Вот функции админа.'
                                           '\nХотите посмотреть функции бота, нажмите «Другие функции»',
                                      reply_markup=keyboard)
        except:
            if not str(call.message.chat.id) in adminUsers:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                b1 = types.InlineKeyboardButton(text='Мероприятия', callback_data='Events')
                b2 = types.InlineKeyboardButton(text='Мои заявки', callback_data='AllClaims')
                b3 = types.InlineKeyboardButton(text='Контакты', callback_data='Contacts')
                keyboard.add(b1, b2, b3)
                bot.send_message(call.message.chat.id, 'Приветствуем в нашем боте!!!'
                                           '\nВо вкладке "Мероприятия" вы можете оставить заявку на одно из мероприятий Лицея «Сириус»'
                                           '\n\nВыберите тот вариант который вам нужен:', reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                b1 = types.InlineKeyboardButton(text='Все заявки', callback_data='AllClaims')
                b2 = types.InlineKeyboardButton(text='Отправить сообщение 1 человеку', callback_data='SendMessageOne')
                b3 = types.InlineKeyboardButton(text='Отправить сообщение всем', callback_data='SendMessageAll')
                b4 = types.InlineKeyboardButton(text='Рекламное сообщение', callback_data='SendAdvertisement')
                b5 = types.InlineKeyboardButton(text='Другие функции', callback_data='StartAdmin')
                keyboard.add(b1, b2, b3, b4, b5)
                bot.send_message(call.message.chat.id, 'Вот функции админа.'
                                           '\nХотите посмотреть функции бота, нажмите «Другие функции»',
                                      reply_markup=keyboard)

    if call.data == 'StartAdmin':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton(text='Мероприятия', callback_data='Events')
        b2 = types.InlineKeyboardButton(text='Мои заявки', callback_data='AllClaims')
        b3 = types.InlineKeyboardButton(text='Контакты', callback_data='Contacts')
        keyboard.add(b1, b2, b3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Приветствуем в нашем боте!!!'
                                   '\nВо вкладке "Мероприятия" вы можете оставить заявку на одно из мероприятий Лицея «Сириус»'
                                   '\n\nВыберите тот вариант который вам нужен:', reply_markup=keyboard)

    if call.data == 'Events':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton(text='Олимпиадная программа по биологии', callback_data='Claim1')
        b2 = types.InlineKeyboardButton(text='Финансовая кибербезопасность 2.0', callback_data='Claim2')
        b3 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Start')
        keyboard.add(b1, b2, b3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вот список всех мероприятий. Если хотите посмотреть меропрятие с описанием нажмите на него. '
                                   'И там же можно оставить заявку.', reply_markup=keyboard)

    if call.data == 'Claim1':
        try:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='QR-Код мероприятия', callback_data='qrclaim1')
            b2 = types.InlineKeyboardButton(text='Подать заявку', callback_data='Claim1Send')
            b3 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Events')
            keyboard.add(b1, b2, b3)
            if len(claim1) >= 1 and len(claim1) <= 70:
                number = 70 - int(len(claim1))
            elif len(claim1) > 70:
                number = 'нет'
            else:
                number = 70
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Олимпиадная программа по биологии пройдет в Образовательном центре с 1 по 24 сентября 2021 года'
                                       f'\n\nК участию в конкурсном отборе приглашаются учащиеся 9-11 классов (по состоянию на 1 сентября 2021 года) из всех регионов, показавшие высокие результаты на биологических олимпиадах. '
                                       f'Победители и призеры заключительного этапа Всероссийской олимпиады школьников приглашаются на программу без дополнительного отбора.'
                                       f'\n\nРуководителем программы выступит заместитель декана биологического факультета МГУ, член Центральной предметно-методической комиссии и член жюри заключительного этапа ВсОШ по биологии, '
                                       f'кандидат биологических наук Белякова Галина Алексеевна.'
                                       f'\n\nСписок кандидатов на участие в программе будет определен не позднее 9 августа.'
                                       f'\n\nСвободных мест: {number}'
                                       f'\nДата: 1-24 сентября 2021 года'
                                       f'\nВремя: 15:00', reply_markup=keyboard)
        except:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='QR-Код мероприятия', callback_data='qrclaim1')
            b2 = types.InlineKeyboardButton(text='Подать заявку', callback_data='Claim1Send')
            b3 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Events')
            keyboard.add(b1, b2, b3)
            if len(claim1) >= 1 and len(claim1) <= 70:
                number = 70 - int(len(claim1))
            elif len(claim1) > 70:
                number = 'нет'
            else:
                number = 70
            bot.send_message(call.message.chat.id, f'Олимпиадная программа по биологии пройдет в Образовательном центре с 1 по 24 сентября 2021 года'
                                       f'\n\nК участию в конкурсном отборе приглашаются учащиеся 9-11 классов (по состоянию на 1 сентября 2021 года) из всех регионов, показавшие высокие результаты на биологических олимпиадах. '
                                       f'Победители и призеры заключительного этапа Всероссийской олимпиады школьников приглашаются на программу без дополнительного отбора.'
                                       f'\n\nРуководителем программы выступит заместитель декана биологического факультета МГУ, член Центральной предметно-методической комиссии и член жюри заключительного этапа ВсОШ по биологии, '
                                       f'кандидат биологических наук Белякова Галина Алексеевна.'
                                       f'\n\nСписок кандидатов на участие в программе будет определен не позднее 9 августа.'
                                       f'\n\nСвободных мест: {number}'
                                       f'\nДата: 1-24 сентября 2021 года'
                                       f'\nВремя: 15:00', reply_markup=keyboard)

    if call.data == 'Claim2':
        try:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='QR-Код мероприятия', callback_data='qrclaim2')
            b2 = types.InlineKeyboardButton(text='Подать заявку', callback_data='Claim2Send')
            b3 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Events')
            keyboard.add(b1, b2, b3)
            if len(claim2) >= 1 and len(claim2) <= 70:
                number = 70 - int(len(claim2))
            elif len(claim2) > 70:
                number = 'нет'
            else:
                number = 70
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'На образовательном модуле студенты смогут попробовать себя в роли сотрудников службы защиты IT-систем финансовых организаций. '
                                       f'Обучение пройдет с 20 по 27 сентября 2021 года. '
                                       f'Организаторами программы выступают Финтех Хаб Банка России, Университет «Сириус» и ПАО «Ростелеком».'
                                       f'\n\nК участию в отборочных испытаниях приглашаются студенты (18+) очной формы обучения российских вузов: бакалавры, специалисты, магистранты и аспиранты. '
                                       f'Кандидатам нужно будет выполнить профильное тестирование и пройти собеседование.'
                                       f'\n\nЗаявки принимаются до 23 июля включительно.'
                                       f'\n\nСвободных мест: {number}'
                                       f'\nДата: 20-27 сентября 2021 года'
                                       f'\nВремя: 17:00', reply_markup=keyboard)
        except:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='QR-Код мероприятия', callback_data='qrclaim2')
            b2 = types.InlineKeyboardButton(text='Подать заявку', callback_data='Claim2Send')
            b3 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Events')
            keyboard.add(b1, b2, b3)
            if len(claim2) >= 1 and len(claim2) <= 70:
                number = 70 - int(len(claim2))
            elif len(claim2) > 70:
                number = 'нет'
            else:
                number = 70
            bot.send_message(call.message.chat.id, f'На образовательном модуле студенты смогут попробовать себя в роли сотрудников службы защиты IT-систем финансовых организаций. '
                                       f'Обучение пройдет с 20 по 27 сентября 2021 года. '
                                       f'Организаторами программы выступают Финтех Хаб Банка России, Университет «Сириус» и ПАО «Ростелеком».'
                                       f'\n\nК участию в отборочных испытаниях приглашаются студенты (18+) очной формы обучения российских вузов: бакалавры, специалисты, магистранты и аспиранты. '
                                       f'Кандидатам нужно будет выполнить профильное тестирование и пройти собеседование.'
                                       f'\n\nЗаявки принимаются до 23 июля включительно.'
                                       f'\n\nСвободных мест: {number}'
                                       f'\nДата: 20-27 сентября 2021 года'
                                       f'\nВремя: 17:00', reply_markup=keyboard)

    if call.data == 'qrclaim1':
        if len(claim1) >= 1 and len(claim1) <= 70:
            number = 70 - int(len(claim1))
        elif len(claim1) > 70:
            number = 'нет'
        else:
            number = 70
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton(text='Вернуться »', callback_data='Claim1')
        keyboard.add(b1)
        data = f"Мероприятие: Олимпиадная программа по биологии" \
               f"\nСвободных мест: {number}" \
               f"\nВремя: 15:00" \
               f"\nДата: 1-24 сентября 2021 года"
        filename = "qrclaim1.png"
        img = qrcode.make(data)
        img.save(filename)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='.')
        file = open('qrclaim1.png', 'rb')
        bot.send_photo(call.message.chat.id, file, f"Мероприятие: Олимпиадная программа по биологии"
                                                   f"\nСвободных мест: {number}"
                                                   f"\nВремя: 15:00"
                                                   f"\nДата: 1-24 сентября 2021 года", reply_markup=keyboard)
        file.close()

    if call.data == 'qrclaim2':
        if len(claim2) >= 1 and len(claim2) <= 70:
            number = 70 - int(len(claim2))
        elif len(claim2) > 70:
            number = 'нет'
        else:
            number = 70
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton(text='Вернуться »', callback_data='Claim2')
        keyboard.add(b1)
        data = f"Мероприятие: Финансовая кибербезопасность 2.0" \
               f"\nСвободных мест: {number}" \
               f"\nВремя: 17:00" \
               f"\nДата: 20-27 сентября 2021 года"
        filename = "qrclaim2.png"
        img = qrcode.make(data)
        img.save(filename)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='.')
        file = open('qrclaim2.png', 'rb')
        bot.send_photo(call.message.chat.id, file, f"Мероприятие: Финансовая кибербезопасность 2.0"
                                                   f"\nСвободных мест: {number}"
                                                   f"\nВремя: 17:00"
                                                   f"\nДата: 20-27 сентября 2021 года", reply_markup=keyboard)
        file.close()

    if call.data == 'Claim1Send':
        claim1s[call.message.chat.id, 'event'] = f'Олимпиадная программа по биологии'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Чтобы создать заявку напишите как вас зовут:')
        dbworker.set_state(call.message.chat.id, config.States.S_ENTER_NAME_1.value)

    if call.data == 'Claim2Send':
        claim2s[call.message.chat.id, 'event'] = f'Финансовая кибербезопасность 2.0'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Чтобы создать заявку напишите как вас зовут:')
        dbworker.set_state(call.message.chat.id, config.States.S_ENTER_NAME_2.value)

    if call.data == 'AllClaims':
        users = {}
        for user in adminUsers:
            users[str(user)] = str(user)
        if str(call.message.chat.id) in str(allclaims.keys()) and not str(call.message.chat.id) in users.keys():
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for key in allclaims.keys():
                title = str(key)
                text = title.replace(f"({call.message.chat.id}, '", "").strip()
                text_name = text.replace("')", "").rstrip()
                keyboard.add(types.InlineKeyboardButton(text=f'{str(text_name)}', callback_data=f'{title}'))
            b1 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Start')
            keyboard.add(b1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Вот ваши заявки', reply_markup=keyboard)

        elif str(call.message.chat.id) in users.keys():
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for key in allclaims.keys():
                title = str(key)
                text = title.replace(f"(", "").strip()
                text_name = text.replace(")", "").rstrip()
                keyboard.add(types.InlineKeyboardButton(text=f'{text_name}', callback_data=f'{key}'))
            b1 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Start')
            keyboard.add(b1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Вот все заявки', reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Start')
            keyboard.add(b1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Поданных заявок пока нет', reply_markup=keyboard)

    for key in allclaims.keys():
        if call.data == str(key):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton(text='« Вернуться', callback_data='AllClaims')
            keyboard.add(b1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f'{allclaims[key]}', reply_markup=keyboard)

    if call.data == 'Contacts':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        b1 = types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/sirius.lyceum/')
        b2 = types.InlineKeyboardButton(text='ВК', url='https://vk.com/sirius.lyceum')
        b3 = types.InlineKeyboardButton(text='Наш сайт', url='https://siriuslyceum.ru/')
        b4 = types.InlineKeyboardButton(text='« Вернуться', callback_data='Start')
        keyboard.add(b1, b2, b3, b4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вот наши социальные сети:', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def saw(message):
    msg = message.text
    if msg == 'Я админ':
        if not str(message.chat.id) in adminUsers:
            adminFile = open('admin.txt', 'a')
            adminFile.write(str(message.chat.id) + '\n')
            adminUsers.add(message.chat.id)


bot.polling(none_stop = True, interval = 0)