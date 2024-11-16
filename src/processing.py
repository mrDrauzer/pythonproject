def filter_by_state(list_operations: list[dict], operation_status: str = "EXECUTED") -> list[dict]:
    """
    Принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    list_operations_state = []
    for operations in list_operations:
        if operations["state"] in operation_status:
            list_operations_state.append(operations)
    return list_operations_state


def sort_by_date(list_operations: list[dict], ascending: bool = True) -> list[dict]:
    """
    Принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """
    sort_by_date = sorted(list_operations, key=lambda x: x.get("date", 0), reverse=not ascending)
    return sort_by_date
