import os
from typing import Dict, Union

from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.apilayer.com/exchangerates_data")


def get_exchange_rate(target_currency: str) -> float:
    """Получает текущий курс валюты к RUB"""
    try:
        response = requests.get(
            f"{BASE_URL}/latest",
            params={"symbols": "RUB", "base": target_currency},
            headers={"apikey": API_KEY},
            timeout=5,
        )
        response.raise_for_status()
        return response.json()["rates"]["RUB"]
    except (requests.RequestException, KeyError) as e:
        raise ValueError(f"Failed to get exchange rate: {str(e)}")


def convert_to_rub(transaction: Dict[str, Union[str, float]]) -> float:
    """
    Конвертирует сумму транзакции в рубли
    :param transaction: Словарь с данными транзакции
    :return: Сумма в рублях (float)
    """
    amount = float(transaction["amount"])
    currency = transaction.get("currency", "RUB").upper()

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(f"Unsupported currency: {currency}")

    rate = get_exchange_rate(currency)
    return round(amount * rate, 2)
