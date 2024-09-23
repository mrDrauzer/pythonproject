import datetime

from masks import get_mask_account, get_mask_card_number


def mask_account_card(cards_accounts: str) -> str:
    """
    Принимает строковое значение забирает из их только цыфры
    по количеству цифр сооотносит номер карты или счета после
    проводит через функции get_mask_account либо get_mask_card_number
    """
    numbers = ""
    mask_cards_accounts = ""
    for char in cards_accounts:
        if char.isdigit():
            numbers += char
        else:
            mask_cards_accounts += char
    if len(numbers) > 16:
        mask_cards_accounts += get_mask_account(numbers)

    else:
        mask_cards_accounts += get_mask_card_number(numbers)
    return mask_cards_accounts


def get_date(data_st: str) -> str:
    """
    Принимает на вход строку 2024-03-11T02:26:18.671407 и отдает корректный результат в формате ДД.ММ.ГГГГ
    В случаи некоректного вода возращает:
    "Некорректный формат даты, укажите дату в формате день месяц год (ДД.ММ.ГГГГ)", "Cегодня", ДД.ММ.ГГГГ)
    """
    try:
        date_object = datetime.datetime.strptime(data_st, "%Y-%m-%dT%H:%M:%S.%f")
        return date_object.strftime("%d.%m.%Y")
    except ValueError:
        return "Некорректный формат даты, укажите дату в формате 2024-03-11T02:26:18.671407"


print(get_date("2024-11-11T02:26:18.671407"))
print(mask_account_card("Счет 73654108430135874305"))
print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card("MasterCard 7158300734726758"))
print(mask_account_card("Счет 35383033474447895560"))
print(mask_account_card("Visa Classic 6831982476737658"))
print(mask_account_card("Visa Platinum 8990922113665229"))
print(mask_account_card("Visa Gold 5999414228426353"))
print(mask_account_card("Счет 73654108430135874305"))
