import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_data, expected",
    [
        # Тесты для счетов
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Счет 0000111122223333", "Счет **3333"),
        ("Счет 1234", "Счет **1234"),  # Минимальная длина
        # Тесты для карт
        ("Карта 1234567890123456", "Карта 1234 56** **** 3456"),
        ("Visa 1111222233334444", "Visa 1111 22** **** 4444"),
        ("МИР 9999888877776666", "МИР 9999 88** **** 6666"),
        ("Credit card 1234567890123456", "Credit card 1234 56** **** 3456"),
        # Некорректные данные
        ("Карта 1234", "Карта 1234"),  # Слишком короткий
        ("Карта 1234-5678-9012-3456", "Карта 1234-5678-9012-3456"),  # Дефисы
        ("Не карта", "Не карта"),  # Нет номера
        ("", ""),  # Пустая строка
        # Граничные случаи
        ("  Счет  12345678  ", "Счет **5678"),  # Лишние пробелы
        ("Карта    1234567890123456", "Карта 1234 56** **** 3456"),  # Много пробелов
    ],
)
def test_mask_account_card(input_data, expected):
    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize(
    "input_date, expected",
    [
        # Валидные даты
        ("2023-12-31", "31.12.2023"),
        ("2020-02-29T23:59:59", "29.02.2020"),
        ("1999-01-01T01:01:01.123Z", "01.01.1999"),
        # Невалидные данные
        ("", "Invalid date format"),
        ("2023", "Invalid date format"),
        ("2023-12", "Invalid date format"),
        ("31.12.2023", "Invalid date format"),
        (None, "Invalid date format"),
        (12345, "Invalid date format"),
    ],
)
def test_get_date(input_date, expected):
    assert get_date(input_date) == expected
