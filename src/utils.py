from src.external_api import convert_to_rub

import json


def load_transactions(file_path):
    """
    Загружает список транзакций из JSON-файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception:
        return []


def get_transaction_amount_rub(transaction: dict) -> float:
    """
    Возвращает сумму транзакции в рублях
    :param transaction: Словарь с данными транзакции
    :return: Сумма в рублях (float)
    """
    try:
        amount = float(transaction["amount"])
        currency = transaction.get("currency", "RUB").upper()

        if currency == "RUB":
            return amount

        return convert_to_rub(transaction)
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid transaction data: {str(e)}")
