from src.external_api import convert_to_rub


def get_transaction_amount_rub(transaction: dict) -> float:
    """
    Возвращает сумму транзакции в рублях
    :param transaction: Словарь с данными транзакции
    :return: Сумма в рублях (float)
    """
    try:
        return convert_to_rub(transaction)
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid transaction data: {str(e)}")
