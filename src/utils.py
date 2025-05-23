import json
import datetime
import os
import logging
import pandas as pd
import re
from json import JSONDecodeError
from typing import List, Dict, Any, Optional


# Настройка логирования
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


def fetch_data_from_api(api_url: str) -> Dict[str, Any]:
    """Получает данные из внешнего API."""
    try:
        # Здесь может быть запрос через requestso.
        response = {"data": "example"}  # Заглушка
        logger.info("Данные успешно получены из API")
        return response
    except Exception as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return {}

def process_dataframe(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Обрабатывает DataFrame и преобразует в список словарей."""
    try:
        # Фильтрация, группировка, добавление полей
        processed_data = df.to_dict(orient="records")
        logger.info("DataFrame успешно обработан")
        return processed_data
    except Exception as e:
        logger.error(f"Ошибка обработки DataFrame: {e}")
        return []

def generate_json_response(data: List[Dict[str, Any]]) -> str:
    """Генерирует JSON-ответ."""
    try:
        response = {
            "status": "success",
            "timestamp": datetime.datetime.now().isoformat(),
            "data": data
        }
        return json.dumps(response, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Ошибка генерации JSON: {e}")
        return json.dumps({"status": "error", "message": str(e)})


# --- Функции поиска ---
def search_transactions(
        transactions: List[Dict[str, Any]],
        query: str,
        case_sensitive: bool = False
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании или категории.

    Пример:
    >>> search_transactions([{"Описание": "Кофе"}], "кофе")
    [{"Описание": "Кофе"}]
    """
    try:
        if not query:
            return transactions

        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(re.escape(query), flags)

        result = [
            t for t in transactions
            if pattern.search(str(t.get("Описание", "")))
               or pattern.search(str(t.get("Категория", "")))
        ]
        logger.info(f"Найдено {len(result)} транзакций по запросу '{query}'")
        return result
    except Exception as e:
        logger.error(f"Ошибка поиска: {e}")
        return []


def find_phone_transactions(
        transactions: List[Dict[str, Any]],
        phone_pattern: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции с номерами телефонов в описании.

    Пример:
    >>> find_phone_transactions([{"Описание": "Пополнение +7 921 123-45-67"}])
    [{"Описание": "Пополнение +7 921 123-45-67"}]
    """
    default_pattern = r'(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    try:
        regex = re.compile(phone_pattern or default_pattern)
        result = [
            t for t in transactions
            if regex.search(str(t.get("Описание", "")))
        ]
        logger.info(f"Найдено {len(result)} транзакций с номерами телефонов")
        return result
    except Exception as e:
        logger.error(f"Ошибка поиска номеров: {e}")
        return []


def find_person_transfers(
        transactions: List[Dict[str, Any]],
        name_pattern: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Ищет переводы физлицам (шаблон: 'Имя Ф.' + категория 'Переводы').

    Пример:
    >>> find_person_transfers([{"Описание": "Иван П.", "Категория": "Переводы"}])
    [{"Описание": "Иван П.", "Категория": "Переводы"}]
    """
    default_pattern = r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$'
    try:
        regex = re.compile(name_pattern or default_pattern)
        result = [
            t for t in transactions
            if str(t.get("Категория", "")).lower() == "переводы"
               and regex.search(str(t.get("Описание", "")))
        ]
        logger.info(f"Найдено {len(result)} переводов физлицам")
        return result
    except Exception as e:
        logger.error(f"Ошибка поиска переводов: {e}")
        return []