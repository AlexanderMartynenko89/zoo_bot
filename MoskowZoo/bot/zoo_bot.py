import telebot
import re
from telebot import types
from config import TOKEN
from extensions import InputException
from questions import QuestionsAboutAnimals


# 1. Регистрация бота
bot = telebot.TeleBot(TOKEN)


# 2. Начало работы с ботом (/start и /help).
@bot.message_handler(commands=['start', 'help'])
def start(message):
    photo = open("MZoo-logo since 1864-vert-rus_preview-01.jpg", "rb")
    text = ('👋🏼 Здравствуй! Ты попал на викторину, связанную с Московским зоопарком, \
на тему "Какое у вас тотемное животное?". \n\nГотовы ли вы погрузиться в один из самых популярных \
зоопарков Европы, познакомиться с его обитателями в форме викторины и весело провести время? \n\n\
Тогда нажми на кнопку ниже – "Начать тест". \n\n‼️ Для дополнительной информации можете также связаться \
с сотрудником зоопарка, нажав по кнопке ниже.')
    bot.send_message(message.chat.id, text)
    bot.send_photo(message.chat.id, photo=photo)
    button_start(message)


# 3. Вывод кнопок "Начать тест" и "Связаться с сотрудником зоопарка".
@bot.message_handler(commands=['button'])
def button_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("Начать тест")
    item2 = types.KeyboardButton("Связаться с сотрудником зоопарка")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Выберите то, что вам нужно:', reply_markup=markup)


# 4. Проверка ввода на ошибку.
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        if message.text.lower() != 'начать тест':
            if message.text.lower() != 'связаться с сотрудником зоопарка':
                raise InputException("Введено неправильное значение!")
        if message.text.lower() == 'начать тест':
            ask_question(message)
        elif message.text.lower() == 'связаться с сотрудником зоопарка':
            contact_zoo_staff(message)
    except InputException as e:
        bot.reply_to(message, f"Ошибка отправки сообщения: \n{e}")


