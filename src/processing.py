def filter_by_state(operations: list[dict[str, object]], state: str = "EXECUTED") -> list[dict[str, object]]:
    """
    Фильтрует список операций, оставляя только операции с указанным статусом.
    """
    filtered = []

    for op in operations:
        if op.get("state") == state:
            filtered.append(op)

    return filtered


def sort_by_date(operations: list[dict[str, str]]) -> list[dict[str, str]]:
    """Сортирует операции по дате (от старых к новым)."""

    sorted_ops = operations.copy()
    n = len(sorted_ops)

    for i in range(n):
        for j in range(n - i - 1):
            if sorted_ops[j]["date"] > sorted_ops[j + 1]["date"]:
                sorted_ops[j], sorted_ops[j + 1] = sorted_ops[j + 1], sorted_ops[j]

    return sorted_ops
