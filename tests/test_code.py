import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator



@pytest.fixture
def namber_cart():
    return ["Maestro 1596837868705199",
            "Счет 64686473678894779589",
            "MasterCard 7158300734726758",
            "Счет 35383033474447895560",
            "Visa Classic 6831982476737658",
            "Visa Platinum 8990922113665229",
            "Visa Gold 5999414228426353",
            "Счет 73654108430135874305"]

def test_get_mask_card_number_14():
    assert get_mask_card_number('12345678901234') == '1234 56** **** 34'


def test_get_mask_card_number_16():
    assert get_mask_card_number('1234567890123456') == '1234 56** **** 3456'


def test_get_mask_account():
    assert get_mask_account('1234567890123456') == '**3456'


def test_mask_account_card_c14():
    assert mask_account_card('12345678901234') == '1234 56** **** 34'


def test_mask_account_card_c16():
    assert mask_account_card('1234567890123456') == '1234 56** **** 3456'


def test_mask_account_card_a17():
    assert mask_account_card('12345678901234567') == '**4567'


def test_mask_account_card_a20():
    assert mask_account_card('12345678901234567890') == '**7890'


def test_get_date():
    assert get_date('2024-03-11T02:26:18.671407') == '11.03.2024'


def test_filter_by_state():
    test_txt_in = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                   {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                   {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                   {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    test_txt_out = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    assert filter_by_state(test_txt_in) == test_txt_out


def test_sort_by_date():
    test_data_out = [{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]
    test_data_in = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    assert sort_by_date(test_data_in) == test_data_out

def test_sort_by_date_none():
    test_data_out = [{'id': 41428829, 'state': 'EXECUTED', 'date': ''},
                     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    test_data_in = [{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                     {'id': 41428829, 'state': 'EXECUTED', 'date': ''},
                     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    assert sort_by_date(test_data_in) == test_data_out





def test_transaction_descriptions():
    transactions = [
        {"id": 1, "description": "Test1", "amount": 100},
        {"id": 2, "description": "Test2", "amount": 200},
        {"id": 3, "description": "Test3", "amount": 300}
    ]
    generator = transaction_descriptions(transactions)

    assert next(generator) == "Test1"
    assert next(generator) == "Test2"
    assert next(generator) == "Test3"

    with pytest.raises(StopIteration):
        next(generator)


def test_transaction_descriptions_empty_combination():
    transactions = []
    generator =  transaction_descriptions(transactions)

    with pytest.raises(StopIteration):
        next(generator)



def test_filter_by_currency_no_transaction():
    transactions = []
    currency_code = 'USD'
    result = filter_by_currency(transactions, currency_code)
    assert list(result) == []


def test_filter_by_currency_single_transaction_same_currency():
    transactions = [{"operationAmount": {"currency": {"code": 'USD'}}}]
    currency_code = 'USD'
    result = filter_by_currency(transactions, currency_code)
    assert list(result) == transactions


def test_filter_by_currency_single_transaction_different_currency():
    transactions = [{"operationAmount": {"currency": {"code": 'EUR'}}}]
    currency_code = 'USD'
    result = filter_by_currency(transactions, currency_code)
    assert list(result) == []


def test_filter_by_currency_multiple_transactions():
    transactions = [
        {"operationAmount": {"currency": {"code": 'USD'}}},
        {"operationAmount": {"currency": {"code": 'EUR'}}},
        {"operationAmount": {"currency": {"code": 'JPY'}}}
    ]
    currency_code = 'JPY'
    result = filter_by_currency(transactions, currency_code)
    assert list(result) == [transactions[2]]


def test_filter_by_currency_multiple_transactions_same_currency():
    transactions = [
        {"operationAmount": {"currency": {"code": 'USD'}}},
        {"operationAmount": {"currency": {"code": 'USD'}}},
        {"operationAmount": {"currency": {"code": 'USD'}}}
    ]
    currency_code = 'USD'
    result = filter_by_currency(transactions, currency_code)
    assert list(result) == transactions



def test_card_number_generator_ascending():
    # Test for ascending generated card numbers with default step
    generator = card_number_generator(5, 7)
    assert next(generator) == "0000 0000 0000 0005"
    assert next(generator) == "0000 0000 0000 0006"
    assert next(generator) == "0000 0000 0000 0007"


def test_card_number_generator_descending():
    # Test for descending generated card numbers with default step
    generator = card_number_generator(7, 5)
    assert next(generator) == "0000 0000 0000 0007"
    assert next(generator) == "0000 0000 0000 0006"
    assert next(generator) == "0000 0000 0000 0005"


def test_card_number_generator_step():
    # Test for ascending generated card numbers with custom step
    generator = card_number_generator(5, 15, 5)
    assert next(generator) == "0000 0000 0000 0005"
    assert next(generator) == "0000 0000 0000 0010"
    assert next(generator) == "0000 0000 0000 0015"

@pytest.mark.parametrize("a, b, c", [
    (1, 2, 19),
    (5, 9, 19),
    (4, 8, 19),
    (0, 29, 19),
])
def test_addition(a, b, c):
    generator = card_number_generator(a, b)
    namber = next(generator)
    assert c == len(str(namber))