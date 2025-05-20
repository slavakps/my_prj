from unittest.mock import patch

import pytest

from src.utils import get_transaction_amount_rub


def test_rub_transaction():
    """Тест транзакции в рублях"""
    with patch("src.external_api.convert_to_rub") as mock_convert:
        mock_convert.return_value = 100.50
        transaction = {"amount": 100.50, "currency": "RUB"}

        result = get_transaction_amount_rub(transaction)

        assert result == 100.50
        assert isinstance(result, float)
        mock_convert.assert_called_once_with(transaction)


def test_usd_transaction():
    """Тест транзакции в долларах"""
    with patch("src.external_api.convert_to_rub") as mock_convert:
        mock_convert.return_value = 7500.0
        transaction = {"amount": 100.0, "currency": "USD"}

        result = get_transaction_amount_rub(transaction)

        assert result == 7500.0
        mock_convert.assert_called_once_with(transaction)


def test_missing_amount():
    """Тест отсутствия суммы"""
    transaction = {"currency": "USD"}

    with pytest.raises(ValueError, match="Invalid transaction data"):
        get_transaction_amount_rub(transaction)


def test_missing_currency():
    """Тест отсутствия валюты"""
    transaction = {"amount": 100.0}

    with pytest.raises(ValueError, match="Invalid transaction data"):
        get_transaction_amount_rub(transaction)


def test_invalid_amount_type():
    """Тест неверного типа суммы"""
    transaction = {"amount": "100", "currency": "USD"}

    with pytest.raises(ValueError, match="Invalid transaction data"):
        get_transaction_amount_rub(transaction)


def test_api_error():
    """Тест ошибки API"""
    with patch("src.external_api.convert_to_rub") as mock_convert:
        mock_convert.side_effect = ValueError("API error")
        transaction = {"amount": 100.0, "currency": "USD"}

        with pytest.raises(ValueError, match="Invalid transaction data"):
            get_transaction_amount_rub(transaction)


def test_unsupported_currency():
    """Тест неподдерживаемой валюты"""
    with patch("src.external_api.convert_to_rub") as mock_convert:
        mock_convert.side_effect = ValueError("Unsupported currency")
        transaction = {"amount": 100.0, "currency": "GBP"}

        with pytest.raises(ValueError, match="Invalid transaction data"):
            get_transaction_amount_rub(transaction)
