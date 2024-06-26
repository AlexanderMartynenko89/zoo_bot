import telebot
from telebot import types
from config import TOKEN
from extensions import InputException
from questions import QuestionsAboutAnimals


#1. Регистрация бота
bot = telebot.TeleBot(TOKEN)


#2. Начало работы с ботом (/start и /help).
@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = ('👋🏼 Здравствуй! Ты попал на викторину, связанную с Московским зоопарком, \
на тему "Какое у вас тотемное животное?". \n\nГотовы ли вы погрузиться в один из самых популярных \
зоопарков Европы, познакомиться с его обитателями в форме викторины и весело провести время? \n\n\
Тогда нажми на кнопку ниже – "Начать тест". \n\n‼️ Для дополнительной информации можете также связаться \
с сотрудником зоопарка, нажав по кнопке ниже.')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['button'])
def button_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать тест")
    item2 = types.KeyboardButton("Связаться с сотрудником зоопарка")
    markup.add(item1)
    markup.add(item2)

    bot.send_message(message.chat.id, 'Выберите что вам нужно', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        if message.text == 'Начать тест':
            start_quiz(message)
        elif message.text == 'Начать тест заново':
            start_quiz(message)
        else:
            process_answer(message)
    except InputException as e:
        print(f"Ошибка отправки сообщения: {e}")


def start_quiz(message):
    pass


k = 0
def output_question(message):
    global k
    bot.send_message(message.chat.id, list(QuestionsAboutAnimals.items())[k][0])
    k += 1


@bot.message_handler(commands=['button'])
def buttons_for_answer(message):
    global k
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    answer1 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][0])
    answer2 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][1])
    answer3 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][2])
    answer4 = types.KeyboardButton(list(QuestionsAboutAnimals.items())[k][1][3])
    markup.add(answer1)
    markup.add(answer2)
    markup.add(answer3)
    markup.add(answer4)

    bot.send_message(message.chat.id, 'Выберите, правильный для вас, ответ:', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def process_answer(message):
    pass


#5. Запуск бота.
if __name__ == '__main__':
    bot.infinity_polling()