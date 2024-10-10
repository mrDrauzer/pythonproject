
def filter_by_currency(transactions, currency_code):
    def currency_filter(transaction):
        return transaction["operationAmount"]["currency"]["code"] == currency_code

    return (transaction for transaction in transactions if currency_filter(transaction))


def transaction_descriptions(transactions):
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start=0, stop=5, step=1):
    if start < stop:
        for i in range(start, stop + 1, step):
            number_card = ""
            number_card += "0" * (16 - len(str(i))) + str(i)
            blocks = [number_card[0:4], number_card[4:8], number_card[8:12], number_card[12:16]]
            number_card_blocks = " ".join(blocks)
            yield number_card_blocks
    elif stop < start:
        for i in range(start, stop + 1, -step):
            number_card = ""
            number_card += "0" * (16 - len(str(i))) + str(i)
            blocks = [number_card[0:4], number_card[4:8], number_card[8:12], number_card[12:16]]
            number_card_blocks = " ".join(blocks)
            yield number_card_blocks


#for card_number in card_number_generator(0, 5000000000000000, 2325454560):
#    print(card_number)




transactions = (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))