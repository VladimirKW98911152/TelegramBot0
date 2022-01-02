import requests
import json
from configuration import keys

class ConvertionException(Exception):  # Создаем класс исключений
    pass

class get_price:  # Класс, который конвертирует валюты
    @staticmethod
    def convert(quote: str, base: str, amount: float):
        if quote == base:  # Исключение, которое выводит в чат сообщение о том, что нельзя менять валюту на саму себя
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]  # Исключение, срабатывающее в случае ввода валюты, не указанной в программе
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)  # Исключение, срабатывающее в случае, если вводится неправильное количество валюты
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]*amount

        return total_base


