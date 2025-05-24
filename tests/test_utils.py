from unittest.mock import patch

import pytest

from src.utils import load_transactions, get_transaction_amount_rub


def test_rub_transaction():
    transaction = {"amount": "100.50", "currency": "RUB"}
    assert get_transaction_amount_rub(transaction) == 100.50


def test_rub_transaction_default_currency():
    transaction = {"amount": "200.75"}
    assert get_transaction_amount_rub(transaction) == 200.75


def test_foreign_currency_transaction():
    """Тест транзакции в иностранной валюте (USD)"""
    transaction = {"amount": "50.00", "currency": "USD"}

    with patch("src.utils.convert_to_rub", return_value=3750.00) as mock_convert:
        result = get_transaction_amount_rub(transaction)

        mock_convert.assert_called_once_with(transaction)

        assert result == 3750.00
        assert isinstance(result, float)


def test_invalid_amount():
    transaction = {"amount": "invalid", "currency": "RUB"}
    with pytest.raises(ValueError, match="Invalid transaction data"):
        get_transaction_amount_rub(transaction)


def test_missing_amount():
    transaction = {"currency": "RUB"}
    with pytest.raises(ValueError, match="Invalid transaction data"):
        get_transaction_amount_rub(transaction)


def test_lowercase_currency():
    transaction = {"amount": "100.00", "currency": "rub"}
    assert get_transaction_amount_rub(transaction) == 100.00


def test_negative_amount():
    transaction = {"amount": "-50.25", "currency": "RUB"}
    assert get_transaction_amount_rub(transaction) == -50.25


def test_load_transactions_empty_file(tmp_path):
    """Проверка пустого файла (должен вернуть [])."""
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")  # Создаем пустой файл

    result = load_transactions(file_path)
    assert result == []


def test_load_transactions_non_list_json(tmp_path):
    """Проверка JSON-словаря вместо списка (должен вернуть [])."""
    file_path = tmp_path / "not_a_list.json"
    file_path.write_text('{"transactions": [1, 2, 3]}', encoding="utf-8")

    result = load_transactions(file_path)
    assert result == []


def test_load_transactions_file_not_found():
    """Проверка несуществующего файла (должен вернуть [])."""
    result = load_transactions("non_existent_file.json")
    assert result == []


def test_load_transactions_invalid_json(tmp_path):
    """Проверка битого JSON (должен вернуть [])."""
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid json}", encoding="utf-8")

    result = load_transactions(file_path)
    assert result == []


def test_load_transactions_encoding_error(tmp_path):
    """Проверка файла с некорректной кодировкой (должен вернуть [])."""
    file_path = tmp_path / "bad_encoding.json"
    # Записываем данные в бинарном режиме с некорректной кодировкой
    with open(file_path, "wb") as f:
        f.write(b"\xff\xfe")  # Невалидный UTF-8

    result = load_transactions(file_path)
    assert result == []
