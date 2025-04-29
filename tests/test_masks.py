import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected", [("1234567890123456", "1234 56** **** 3456"), ("1111111122222222", "1111 11** **** 2222")]
)
def test_get_mask_card_number(card_number: str, expected: str):
    """Проверяет корректную маскировку номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("account_number, expected", [("1234567890", "**7890"), ("9999", "**9999")])
def test_get_mask_account(account_number: str, expected: str):
    """Проверяет корректную маскировку номера счёта и обработку ошибок."""
    assert get_mask_account(account_number) == expected
