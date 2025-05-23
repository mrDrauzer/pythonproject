import os
import datetime
import json
import requests
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
import pandas as pd
from utils import fetch_data_from_api, process_dataframe, generate_json_response

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка ключа из .env
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("API_Alpha_Vantage")


# Приветствие ---
def get_greeting(time_str: str) -> str:
    """Возвращает приветствие по времени."""
    try:
        time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").time()
        if 5 <= time.hour < 12:
            return "Доброе утро"
        elif 12 <= time.hour < 18:
            return "Добрый день"
        elif 18 <= time.hour < 23:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
    except ValueError:
        logger.warning("Неверный формат времени. Используется время по умолчанию.")
        return "Добрый день"


# Данные по картам ---
def get_card_data(cards: List[Dict]) -> List[Dict]:
    """Обрабатывает данные карт: последние 4 цифры, сумма, кешбэк."""
    result = []
    for card in cards:
        try:
            last_digits = card["number"][-4:]
            total_spent = sum(t["amount"] for t in card["transactions"])
            cashback = round(total_spent / 100, 2)  # 1% кешбэка
            result.append({
                "last_digits": last_digits,
                "total_spent": round(total_spent, 2),
                "cashback": cashback
            })
        except KeyError as e:
            logger.error(f"Ошибка в данных карты: {e}")
    return result


# Топ-5 транзакций ---
def get_top_transactions(transactions: List[Dict]) -> List[Dict]:
    """Возвращает 5 самых крупных транзакций."""
    try:
        return sorted(transactions, key=lambda x: abs(x["amount"]), reverse=True)[:5]
    except KeyError:
        logger.error("Некорректные данные транзакций")
        return []


#   Курсы валют (API ЦБ РФ) ---
def get_currency_rates() -> List[Dict]:
    """Получает курсы волют USD и EUR."""
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)
        data = response.json()
        return [
            {"currency": "USD", "rate": round(data["Valute"]["USD"]["Value"], 2)},
            {"currency": "EUR", "rate": round(data["Valute"]["EUR"]["Value"], 2)}
        ]
    except Exception as e:
        logger.error(f"Ошибка при запросе курсов: {e}")
        return [  # Резервные данные
            {"currency": "USD", "rate": 83.21},
            {"currency": "EUR", "rate": 97.08}        ]


# --- 5. Акции S&P500 (Alpha Vantage) ---
def get_stock_prices() -> List[Dict]:
    """Получает цены акций. Если API не работает, возвращает заглушку."""
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = []

    if not ALPHA_VANTAGE_API_KEY:
        logger.warning("Ключ Alpha Vantage не найден в .env")
        return get_backup_stock_data()

    for stock in stocks:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                price = float(data["Global Quote"]["05. price"])
                prices.append({"stock": stock, "price": round(price, 2)})
        except Exception as e:
            logger.error(f"Ошибка при запросе акции {stock}: {e}")

    return prices if prices else get_backup_stock_data()


def get_backup_stock_data() -> List[Dict]:
    """Резервные данные акций."""
    return [
        {"stock": "AAPL", "price": 175.20},
        {"stock": "AMZN", "price": 3250.10},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08}
    ]


# --- Главная функция ---
def generate_report(
        time_str: str,
        cards_data: List[Dict],
        transactions: List[Dict]
) -> Dict[str, Any]:
    """Генерирует итоговый JSON-отчёт."""
    return {
        "greeting": get_greeting(time_str),
        "cards": get_card_data(cards_data),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices()
    }

# ---Функция для страницы «События»
def events_page_handler(input_df: pd.DataFrame) -> str:
    """
    Основная функция для страницы «События».
    Принимает DataFrame, обрабатывает его и возвращает JSON.
    """
    try:
        # 1. Получение дополнительных данных из API
        api_data = fetch_data_from_api("https://api.example.com/events")

        # 2. Обработка DataFrame
        processed_data = process_dataframe(input_df)

        # 3. Формирование JSON-ответа
        json_response = generate_json_response(processed_data)

        return json_response
    except Exception as e:
        return generate_json_response({"error": str(e)})
