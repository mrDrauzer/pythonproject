from src.utils import open_json, open_csv, open_excel
from src.processing import filter_by_state, sort_by_date
from collections import Counter
import re


def count_operations_by_category(operations, categories):
    """
    Подсчитывает количество операций по заданным категориям.

    :param operations: Список словарей с операциями.
    :param categories: Список категорий для подсчёта.
    :return: Словарь вида {"категория_1": 2, "категория_2": 3}.
    """
    category_counter = Counter()
    for operation in operations:
        if 'category' in operation and operation['category'] in categories:
            category_counter[operation['category']] += 1
    return dict(category_counter)


def main():
    print(f"""                                                                                                              
8888888b.          d8b                   888    888 
888   Y88b         Y8P                   888    888 
888    888                               888    888 
888   d88P 888d888 888 888  888  .d88b.  888888 888 
8888888P"  888P"   888 888  888 d8P  Y8b 888    888 
888        888     888 Y88  88P 88888888 888    Y8P 
888        888     888  Y8bd8P  Y8b.     Y88b.   "  
888        888     888   Y88P    "Y8888   "Y888 888 

    Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню Получить информацию о транзакциях из:""")
    options = [1, 2, 3, 0]
    while options:
        print(" 1. [JSON-файла]   2. [CSV-файла]   3. [XLSX-файла]    0. [Завершить работу]")
        choice = input("Ваш выбор: ")

        # Проверка на ввод пользователя
        if not choice.isdigit():
            print("Пожалуйста, введите только цифры.")
            continue

        # Проверка на допустимость выбора
        if int(choice) not in options:
            print(f"Такой вариант отсутствует. Выберите другой вариант.")
            continue

        # Обработка выбора файла
        if int(choice) == 1:
            print("Вы выбрали JSON-файл. Обработка JSON-файла...")
            list_transac = open_json()

        elif int(choice) == 2:
            print("Вы выбрали CSV-файл. Обработка CSV-файла...")
            list_transac = open_csv()

        elif int(choice) == 3:
            print("Вы выбрали XLSX-файл. Обработка XLSX-файла...")
            list_transac = open_excel()

        elif int(choice) == 0:
            print("Программа завершена.")
            return

        # Проверка на пустой список
        if not list_transac:
            print("Файл пуст или данные не загружены. Программа завершена.")
            return

        # Фильтрация по статусу
        print(f"""
    Выберети статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы:

    1.EXECUTED [ВЫПОЛНЕНО]
    2.CANCELED [ОТМЕНЕНО]
    3.PENDING  [ОЖИДАЕТСЯ] """)
        options_stat = ["1.0", "1", "EXECUTED", "2.0", "2", "CANCELED", "3.0", "3", "PENDING"]
        type_status = input().upper()

        if type_status not in options_stat:
            print(f"Такой вариант отсутствует. Выберите другой вариант.")
            continue

        operation_status = None
        if type_status in ("1.0", "1", "EXECUTED"):
            operation_status = "EXECUTED"
        elif type_status in ("2.0", "2", "CANCELED"):
            operation_status = "CANCELED"
        elif type_status in ("3.0", "3", "PENDING"):
            operation_status = "PENDING"

        list_transac = filter_by_state(list_transac, operation_status)

        # Сортировка по дате
        print(f"""
        Отсортировать операции по дате? Да/Нет

        1.ДА
        2.НЕТ """)
        options_data_sorted = ["1.0", "1", "YES", "ДА", "2.0", "2", "НЕТ", "NO"]
        data_sorted = input().upper()

        if data_sorted not in options_data_sorted:
            print(f"Такой вариант отсутствует. Выберите другой вариант.")
            continue

        if data_sorted in ("1.0", "1", "YES", "ДА"):
            print(f"""Отсортировать по возрастанию или по убыванию?
            1.По возрастанию
            2.По убыванию """)
            options_sorted = ["1.0", "1", "ПО ВОЗРАСТАНИЮ", "2.0", "2", "ПО УБЫВАНИЮ"]
            type_data_sorted = input().upper()

            if type_data_sorted not in options_sorted:
                print(f"Такой вариант отсутствует. Выберите другой вариант.")
                continue

            reverse = type_data_sorted in ("2.0", "2", "ПО УБЫВАНИЮ")
            list_transac = sort_by_date(list_transac, reverse=reverse)

        # Фильтрация по рублевым транзакциям
        print(f"""Выводить только рублевые тразакции? Да/Нет?
        1.ДА
        2.НЕТ""")
        currency_choice = input().upper()

        if currency_choice in ("1.0", "ДА", "YES"):
            list_transac = [t for t in list_transac if t.get("currency") == "RUB"]

        # Фильтрация по ключевому слову
        print(f"""Отфильтровать список транзакций по определенному слову в описании? Да/Нет?
                1.ДА
                2.НЕТ""")
        filter_choice = input().upper()

        if filter_choice in ("1.0", "1", "ДА", "YES"):
            keyword = input("Введите слово для фильтрации: ")
            list_transac = [t for t in list_transac if
                            isinstance(t, dict) and re.search(keyword, t.get("description", ""), re.IGNORECASE)]

        # Подсчёт операций по категориям
        categories = ["перевод", "покупка", "оплата"]  # Пример списка категорий
        category_counts = count_operations_by_category(list_transac, categories)
        print("Количество операций по категориям:", category_counts)

        # Вывод результата
        if not list_transac:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        else:
            for transaction in list_transac:
                print(transaction)

        return list_transac