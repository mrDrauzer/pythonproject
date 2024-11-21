import os
import logging


logger_card_number = logging.getLogger("get_mask_card_number")
logger_card_number.setLevel(logging.DEBUG)

logger_mask_account = logging.getLogger("get_mask_account")
logger_mask_account.setLevel(logging.DEBUG)

file_handle = logging.FileHandler(os.path.join(os.path.dirname(__file__), "..", "logs", "masks.log"), encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s- %(name)s - %(levelname)s: %(message)s")
file_handle.setFormatter(file_formatter)

logger_card_number.addHandler(file_handle)
logger_mask_account.addHandler(file_handle)


def get_mask_card_number(card_number: int) -> str:
    """
    Принимает числовое либо строковое значение и скрывает
    символы указанные в hidden_chars = [6, 7, 8, 9, 10, 11]
    """
    try:
        hidden_chars = [6, 7, 8, 9, 10, 11]
        hidden_number = ""
        for i, char in enumerate(str(card_number)):
            if i in hidden_chars:
                hidden_number += "*"
            else:
                hidden_number += char
        blocks = [hidden_number[0:4], hidden_number[4:8], hidden_number[8:12], hidden_number[12:16]]
        logger_card_number.debug(f"Card number: {" ".join(blocks)}")
        return " ".join(blocks)
    except Error:
        logger_card_number.error((f"Произошла ошибка"))
        print("ошибка")
        return ""


def get_mask_account(account_number: int) -> str:
    """
    Принимает числовое либо строковое значение и скрывает
    символы указанные в hidden_chars = [0, 1]
    """
    try:
        account_number_txt = str(account_number)
        hidden_number = "**" + account_number_txt[-4:]
        logger_mask_account.debug(f"Account number: {hidden_number}")
        return hidden_number
    except Error:
        logger_mask_account.error((f"Произошла ошибка"))
        print("ошибка")
        return ""
