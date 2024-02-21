import telebot
from config import TOKEN, keys
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:\n'
            '<имя интересующей валюты><в какой валюте представить>'
            '<количество интересующей валюты>\n'
            'Увидеть список всех доступных валют: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Указано неправильное количество параметров.')

        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}.'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
