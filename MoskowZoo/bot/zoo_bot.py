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
    bot.send_message(message.chat.id, '⬇️ Выберите то, что вам нужно, нажав по кнопке ниже', reply_markup=markup)


# 4. Проверка ввода на ошибку.
@bot.message_handler(func=lambda message: message.text.lower() == 'начать тест' or message.text.lower() == 'связаться с сотрудником зоопарка' or message.text.lower() == 'сыграть снова' or message.text.lower() == 'закончить игру' or message.text.lower() == 'перейти на официальный сайт московского зоопарка' or message.text.lower() == 'расскажите мне о программе опеки')
def handle_text(message):
    try:
        if message.text.lower() == 'начать тест' or message.text.lower() == 'сыграть снова':
            ask_question(message)
        elif message.text.lower() == 'связаться с сотрудником зоопарка':
            contact_zoo_staff(message)
        elif message.text.lower() == 'перейти на официальный сайт московского зоопарка':
            MoskowZooSite(message)
        elif message.text.lower() == 'закончить игру':
            end_game(message)
        elif message.text.lower() == 'расскажите мне о программе опеки':
            guardianship_program(message)
    except InputException as e:
        bot.reply_to(message, f"‼️ Ошибка отправки сообщения: \n{e}")


# 5. Функция вывода контакта сотрудника зоопарка.
def contact_zoo_staff(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Связаться с сотрудником зоопарка", url="https://t.me/alexandetto")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "⬇️ Вы можете связаться с сотрудником зоопарка, нажав по кнопке ниже:", reply_markup=keyboard)


# 6. Функция вывода кнопок с ответами.
def output_question_and_answers(message, k):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for var in list(QuestionsAboutAnimals.items())[k][1]:
        buttons.append(types.KeyboardButton(text=var))
    keyboard.add(*buttons)

    return keyboard


# 7. Функция для отправки вопроса.
def ask_question(message: types.Message, k=-2, counts=None):
    if counts is None:
        counts = {'1': 0, '2': 0, '3': 0, '4': 0}
    if k != len(QuestionsAboutAnimals) - 2:
        k += 1
        kb = output_question_and_answers(message, k)
        msg = bot.send_message(message.chat.id, text=list(QuestionsAboutAnimals.items())[k][0], reply_markup=kb)
        bot.register_next_step_handler(msg, process_answer, k, counts)
    else:
        bot.send_message(message.chat.id, text='Тест завершён! 🥳\n\nИиии, Ваше тотемное животное...', reply_markup=types.ReplyKeyboardRemove())
        calculation_results(counts, message)


# 8. Функция для обработки ответа.
@bot.message_handler()
def process_answer(message: types.Message, k, counts):
    try:
        if re.search(r'^([1-4]\.\s)', message.text):
            counts[message.text[0]] += 1
            ask_question(message, k, counts)
        else:
            raise InputException("– Нажимайте на кнопки ниже, для того, чтобы дать ответ!")
    except InputException as e:
        bot.reply_to(message, f"‼️ Ошибка отправки сообщения: \n{e}")
        ask_question(message, k-1, counts)

    print(counts)


# 9. Функция для подсчета ответов.
def calculation_results(counts, message):
    max_count = max(counts.values())
    max_categories = [cat for cat, count in counts.items() if count == max_count]

    totem_info = {
        '1': ("🐺 Волк — символизирует свободу и интуицию. Волки известны своей социальной организованностью, живут и охотятся в стаях, что говорит о их глубоких социальных связях. Они обладают выдающимися интуитивными способностями, помогающими им выживать в дикой природе. Волк также является символом свободы духа, смелости и независимости, он не боится идти своим путем.", "CAACAgIAAxkBAAEMcGBmh7RGtirsKplZgx9YvyxQRmEyWwAClU4AAos6QUgfEYkYUBjSWTUE"),
        '2': ("🐻 Медведь — олицетворяет силу и уверенность. Медведь — мощное и внушающее уважение животное, которое символизирует лидерство и силу. Он также ассоциируется с защитой, внутренней уверенностью и самодостаточностью. Медведи способны к глубокому размышлению и медитации, особенно во время зимней спячки, что отражает их связь с более глубокими уровнями сознания и интуицией.", "CAACAgIAAxkBAAEMcERmh7Mad_ihHUzkfXmugJuphwqJXgACvEwAAtQxQEjFAVvyRljyuzUE"),
        '3': ("🐎 Лошадь — символ свободы и мощи. Лошади — существа, излучающие элегантность и мощь, способные быстро двигаться и преодолевать препятствия. Они также ассоциируются со свободой, поскольку их грациозное движение и сила духа вдохновляют на освобождение от ограничений и следование своим желаниям.", "CAACAgIAAxkBAAEMcEZmh7MrlBV0UKCxcygMaehX1yanZgACwEUAApKHQUglNOHSSuR1FTUE"),
        '4': ("🦉 Сова — мудрость и загадочность. Совы, с их способностью видеть в темноте, символизируют глубокую интуицию и знание тайного. Эти птицы часто ассоциируются с мудростью, поскольку их предполагаемая способность видеть то, что скрыто от других, делает их символом знания и загадочности.", "CAACAgIAAxkBAAEMcEhmh7M9ad02TGcYTYlaFjJfX1JHywACeVAAAskcQUi2TvgHTAOeAjUE"),
        ('1', '2'): ("🦌 Олень — изящество и спокойствие. Олени — элегантные животные, движения которых наполнены грацией и спокойствием. Они напоминают о важности быть легким на подъем и способным адаптироваться к изменениям, сохраняя при этом внутреннее спокойствие и достоинство.", "CAACAgIAAxkBAAEMcEpmh7NLj9rDva4HKN81qEO-zNjyLAACxVUAAl5SOUgeRzoC2oF01TUE"),
        ('1', '3'): ("🐬 Дельфин — игривость и гармония. Дельфины известны своей дружелюбностью, интеллектом и любопытством. Они напоминают о важности поддерживать легкость бытия, наслаждаться общением и находить радость в простых вещах, поддерживая при этом гармонию с окружающим миром.", "CAACAgIAAxkBAAEMcExmh7NaPnM6QCkbKDZtzibx2YPZ2gACFEsAAm9eOEgAAaGQN4mmMUQ1BA"),
        ('1', '4'): ("🐆 Пума — решительность и независимость. Пумы — сильные и независимые хищники, которые руководствуются своей интуицией и имеют сильный дух. Они олицетворяют смелость идти своим", "CAACAgIAAxkBAAEMcE5mh7No_l1FLehOM6VGtUwOkTzhKAACj0kAAoWqQEio0bZ8S_LIsDUE"),
        ('2', '3'): ("🦅 Орёл — символизирует остроту зрения и свободу духа. Орлы обладают уникальной способностью видеть цели на большом расстоянии, не теряя при этом связи с землёй. Это животные, которые сочетают в себе как мощь, так и красоту, способные приспосабливаться к изменениям и преодолевать препятствия.", "CAACAgIAAxkBAAEMcFBmh7N18Blq1KTEcYn-Wod0YfnNRwACvUsAAlmBOUjg4BfEqnoVWzUE"),
        ('2', '4'): ("🦊 Лиса — метафора хитрости и адаптивности. Лисы известны своей способностью выживать в различных условиях, используя острый ум и изобретательность. Они символизируют способность находить нестандартные решения и легко адаптироваться к новым обстоятельствам, сохраняя при этом уверенность и силу.", "CAACAgIAAxkBAAEMcFJmh7OCC4L-ZTUDiDpoiMgaK_1H8gACTUkAAqTRQEjbOnSrbi84ojUE"),
        ('3', '4'): ("🐢 Черепаха — представляет мудрость, долголетие и стойкость. Черепахи живут долго, двигаются медленно, но всегда достигают своей цели благодаря непоколебимой уверенности в себе и своих силах. Они напоминают о важности терпения, устойчивости перед лицом трудностей и способности сохранять спокойствие в любой ситуации.", "CAACAgIAAxkBAAEMcFRmh7OTUHm3i__iduQKG-ohSOkTbwAC9FEAAtXPOEhVDqgD_bwXlTUE"),
        ('1', '2', '3'): ("🐅 Тигр — тотемное животное, которое олицетворяет созидание и разрушение. Это животное с поистине королевским достоинством, сильное, властное, жестокое, мужественное и яростное. Все эти качества характеризуют его как защитника. Человек, находящийся под покровительством тотема тигра, является властителем собственной жизни. Этот тотем учит, что для достижения целей необходима настойчивость. Необходимо запастись терпением и использовать проверенные способы.", "CAACAgIAAxkBAAEMcFZmh7OrCoLMqp1eGxiqITRtqbBSUAACeEMAAhxbQUhXLUkIxF-URjUE"),
        ('1', '2', '4'): ("🦝 Енот — тотемное животное с обманчиво милой внешностью и удивительным характером. Его изображение наносили на тело с давних времен, чтобы перенять основные черты звериной натуры — ловкость и умение маскироваться. В современном мире тату с енотом обозначает неуловимую скрытность, несовпадение внешнего вида и внутренних ощущений.", "CAACAgIAAxkBAAEMcFhmh7O7_YRR6wWEaDXX9U-IXk5nwwACWUUAAqmPQUhRmwp5Mg70jzUE"),
        ('1', '3', '4'): ("🦁 Лев — символизирует силу, отвагу, могущество, королевскую власть, защиту, гордость, власть, величие и мудрость. И поскольку львицы являются основными охотниками прайда, львы также являются символами женской силы, свирепости и семьи. Эти существа одновременно бесстрашны и уверены в себе, что делает их символами королевской власти и отваги. Львы-самцы и самки также работают вместе, поднимая свою гордость, представляя силу, семью и защиту.", "CAACAgIAAxkBAAEMcFpmh7PK4bEb2aFhCpGSlhalk_uiSQACrk0AAlJdQEhOB7te0OCrljUE"),
        ('2', '3', '4'): ("🐿 Белка — активность и готовность. Белки всегда пребывают в движении и постоянно куда-то торопятся, совершая постоянные суетливые движения. Большую часть времени они проводят в поисках корма и создании его запасов на зиму, поскольку в спячку они не впадают. Готовясь к зиме, они интенсивно едят и наращивают вес, а также отращивают густой мех. Белки являются символами предусмотрительности и активности.", "CAACAgIAAxkBAAEMcFxmh7PcXzc9cNSOHASuMqXyeu_p7QACBVMAAvGjQEhxWtZurIgDmTUE"),
    }

    if len(max_categories) == 1:
        bot.send_message(message.chat.id, totem_info[str(max_categories[0])])
        bot.send_sticker(message.chat.id, list(totem_info.values())[int(max_categories[0]) - 1][1])
        final_choice(message)
    else:
        bot.send_message(message.chat.id, totem_info[tuple(sorted(max_categories))])
        bot.send_sticker(message.chat.id, totem_info[tuple(sorted(max_categories))][1])
        final_choice(message)


# 10. Функция, для предложения сыграть снова.
def final_choice(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button1 = types.KeyboardButton("Связаться с сотрудником зоопарка")
    button2 = types.KeyboardButton("Перейти на официальный сайт Московского Зоопарка")
    button3 = types.KeyboardButton("Расскажите мне о программе опеки")
    button4 = types.KeyboardButton("Сыграть снова")
    button5 = types.KeyboardButton("Закончить игру")

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    markup.add(button5)

    bot.send_message(message.chat.id, '⬇️ Выберите то, что вам нужно, нажав по кнопке ниже', reply_markup=markup)


# 11. Функция для перевода на сайт зоопарка.
def MoskowZooSite(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на сайт московского зоопарка", url="https://moscowzoo.ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "⬇️ Вы можете перейти на сайт зоопарка, нажав по кнопке ниже:", reply_markup=keyboard)


# 12. Функция, рассказывающая о программе опеки.
def guardianship_program(message):
    custody = ("Программа опеки от Московского зоопарка предоставляет уникальную возможность стать опекуном за \
конкретным животным, проживающим в зоопарке. Участвуя в этой программе, вы фактически поддерживаете выбранное вами \
животное, помогая обеспечить его уход, кормление и медицинское обслуживание.\n\nПроцесс участия в программе опеки \
обычно включает в себя выбор конкретного животного из числа доступных опекунству, заключение специального договора \
и уплату ежемесячного или ежегодного взноса. В качестве опекуна вы можете получить сертификат, фотографии вашего \
животного, регулярные обновления и информацию о жизни и благосостоянии вашего подопечного.\n\nДеньги, собранные от \
программы опеки, обычно направляются на улучшение условий содержания животных в зоопарке, их медицинское обслуживание, \
а также на проведение научных исследований и программы охраны природы.\n\nУчастие в программе опеки позволяет вам не \
только поддержать зоопарк, но и получить уникальный опыт взаимодействия с животным миру, а также быть частью \
благотворительной деятельности.")
    bot.send_message(message.chat.id, custody)


# 13. Функция окончания игры.
def end_game(message):
    bot.send_message(message.chat.id, "Отлично сыграли! ✅\n\n‼️ Переходите на сайт зоопарка, для получения большей \
информации о животных, по ссылке:\n\n– https://moscowzoo.ru\n– https://moscowzoo.ru\n– https://moscowzoo.ru")
    bot.stop_bot()


# 14. Запуск бота.
if __name__ == '__main__':
    bot.infinity_polling()
