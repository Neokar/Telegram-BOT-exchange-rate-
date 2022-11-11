import telebot
from settings import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = "Здравствуйте! Моя задача - конвертация валют.\nЧтобы начать работу, отправьте сообщение в следующем формате:\n<имя валюты> \
 <в какую валюту перевести> \
 <количество переводимой валюты>\nПример: доллар рубль 100\nУвидеть список всех доступных валют: /values\nЕсли что-то забыли, то вам поможет команда /help"
    bot.reply_to(message, text)


@bot.message_handler(commands=["help"])
def help(message:telebot.types.Message):
    text = "Чтобы начать работу, отправьте сообщение в следующем формате:\n<имя валюты> \
 <в какую валюту перевести> \
 <количество переводимой валюты>\nПример: доллар рубль 100\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("Некорректный запрос. Пример запроса: доллар рубль 100\nДоступные команды: /start /help /values")

        base, quote, amount = values
        total_base = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"На текущий момент {amount} {base.lower()} = {total_base} {quote.lower()}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
