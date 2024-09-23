def filter_by_state(list_operations, operation_status="EXECUTED"):
    """
    Принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    try:
        list_operations_state = []
        key = {}
        for operations in list_operations:
            if operations["state"] in operation_status:
                list_operations_state.append(operations)
        return list_operations_state

    except Exception:
        return


def sort_by_date(list_operations, ascending=False):
    """
    Принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """

    sort_by_date = sorted(list_operations, key=lambda x: x.get("date", 0), reverse=ascending)
    return sort_by_date


list = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(sort_by_date(list))
print(filter_by_state(list))
print(filter_by_state(list, "CANCELED"))
