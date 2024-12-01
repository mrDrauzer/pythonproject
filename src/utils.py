import json
import os
import logging
import pandas as pd
from json import JSONDecodeError


logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handle = logging.FileHandler(os.path.join(os.path.dirname(__file__), "..", "logs", "utils.log"), encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s- %(name)s - %(levelname)s: %(message)s")
file_handle.setFormatter(file_formatter)
logger.addHandler(file_handle)


def open_json(local_json_file=os.path.join(os.path.dirname(__file__), "..", "data", "operations.json")):
    """Принимат на вход сслыку на файл JSON выдает список словарей"""
    try:
        logger.debug("Выполнение чтения JSON")
        if not os.path.exists(local_json_file):
            print(f"Файл {local_json_file} не найден")
            return "[]"
        else:
            with open(local_json_file, encoding="utf-8") as f:
                data = json.load(f)
                return data
    except JSONDecodeError:
        logger.error(("Произошла ошибка"))
        print("Фаил пустой")
        return "[]"


def open_csv(local_csv_file=os.path.join(os.path.dirname(__file__), "..", "data", "transactions.csv")):
    """Принимат на вход сслыку на файл CSV выдает список словарей"""
    try:
        logger.debug("Выполнение чтения CSV")
        if not os.path.exists(local_csv_file):
            print(f"Файл {local_csv_file} не найден")
            return "[]"
        else:
            wine_reviews = pd.read_csv(local_csv_file, delimiter=';')
            print(wine_reviews.shape)
            return wine_reviews.to_dict("records")
    except csv.Error as e:
        logger.error(f"Ошибка чтения CSV файла {local_csv_file}: {e}")


def open_excel(local_excel_file=os.path.join(os.path.dirname(__file__), "..", "data", "transactions_excel.xlsx")):
    """Принимат на вход сслыку на файл XLSX выдает список словарей"""
    try:
        logger.debug("Выполнение чтения excel")
        if not os.path.exists(local_excel_file):  # поправить ниже
            print(f"Файл {local_excel_file} не найден")
            return "[]"
        else:
            wine_reviews = pd.read_excel(local_excel_file)
            print(wine_reviews.head())
            return wine_reviews.to_dict(orient="records")
    except FileNotFoundError as e:
        logger.error(("Произошла ошибка"))
        print(f"Файл {local_excel_file} не найден: {e}")
        return "[]"
    except Exception as e:
        logger.error(("Произошла ошибка"))
        print(f"Неизвестная ошибка при чтении файла {local_excel_file}: {e}")
        return "[]"
    return "[]"


print(open_csv())