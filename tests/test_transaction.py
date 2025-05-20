from unittest.mock import patch

import pytest

from src.utils import get_transaction_amount_rub


def test_rub_transaction():
    """Тест транзакции в рублях"""
    transaction = {"amount": 100.50, "currency": "RUB"}
    assert get_transaction_amount_rub(transaction) == 100.50


@patch("src.external_api.get_exchange_rate", return_value=75.50)
def test_usd_conversion(mock_rate):
    """Тест конвертации USD в RUB"""
    transaction = {"amount": 100.0, "currency": "USD"}
    assert get_transaction_amount_rub(transaction) == 7550.0
    mock_rate.assert_called_once_with("USD")


@patch("src.external_api.get_exchange_rate", return_value=85.30)
def test_eur_conversion(mock_rate):
    """Тест конвертации EUR в RUB"""
    transaction = {"amount": 100.0, "currency": "EUR"}
    assert get_transaction_amount_rub(transaction) == 8530.0
    mock_rate.assert_called_once_with("EUR")


def test_missing_amount():
    """Тест обработки отсутствия суммы"""
    with pytest.raises(ValueError):
        get_transaction_amount_rub({"currency": "USD"})


def test_unsupported_currency():
    """Тест неподдерживаемой валюты"""
    with pytest.raises(ValueError):
        get_transaction_amount_rub({"amount": 100, "currency": "GBP"})
