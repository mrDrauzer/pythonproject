import json
import os
import logging
from json import JSONDecodeError


logger = logging.getLogger('open_json')
logger.setLevel(logging.DEBUG)
file_handle = logging.FileHandler(os.path.join(os.path.dirname(__file__), "..", "logs", "open_json.log"), encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s- #(name)s - %(levelname)s: %(message)s')
file_handle.setFormatter(file_formatter)
logger.addHandler(file_handle)


def open_json(local_json_file=r"c:\python\project\home_work\data\operations.json"):
    """Принимат на вход сслыку на файл JSON выдает список словарей"""
    try:
        logger.debug(f'Выполнение чтения JSON')
        if not os.path.exists(local_json_file):
            print(f"Файл {local_json_file} не найден")
            return "[]"
        else:
            with open(local_json_file, encoding="utf-8") as f:
                data = json.load(f)
                return data
    except JSONDecodeError:
        logger.error((f'Произошла ошибка'))
        print("Фаил пустой")
        return "[]"


# Пример использования
# current_dir = os.path.dirname(__file__)  # Текущий каталог скрипта
# json_file = os.path.join(current_dir, "data", "operations.json")  # Относительный путь к файлу

#print(open_json(r'c:\python\project\home_work\data\operations.jso'))

# current_dir = os.path.dirname(__file__),   # Текущий каталог скрипта

json_file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.json")  # Относительный путь к файлу
print(open_json())
print(open_json(json_file))
print(json_file)
print(open_json(os.path.join(os.path.dirname(__file__), "..", "data", "empti.json")))

# local_json_file = os.path.join(os.path.dirname(__file__), "..", "data", "operations.json")
# if not os.path.exists(local_json_file):