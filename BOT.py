import telebot
import traceback
from config import coins
from extensions import APIException, Convertor

bot = telebot.TeleBot("5761082196:AAFzhaCszfyzGJvA6-zoCib08CFFc2BSDrM")


@bot.message_handler(commands=['start', 'help'])
def helping(message: telebot.types.Message):
    text = "Здравствуйте! Чтобы использовать функционал бота введите: \n<имя валюты> \
<в какую требуется конвертировать> \
<количество валюты>"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for coin in coins.keys():
        text = '\n'.join((text, coin))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(non_stop=True)