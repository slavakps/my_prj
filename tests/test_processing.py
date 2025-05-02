import pytest

from src.processing import filter_by_state, sort_by_date

SAMPLE_DATA = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "PENDING"},
    {"id": 3, "state": "EXECUTED"},
    {"id": 4, "state": "CANCELED"},
    {"id": 5},  # Операция без статуса
]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("PENDING", [2]),
        ("CANCELED", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(state, expected_ids):
    """Тестирует фильтрацию по разным статусам"""
    result = filter_by_state(SAMPLE_DATA, state)
    assert [op["id"] for op in result] == expected_ids


def test_default_state():
    """Тестирует фильтрацию со статусом по умолчанию (EXECUTED)"""
    result = filter_by_state(SAMPLE_DATA)
    assert [op["id"] for op in result] == [1, 3]


def test_empty_input():
    """Тестирует работу с пустым списком операций"""
    assert filter_by_state([]) == []
    assert filter_by_state([], "EXECUTED") == []
    assert filter_by_state([], "PENDING") == []


def test_operations_without_state():
    """Тестирует обработку операций без поля state"""
    test_data = [{"id": 1}, {"id": 2}, {"id": 3}]
    assert filter_by_state(test_data, "EXECUTED") == []


def test_sort_by_date_ascending():
    """Сортировка по возрастанию даты"""
    operations = [
        {"date": "2023-01-15"},
        {"date": "2023-01-10"},
        {"date": "2023-01-20"},
    ]
    expected = [
        {"date": "2023-01-10"},
        {"date": "2023-01-15"},
        {"date": "2023-01-20"},
    ]
    assert sort_by_date(operations) == expected


def test_sort_by_date_descending():
    """Сортировка по убыванию даты"""
    operations = [
        {"date": "2023-01-15"},
        {"date": "2023-01-10"},
        {"date": "2023-01-20"},
    ]
    expected = [
        {"date": "2023-01-20"},
        {"date": "2023-01-15"},
        {"date": "2023-01-10"},
    ]
    assert sort_by_date(operations, reverse=True) == expected


def test_sort_by_date_same_dates():
    """Проверка сортировки при одинаковых датах"""
    operations = [
        {"date": "2023-01-15", "id": 1},
        {"date": "2023-01-15", "id": 2},
        {"date": "2023-01-15", "id": 3},
    ]
    assert sort_by_date(operations) == operations


def test_sort_by_date_invalid_format():
    """Тест сортировки с некорректными датами."""
    operations = [
        {"date": "2023-01-15T12:00:00"},
        {"date": "некорректная дата"},
        {"date": "2023-01-20T18:45:00"},
    ]
    expected = [
        {"date": "2023-01-15T12:00:00"},
        {"date": "2023-01-20T18:45:00"},
        {"date": "некорректная дата"},
    ]
    assert sort_by_date(operations) == expected
