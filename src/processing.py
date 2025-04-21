def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует операции по статусу.

    Принимает:
        operations - список словарей (каждый словарь - одна операция)
        state - нужный статус (по умолчанию "EXECUTED")

    Возвращает:
        список отфильтрованных операций (список словарей)
    """
    result = []
    for operation in operations:
        if operation.get("state") == state:
            result.append(operation)
    return result


def sort_by_date(operations: list, reverse: bool = False) -> list:
    """
    Сортирует операции по дате.

    Принимает:
        operations - список словарей (должен содержать ключ "date")
        reverse - порядок сортировки:
            False (по умолчанию) - старые к новым
            True - новые к старым

    Возвращает:
        отсортированный список операций (список словарей)
    """
    # Делаем копию, чтобы не менять исходный список
    sorted_list = operations.copy()

    # Пузырьковая сортировка
    n = len(sorted_list)
    for i in range(n):
        for j in range(n - i - 1):
            # Сравниваем даты с учётом параметра reverse
            if (sorted_list[j]["date"] > sorted_list[j + 1]["date"]) != reverse:
                # Меняем местами
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    return sorted_list
