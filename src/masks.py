def get_mask_card_number(card_number: int) -> str:
    """
    Принимает числовое либо строковое значение и скрывает
    символы указанные в hidden_chars = [6, 7, 8, 9, 10, 11]
    """
    hidden_chars = [6, 7, 8, 9, 10, 11]
    hidden_number = ''
    for i, char in enumerate(str(card_number)):
        if i in hidden_chars:
            hidden_number += '*'
        else:
            hidden_number += char
    blocks = [
        hidden_number[0:4],
        hidden_number[4:8],
        hidden_number[8:12],
        hidden_number[12:16]
    ]
    return ' '.join(blocks)


def get_mask_account(account_number: int) -> str:
    """
    Принимает числовое либо строковое значение и скрывает
    символы указанные в hidden_chars = [0, 1]
    """
    account_number_txt = str(account_number)
    hidden_number = '**' + account_number_txt[-4:]
    return  hidden_number


def mask_account_card(cards_accounts):
    numbers = ''
    mask_cards_accounts = ''
    for char in cards_accounts:
        if char.isdigit():
            numbers += char
    if len(numbers) > 16:
        mask_cards_accounts = get_mask_account(numbers)
    else:
        mask_cards_accounts = get_mask_card_number(numbers)
    return mask_cards_accounts

print(mask_account_card('Счет 73654108430135874305'))
print(mask_account_card("Maestro 7000792289606361"))

import datetime

def get_date(input_string):
    try:
        date_object = datetime.datetime.strptime(input_string, '%d.%m.%Y')
        return date_object.strftime('%d.%m.%Y')
    except ValueError:
        return "Некорректный формат даты"


# Пример использования
result = get_date("11.07.2018")
print(result)