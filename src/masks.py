import logging

# Настройка логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Файловый обработчик
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Форматтер для логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты.
    Если номер некорректный, возвращает 'Неправильный номер карты'
    """
    try:
        if len(card_number) == 16 and card_number.isdigit():
            masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}->"
            logger.info(f"Успешное маскирование номера карты: {masked_number}")
            return masked_number
        logger.error(f"Некорректный номер карты: {card_number}")
        return "Неправильный номер карты"
    except Exception as e:
        logger.error(f"Ошибка при маскировании номера карты: {str(e)}")
        return "Неправильный номер карты"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта, оставляя видимыми только последние 4 цифры.
    Если номер некорректный, возвращает 'Неправильный номер счёта'
    """
    try:
        if len(account_number) >= 4 and account_number.isdigit():
            masked_account = f"** + {account_number[-4:]}"
            logger.info(f"Успешное маскирование номера счета: {masked_account}")
            return masked_account
        logger.error(f"Некорректный номер счета: {account_number}")
        return "Неправильный номер счёта"
    except Exception as e:
        logger.error(f"Ошибка при маскировании номера счета: {str(e)}")
        return "Неправильный номер счёта"
