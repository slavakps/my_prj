def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты.
    Если номер некорректный, возвращает 'Неправильный номер карты'
    """
    if len(card_number) == 16 and card_number.isdigit():
        return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    else:
        return "Неправильный номер карты"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта, оставляя видимыми только последние 4 цифры.
    Если номер некорректный, возвращает 'Неправильный номер карты'
    """
    if len(account_number) >= 4 and account_number.isdigit():
        return "**" + account_number[-4:]
    else:
        return "Неправильный номер счёта"
