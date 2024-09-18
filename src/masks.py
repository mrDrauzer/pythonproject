def get_mask_card_number(card_number: int) -> str:
    """
    Принимает числовое либо строковое значение и скрывает
    символы указанные в hidden_chars = [6, 7, 8, 9, 10, 11]
    """
    hidden_chars = [6, 7, 8, 9, 10, 11]
    hidden_number = ""
    for i, char in enumerate(str(card_number)):
        if i in hidden_chars:
            hidden_number += "*"
        else:
            hidden_number += char
    blocks = [hidden_number[0:4], hidden_number[4:8], hidden_number[8:12], hidden_number[12:16]]
    return " ".join(blocks)


def get_mask_account(account_number: int) -> str:
    """
    Принимает числовое либо строковое значение и скрывает
    символы указанные в hidden_chars = [0, 1]
    """
    account_number_txt = str(account_number)
    hidden_number = "**" + account_number_txt[-4:]
    return hidden_number
