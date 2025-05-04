def filter_by_currency(transactions, currency):
    """Принимает на вход список словарей, представляющих транзакции.
    Функция возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной"""
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        curr = op_amount.get("currency", {})
        if curr.get("code") == currency:
            yield transaction


def transaction_descriptions(transactions):
    """Генератор, который возвращает описания транзакций по одной за раз."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start, end):
    """Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX"""
    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры и объединяем с пробелами
        formatted_card = " ".join([card_str[i : i + 4] for i in range(0, 16, 4)])
        yield formatted_card
