def mask_account_card(data: str) -> str:
    """
    Маскирует номер карты или счёта в переданной строке.
    """
    parts = data.split()

    # Маскировка счёта (если начинается с "Счет")
    if parts[0] == "Счет":
        account_number = parts[-1]
        masked_number = f"**{account_number[-4:]}"
        return " ".join(parts[:-1] + [masked_number])

    # Маскировка карты (все остальные случаи)
    else:
        card_number = parts[-1]
        if len(card_number) >= 16 and card_number.isdigit():
            masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
            return " ".join(parts[:-1] + [masked_card])
        else:
            # Если номер карты некорректный, возвращаем исходную строку без изменений
            return data
