import os
from dotenv import load_dotenv
from src.utils import open_json
import requests
import json
from json import JSONDecodeError


def sum_transaction(local_json_file, coin="RUB") -> float:
    """Возрощат сумму транзакция в указанной волюье по умолчанию в рублях"""
    load_dotenv(".env")
    api_key = os.getenv("API_KEY")
    headers = {"API_KEY": api_key}
    sum = 0.0
    transaction = open_json(local_json_file)
    usd_coin = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    for i in transaction:
        if "operationAmount" in i:
            code = i["operationAmount"]["currency"]["code"]
            amount = i["operationAmount"]["amount"]
            if code == coin:
                sum += float(amount)
            else:
                sum += float(amount) * float(usd_coin["Valute"]["USD"]["Value"])
                # url = f"https://api.apilayer.com/exchangerates_data/convert?from={code}&to={coin}&amount={amount}"
                # response = requests.get(url, headers=headers)
                # result = response.json()
        else:
            continue
    return sum
