import csv
import pandas as pd


def read_transactions_from_csv():
    """
    Читает финансовые операции из transactions.csv
    Возвращает список словарей (каждая строка = словарь)
    """
    transactions = []
    with open("transactions.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(dict(row))
    return transactions


def read_transactions_from_excel():
    """
    Читает финансовые операции из transactions_excel.xlsx
    Возвращает список словарей (каждая строка = словарь)
    """
    df = pd.read_excel("transactions_excel.xlsx")
    return df.to_dict("records")
