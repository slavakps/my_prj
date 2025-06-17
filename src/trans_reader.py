import csv
import pandas as pd
import re
from collections import Counter


def read_transactions_from_csv():
    """
    Читает финансовые операции из transactions.csv
    Возвращает список словарей (каждая строка = словарь)
    """
    transactions = []
    with open("data/transactions.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            transactions.append(dict(row))
    return transactions


def read_transactions_from_excel():
    """
    Читает финансовые операции из transactions_excel.xlsx
    Возвращает список словарей (каждая строка = словарь)
    """
    df = pd.read_excel("data/transactions_excel.xlsx")
    return df.to_dict("records")


import re


def filter_transactions_by_description(transactions: list[dict], sort_by_word: str) -> list[dict]:
    """
    Фильтрует список транзакций, оставляя только те, в описании которых встречается заданная строка.
    """
    while True:  # Основной цикл для проверки "да/нет"
        if sort_by_word.lower() == "да":
            search_string = input("Введите слово для поиска: ").strip()
            if not search_string:  # Проверка на пустой ввод
                print("Ошибка: поисковая строка не может быть пустой!")
                continue

            filtered_transactions = []
            for transaction in transactions:
                description = transaction.get('description', '')
                if re.search(search_string, description, re.IGNORECASE):
                    filtered_transactions.append(transaction)

            print(f"Найдено {len(filtered_transactions)} операций.")
            return filtered_transactions

        elif sort_by_word.lower() == "нет":
            return transactions

        else:
            print("Ошибка: введите 'да' или 'нет'!")
            sort_by_word = input("Хотите выполнить фильтрацию по описанию? (да/нет): ")


def count_transactions_by_categories(transactions: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций в каждой из заданных категорий.

    Args:
        transactions: Список словарей с данными о банковских операциях.
        categories: Список категорий для подсчета.

    Returns:
        Словарь, где ключи - названия категорий, а значения - количество операций в каждой категории.
    """
    descriptions = [transaction.get('description', '').lower() for transaction in transactions]
    category_counts = Counter()

    for category in categories:
        category_lower = category.lower()
        count = sum(1 for desc in descriptions if category_lower in desc)
        category_counts[category] = count

    return dict(category_counts)