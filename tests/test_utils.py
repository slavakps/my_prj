from unittest.mock import patch

import pytest

from src.utils import get_transaction_amount_rub


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
