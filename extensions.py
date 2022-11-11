import requests
import json
from settings import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()
        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}. Введите команду /values для получения списка поддерживаемых валют.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}. Введите команду /values для получения списка поддерживаемых валют.")

        try:
            amount = float(amount)
            if amount < 0:
                raise APIException("Вы ввели отрицательное количество валюты")
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_base = json.loads(r.content)[keys[quote]] * amount

        return total_base
