from datetime import datetime
import json
import logging
from pathlib import Path
from src.external_api import convert_to_rub
from src.generators import filter_by_currency

# Настройка логгера для модуля
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Путь к файлу логов
LOG_PATH = "C:/Users/Admin/PycharmProjects/my_prj/logs/utils.log"
file_handler = logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Форматтер для логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)

def load_transactions(file_path="C:\\Users\\Admin\\PycharmProjects\\my_prj\\data\\operations.json"):
    """
    Загружает список транзакций из JSON-файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Успешно загружены транзакции из файла {file_path}")
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка при загрузке транзакций: {str(e)}")
        return []


def get_transaction_amount_rub(transaction) -> float:
    """
    Возвращает сумму транзакции в рублях
    :param transaction: Словарь с данными транзакции
    :return: Сумма в рублях (float)
    """
    user_input = input()
    try:
        amount = float(transaction["amount"])
        currency = transaction.get("currency", "RUB").upper()
        if currency == "RUB":
            logger.debug(f"Транзакция в RUB: {amount}")
            return amount
        converted_amount = convert_to_rub(transaction)
        logger.debug(f"Конвертированная сумма: {converted_amount} (из {amount} {currency})")
        return converted_amount
    except KeyError as e:
        error_msg = f"Отсутствует ключ в данных транзакции: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except ValueError as e:
        error_msg = f"Некорректное значение в данных транзакции: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Неизвестная ошибка при обработке транзакции: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

def sort_by_rub(data: list)-> list:
    """Фильтрация по валюте"""
    rub_transaction = input()
    if rub_transaction.lower() == "да":
        data = filter_by_currency(data, currency="RUB")
    return list(data)

# Инициализация
logger.info("Модуль utils инициализирован")
transactions = load_transactions()
