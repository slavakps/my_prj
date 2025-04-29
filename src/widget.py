def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счёта в переданной строке.
    Возвращает:
    - Для счета: "**XXXX" (последние 4 цифры)
    - Для карты: "XXXX XX** **** XXXX"
    - Для некорректных данных: исходную строку
    """
    if not data or not data.strip():
        return data

    parts = data.split()
    if len(parts) < 2:
        return data

    # Маскировка счёта
    if parts[0] == "Счет":
        account_number = parts[-1]
        if len(account_number) >= 4 and account_number.isdigit():
            return " ".join(parts[:-1] + [f"**{account_number[-4:]}"])
        return data

    # Маскировка карты
    card_number = parts[-1]
    if len(card_number) == 16 and card_number.isdigit():
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        return " ".join(parts[:-1] + [masked])

    return data


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS в DD.MM.YYYY
    Возвращает "Invalid date format" для некорректных данных
    """
    if not date_str or not isinstance(date_str, str):
        return "Invalid date format"

    try:
        date_part = date_str.split("T")[0]
        parts = date_part.split("-")
        if len(parts) != 3:
            return "Invalid date format"

        year, month, day = parts
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError, AttributeError):
        return "Invalid date format"
