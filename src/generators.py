def filter_by_currency(transactions: list[dict], currency_code: list[dict]) -> list[dict]:
    """Принимает список словарей на вход возвращает итератор"""

    def currency_filter(transaction: list[dict]) -> list[dict[str, str]]:
        return transaction["operationAmount"]["currency"]["code"] == currency_code

    return (transaction for transaction in transactions if currency_filter(transaction))


# @logfile()
def transaction_descriptions(transactions: list[dict]):
    """принимает на вход список словарей.
    использует yield  для генерации значений по запросу"""
    for transaction in transactions:
        yield transaction["description"]


# @log
def card_number_generator(start: int = 0, stop: int = 5, step: int = 1) -> str:
    """Генератор принимает значения start и stop, +дополниетеный step в качестве аргумента.
    Start начальное значение,  Stop - конечное значение
    При значении Start меньше Stop генерируется по порядку
    При значении Start больше Stop генерируется в обратном порядке порядку"""
    if start < stop:
        for i in range(start, stop + 1, step):
            number_card = ""
            number_card += "0" * (16 - len(str(i))) + str(i)
            blocks = [number_card[0:4], number_card[4:8], number_card[8:12], number_card[12:16]]
            number_card_blocks = " ".join(blocks)
            yield number_card_blocks
    elif stop < start:
        for i in range(start, stop - 1, -step):
            number_card = ""
            number_card += "0" * (16 - len(str(i))) + str(i)
            blocks = [number_card[0:4], number_card[4:8], number_card[8:12], number_card[12:16]]
            number_card_blocks = " ".join(blocks)
            yield number_card_blocks
