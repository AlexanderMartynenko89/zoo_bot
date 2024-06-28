TOKEN = "7181163034:AAF4zRomdUzN0stWSM8lnaBKNAW7CJmXGoo"

'''
@bot.message_handler(commands=['button'])
def buttons_for_answer(message):
    global k
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    answer1 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][0])
    answer2 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][1])
    answer3 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][2])
    answer4 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][3])
    markup.add(answer1)
    markup.add(answer2)
    markup.add(answer3)
    markup.add(answer4)

    bot.send_message(message.chat.id, 'Выберите, правильный для вас, ответ:', reply_markup=markup)
    pass


k = 0
def start_quiz(message):
    global k
    output_question(message)
    buttons_for_answer(message)
    pass


def output_question(message):
    global k
    bot.send_message(message.chat.id, list(QuestionsAboutAnimals.items())[k][0])
    k += 1
    pass
'''
