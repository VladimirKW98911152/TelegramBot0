import telebot
from configuration import keys, TOKEN
from extensions import ConvertionException, get_price


bot = telebot.TeleBot(TOKEN)  # Привязываем создаваемого бота к токену бота, зарегистрированного в телеграм


@bot.message_handler(commands=['start', 'help'])  # Обработчик с инструкцией о том, как работать с ботом
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: ' \
'\n <имя валюты, цену которой Вы хотите узнать> ' \
'\n <имя валюты, в которой надо узнать цену первой валюты> ' \
'\n <количество первой валюты> ' \
'\n Вводимые данные должны быть в одной строке' \
'\n Например если желаете узнать стоимость 50 долларов в рублях,' \
'\n Вам нужно ввести так: доллар рубль 50' \
'\n ! Просмотреть доступные валюты можно с помощью команды "/values"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])  # Обработчик, отвечающий за публикацию в чате списка доступных валют
def walues(message: telebot.types.Message):
    text = 'Доступные валюты:'  # Выводит (публикует) в чате заголовок списка доступных валют
    for key in keys.keys():  # Если введено название валюты, содержащееся в переменной keys (словарь с названиями валют)
        text = '\n'.join((text, key, ))  # Сочетание метода .join и управляющего символа \n, будет переводить название
    bot.reply_to(message, text)   # валют на следующую строчку


@bot.message_handler(content_types=['text', ])  # Обработчик, который будет обрабатывать запросы о стоимости кр.валют
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:  # Исключение, выводящее в чат сообщение о том, что нельзя отправлять в чат более трех слов
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)  # Это, чтобы сообщение отсылалось боту


bot.polling()  # Команда, запускающая бота