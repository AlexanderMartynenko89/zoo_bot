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
    text = ('👋🏼 Здравствуй! Ты попал на викторину, связанную с Московским зоопарком, \
на тему "Какое у вас тотемное животное?". \n\nГотовы ли вы погрузиться в один из самых популярных \
зоопарков Европы, познакомиться с его обитателями в форме викторины и весело провести время? \n\n\
Тогда нажми на кнопку ниже – "Начать тест". \n\n‼️ Для дополнительной информации можете также связаться \
с сотрудником зоопарка, нажав по кнопке ниже.')
    bot.send_message(message.chat.id, text)
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
@bot.message_handler(func=lambda msg: msg.text == 'начать тест' or re.search(r'\d\.\s', msg.text))
def ask_question(message: types.Message):
    global k
    kb = output_question_and_answers(message)
    msg = bot.send_message(message.chat.id, text=list(QuestionsAboutAnimals.items())[k][0], reply_markup=kb)
    bot.register_next_step_handler(msg, ask_question)



# 8. Обработка ответа.
@bot.message_handler(func=lambda message: True)
def process_answer(message):
    pass


# 9. Запуск бота.
if __name__ == '__main__':
    bot.infinity_polling()