# 5. Функция вывода контакта сотрудника зоопарка.
def contact_zoo_staff(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Связаться с сотрудником зоопарка", url="https://t.me/alexandetto")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Нажмите кнопку ниже:", reply_markup=keyboard)


# 6. Функция вывода кнопок с ответами.
k = -1
def output_question_and_answers(message):
    global k
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    k += 1
    for var in list(QuestionsAboutAnimals.items())[k][1]:
        buttons.append(types.KeyboardButton(text=var))
    keyboard.add(*buttons)

    return keyboard


# 7. Функция для закольцевания работы метода.
def ask_question(message: types.Message):
    global k
    if re.search(r'^(?:\d\.\s|Начать тест)', message.text):
        kb = output_question_and_answers(message)
        msg = bot.send_message(message.chat.id, text=list(QuestionsAboutAnimals.items())[k][0], reply_markup=kb)
    else:
        msg = bot.send_message(message.chat.id, text="Нажимайте на кнопки ниже, для того, чтобы дать ответ!")
    bot.register_next_step_handler(msg, process_answer)


# 8. Обработка ответа.
def process_answer(message):
    с1 = 0
    с2 = 0
    с3 = 0
    с4 = 0
    counts = {'1.': 0, '2.': 0, '3.': 0, '4.': 0}
    if output_question_and_answers(message) == buttons[0]:
        counts.update({'1.': с1 + 1})
    elif output_question_and_answers(message) == buttons[1]:
        counts.update({'2.': с2 + 1})
    elif output_question_and_answers(message) == buttons[2]:
        counts.update({'3.': с3 + 1})
    elif output_question_and_answers(message) == buttons[3]:
        counts.update({'4.': с4 + 1})

    return counts

def calculation_results(counts, message):
    max_count = max(counts.values())
    max_categories = [cat for cat, count in counts.items() if count == max_count]

    totem_info = {
        '1.': ("Волк - символизирует свободу и интуицию. Волки известны своей социальной организованностью, живут и охотятся в стаях, что говорит о их глубоких социальных связях. Они обладают выдающимися интуитивными способностями, помогающими им выживать в дикой природе. Волк также является символом свободы духа, смелости и независимости, он не боится идти своим путем.", "https://media.istockphoto.com/id/177794699/ru/%D1%84%D0%BE%D1%82%D0%BE/%D1%81%D0%B5%D1%80%D1%8B%D0%B9-%D0%B2%D0%BE%D0%BB%D0%BA-%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82.jpg?s=612x612&w=0&k=20&c=zTMmfuCxFPLGdvQkmS3Xb6MVY7E-wk5nf3lnuVbTc4Q="),
        '2.': ("Медведь - олицетворяет силу и уверенность. Медведь — мощное и внушающее уважение животное, которое символизирует лидерство и силу. Он также ассоциируется с защитой, внутренней уверенностью и самодостаточностью. Медведи способны к глубокому размышлению и медитации, особенно во время зимней спячки, что отражает их связь с более глубокими уровнями сознания и интуицией.", "https://img.freepik.com/free-photo/majestic-large-mammal-walking-in-snowy-forest-generative-ai_188544-36924.jpg"),
        '3.': ("Лошадь - символ свободы и мощи. Лошади — существа, излучающие элегантность и мощь, способные быстро двигаться и преодолевать препятствия. Они также ассоциируются со свободой, поскольку их грациозное движение и сила духа вдохновляют на освобождение от ограничений и следование своим желаниям.", "https://basetop.ru/wp-content/uploads/2019/03/itrttzwr.jpg"),
        '4.': ("Сова - мудрость и загадочность. Совы, с их способностью видеть в темноте, символизируют глубокую интуицию и знание тайного. Эти птицы часто ассоциируются с мудростью, поскольку их предполагаемая способность видеть то, что скрыто от других, делает их символом знания и загадочности.", "https://img.freepik.com/premium-photo/beautiful-owl_254845-8286.jpg"),
        ('1.', '2.'): ("Олень - изящество и спокойствие. Олени — элегантные животные, движения которых наполнены грацией и спокойствием. Они напоминают о важности быть легким на подъем и способным адаптироваться к изменениям, сохраняя при этом внутреннее спокойствие и достоинство.", "https://media.istockphoto.com/id/140157656/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82-%D0%B2%D0%B5%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9-%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D1%8B%D0%B9-%D0%BE%D0%BB%D0%B5%D0%BD%D1%8C-%D0%BE%D0%BB%D0%B5%D0%BD%D1%8C-%D0%B2-%D0%BE%D1%81%D0%B5%D0%BD%D1%8C-%D0%BE%D1%81%D0%B5%D0%BD%D1%8C.jpg?s=612x612&w=0&k=20&c=rCL1dxZz0DdUgcxYEH5a9VZzSpRV15Wx4RY9A_91ovE="),
        ('1.', '3.'): ("Дельфин - игривость и гармония. Дельфины известны своей дружелюбностью, интеллектом и любопытством. Они напоминают о важности поддерживать легкость бытия, наслаждаться общением и находить радость в простых вещах, поддерживая при этом гармонию с окружающим миром.", "https://img.freepik.com/free-photo/beautiful-dolphin-jumping-out-of-water_23-2150770795.jpg"),
        ('1.', '4.'): ("Пума - решительность и независимость. Пумы — сильные и независимые хищники, которые руководствуются своей интуицией и имеют сильный дух. Они олицетворяют смелость идти своим", "https://media.istockphoto.com/id/1392544996/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%BF%D1%83%D0%BC%D0%B0-%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82-%D0%BA%D1%80%D1%83%D0%BF%D0%BD%D1%8B%D0%BC-%D0%BF%D0%BB%D0%B0%D0%BD%D0%BE%D0%BC.jpg?s=612x612&w=0&k=20&c=6O2DD9DtRtRcjrlrZjXdONhEZK67Bn_rhjFG8YKAfP4="),
        ('2.', '3.'): ("Орёл - символизирует остроту зрения и свободу духа. Орлы обладают уникальной способностью видеть цели на большом расстоянии, не теряя при этом связи с землёй. Это животные, которые сочетают в себе как мощь, так и красоту, способные приспосабливаться к изменениям и преодолевать препятствия.", "https://static6.depositphotos.com/1000847/647/i/450/depositphotos_6474531-stock-photo-eagle-close-up.jpg"),
        ('2.', '4.'): ("Лиса - метафора хитрости и адаптивности. Лисы известны своей способностью выживать в различных условиях, используя острый ум и изобретательность. Они символизируют способность находить нестандартные решения и легко адаптироваться к новым обстоятельствам, сохраняя при этом уверенность и силу.", "https://media.istockphoto.com/id/516318760/ru/%D1%84%D0%BE%D1%82%D0%BE/red-fox-vulpes-vulpes.jpg?s=612x612&w=0&k=20&c=6ZbE9z2TK2Jf7ZuRzwZmm1p89jJebHCBe112cisRuj4="),
        ('3.', '4.'): ("Черепаха - представляет мудрость, долголетие и стойкость. Черепахи живут долго, двигаются медленно, но всегда достигают своей цели благодаря непоколебимой уверенности в себе и своих силах. Они напоминают о важности терпения, устойчивости перед лицом трудностей и способности сохранять спокойствие в любой ситуации.", "https://st.depositphotos.com/2021333/2715/i/450/depositphotos_27155705-stock-photo-green-sea-turtle.jpg"),
    }

    if len(max_categories) == 1:
        return totem_info[max_categories[0]]

    answ = bot.send_message(message.chat.id, text="Ваш ответ обработан!")
    bot.register_next_step_handler(answ, ask_question)


# 9. Запуск бота.
if __name__ == '__main__':
    bot.infinity_polling()