import os
from dotenv import load_dotenv
from src.utils import open_json
import requests
import json
from json import JSONDecodeError

def sum_transaction(local_json_file, coin = "RUB") -> float:
    """Возрощат сумму транзакция в указанной волюье по умолчанию в рублях"""
    load_dotenv()
    api_key = os.getenv('API_KEY')
    headers = {'apikey': api_key}
    sum = 0.0
    transaction = open_json(local_json_file)
    for i in transaction:
        code = i["operationAmount"]["currency"]["code"]
        amount = i["operationAmount"]["amount"]
        if code == coin:
            print(amount)
            sum += float(amount)
            print(f"sum {sum}")
        else:
            url = f"https://api.apilayer.com/exchangerates_data/convert?from={code}&to={coin}&amount={amount}"
            response = requests.get(url, headers=headers)
            #result = response.json()
            result_amount = response.json()[0]['result']
            sum += float(result_amount)
            print(result)
            print(result_amount)
            print(f"sum {sum}")
    return sum


print(sum_transaction(r'c:\python\project\home_work\data\operations.json'))
#print(sum_transaction(1))

