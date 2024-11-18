import json
import os
import logging
from json import JSONDecodeError
from venv import logger

logger = logging.getLogger('open_json')
logger.setLevel(logging.INFO)
file_handle = logging.FileHandler('logs/open_json.log')
file_formatter = logging.Formatter('%(asctime)s- #(name)s - %(levelname)s: %(message)s')
file_handle.setFormatter(file_formatter)
logger.addHandler(file_handle)



def open_json(local_json_file=r"c:\python\project\home_work\data\operations.json"):
    """Принимат на вход сслыку на файл JSON выдает список словарей"""
    try:
        logerr.info(f'Выполнение чтения JSON')
        if not os.path.exists(local_json_file):
            print(f"Файл {local_json_file} не найден")
            return "[]"
        else:
            with open(local_json_file, encoding="utf-8") as f:
                data = json.load(f)
                return data
    except JSONDecodeError:
        print("Фаил пустой")
        return "[]"


# print(open_json(r'c:\python\project\home_work\data\operations.json'))
