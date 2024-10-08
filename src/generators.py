def filter_by_currency(list_dict: list[dict], data = "USD"):
    return filter(lambda x: x['currency'] == currency, data)

    # Пример использования
    data = [{'name': 'Товар 1', 'price': 100, 'currency': 'USD'}, {'name': 'Товар 2', 'price': 50, 'currency': 'EUR'},
            {'name': 'Товар 3', 'price': 75, 'currency': 'RUB'}]
    filtered_data = filter_by_currency(data, 'USD')
    for item in filtered_data:
        print(item)


def transaction_descriptions (list_dict: list[dict]):
    yield

def card_number_generator (start, stop, step =1 ):
    if start < stop:
        for i in range(start, stop+1, step):
            number_card = ''
            number_card += "0"*(16-len(str(i)))+str(i)
            blocks = [number_card[0:4], number_card[4:8], number_card[8:12], number_card[12:16]]
            number_card_blocks = " ".join(blocks)
            yield number_card_blocks
    elif stop < start:
        for i in range(start, stop+1, -step):
            number_card = ''
            number_card += "0"*(16-len(str(i)))+str(i)
            blocks = [number_card[0:4], number_card[4:8], number_card[8:12], number_card[12:16]]
            number_card_blocks = " ".join(blocks)
            yield number_card_blocks


for card_number in card_number_generator(60, 50):
    print(card_number)
