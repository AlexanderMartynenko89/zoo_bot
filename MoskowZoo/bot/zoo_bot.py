import telebot
from config import TOKEN
from extensions import InputException

#1. Регистрация бота
bot = telebot.TeleBot(TOKEN)

#2. Начало работы с ботом (/start и /help).
@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = ("Здравствуй! Ты попал на викторину, связанную с Московским зоопарком, \
на тему 'Какое у вас тотемное животное?'. \n\nГотовы ли вы погрузиться в один из самых популярных \
зоопарков Европы, познакомиться с его обитателями в форме викторины и весело провести время? \n\n\
Ответь на это сообщение 'Да', если готов, и 'Нет', если тебе неинтересно.")
    bot.send_message(message.chat.id, text)

#3. Ответ пользователя + Отлов ошибки.
@bot.message_handler(content_types=['text'])
def answer(message: telebot.types.Message):
    try:
        if message.text != "да" and message.text != "Да" and message.text != "ДА" and message.text != "дА":
            raise InputException("Кажется вы ввели не то значение!")
        if message.text != "нет" and message.text != "Нет" and message.text != "НЕТ" and message.text != "нЕт" and message.text != "неТ" and message.text != "НЕт" and message.text != "нЕТ" and message.text != "НеТ":
            raise InputException("Кажется вы ввели не то значение!")

    except InputException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    else:
        text = "Хорошо, тогда приступим!"
        bot.send_message(message.chat.id, text)

#5. Запуск бота.
bot.polling(none_stop=True)