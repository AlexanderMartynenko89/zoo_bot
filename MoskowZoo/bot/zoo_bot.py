import telebot
import random
import tkinter
from config import TOKEN
from extensions import InputException
from questions import QuestionsAboutAnimals


#1. Регистрация бота
bot = telebot.TeleBot(TOKEN)


#2. Начало работы с ботом (/start и /help).
@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = ('Здравствуй! Ты попал на викторину, связанную с Московским зоопарком, \
на тему "Какое у вас тотемное животное?". \n\nГотовы ли вы погрузиться в один из самых популярных \
зоопарков Европы, познакомиться с его обитателями в форме викторины и весело провести время? \n\n\
Ответь на это сообщение "Да", если готов, и "Нет", если тебе неинтересно.')
    bot.send_message(message.chat.id, text)


#3. Ответ пользователя + Отлов ошибки.
@bot.message_handler(content_types=['text'])
def answer(message: telebot.types.Message):
    message.text = message.text.lower()
    try:
        if message.text != "да":
            if message.text != "нет":
                raise InputException("Кажется вы ввели не то значение!")

    except InputException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    else:
        text = ("Хорошо, тогда приступим! \n\n\
В нашей викторине будет 15 вопросов, отвечая на которые, вы сможете узнать свое тотемное животное. \n\n\
Начинаем!")
        bot.send_message(message.chat.id, text)

    if message.text == 'да':
        quest()


#4. Бот задает вопросы
def quest(message: telebot.types.Message):
    tt = random.sample(list(QuestionsAboutAnimals), 15)
    k = 0  # Счетчик вопросов.
    while k != 15:
        k += 1
        bot.send_message(message.chat.id, f'{k}. {tt[1]} \n{tt.values()}')


#5. Запуск бота.
bot.polling(none_stop=True)