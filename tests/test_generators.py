import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD", "name": "USD"}}},
        {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "EUR", "name": "Euro"}}},
        {"id": 3, "operationAmount": {"amount": "300", "currency": {"code": "USD", "name": "USD"}}},
        {"id": 4, "operationAmount": {"amount": "400"}},  # Транзакция без указания валюты (тест на устойчивость)
    ]


def test_filter_usd(sample_transactions):
    """Фильтрация по валюте USD"""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    assert all(tx["operationAmount"]["currency"]["code"] == "USD" for tx in usd_transactions)


def test_filter_eur(sample_transactions):
    """Фильтрация по валюте EUR"""
    eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(eur_transactions) == 1
    assert eur_transactions[0]["id"] == 2


def test_no_matching_currency(sample_transactions):
    """Отсутствие транзакций в заданной валюте (RUB)"""
    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
    assert len(rub_transactions) == 0


def test_empty_transactions():
    """Пустой список транзакций"""
    empty_transactions = []
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert len(result) == 0


def test_missing_currency_field(sample_transactions):
    """Транзакции без поля 'currency' (устойчивость к ошибкам)"""
    broken_tx = {"id": 5, "operationAmount": {"amount": "500"}}
    transactions = sample_transactions + [broken_tx]

    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 2
    assert all(tx["id"] in (1, 3) for tx in usd_transactions)


def test_transaction_descriptions():
    """Обычный случай (несколько транзакций)"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
    ]
    gen = transaction_descriptions(transactions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод с карты на карту"

    """Пустой список транзакций"""
    empty_transactions = []
    gen = transaction_descriptions(empty_transactions)
    try:
        next(gen)
        assert False, "Ожидалось исключение StopIteration для пустого списка"
    except StopIteration:
        pass

    """Одна транзакция"""
    single_transaction = [{"description": "Оплата услуг"}]
    gen = transaction_descriptions(single_transaction)
    assert next(gen) == "Оплата услуг"
    try:
        next(gen)
        assert False, "Ожидалось исключение StopIteration после первой транзакции"
    except StopIteration:
        pass


def test_small_range():
    """Проверяет генерацию небольшого диапазона номеров (1-5)"""
    result = list(card_number_generator(1, 5))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert result == expected


def test_format_correctness():
    """Проверяет корректность форматирования различных номеров карт"""
    test_cases = [
        (1, "0000 0000 0000 0001"),
        (9999, "0000 0000 0000 9999"),
        (10000, "0000 0000 0001 0000"),
        (9999999999999999, "9999 9999 9999 9999"),
    ]
    for number, expected in test_cases:
        assert next(card_number_generator(number, number)) == expected


def test_edge_cases():
    """Проверяет обработку граничных значений диапазона"""
    assert next(card_number_generator(1, 1)) == "0000 0000 0000 0001"
    assert next(card_number_generator(9999999999999999, 9999999999999999)) == "9999 9999 9999 9999"
    assert list(card_number_generator(42, 42)) == ["0000 0000 0000 0042"]


def test_large_range():
    """Проверяет обработку большого диапазона значений"""
    gen = card_number_generator(9999999999999995, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9995"
    assert next(gen) == "9999 9999 9999 9996"
    assert next(gen) == "9999 9999 9999 9997"
    assert next(gen) == "9999 9999 9999 9998"
    assert next(gen) == "9999 9999 9999 9999"


def test_empty_range():
    """Проверяет обработку пустого диапазона (когда start > end)"""
    assert list(card_number_generator(10, 5)) == []
    assert list(card_number_generator(2, 1)) == []


