import json
import os
from json import JSONDecodeError


def open_json(local_json_file = r'c:\python\project\home_work\data\operations.json'):
    """ Принимат на вход сслыку на файл JSON выдает список словарей"""
    try:
        if not os.path.exists(local_json_file):
            print(f"Файл {local_json_file} не найден")
            return "[]"
        else:
            with open(local_json_file, encoding='utf-8') as f:
                data = json.load(f)
                return data
    except JSONDecodeError:
        print('Фаил пустой')
        return "[]"


print(open_json(r'c:\python\project\home_work\data\operations.json'))
