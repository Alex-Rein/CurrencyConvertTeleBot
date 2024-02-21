import json
import requests
from config import keys


class APIException(Exception):
    pass


class Converter:  # Класс обращения с API
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}".')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}".')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/5f5d0285607f966701778e6f/latest/{base_ticker}')
        rate = json.loads(r.content)['conversion_rates'][quote_ticker]

        return rate * amount
