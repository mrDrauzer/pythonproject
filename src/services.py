import json
from datetime import datetime
from collections import defaultdict
import logging
from typing import List, Dict, Any

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def analyze_categories(data, year, month):
    """
    Анализирует данные транзакций и возвращает JSON с суммой возможного кешбэка по категориям.

    :param data: список словарей с транзакциями
    :param year: год для анализа
    :param month: месяц для анализа
    :return: JSON с суммой возможного кешбэка по категориям
    """
    try:
        # Фильтрация транзакций по указанному периоду
        filtered_data = list(filter(
            lambda x: datetime.strptime(x['date'], '%Y-%m-%d').year == year
                      and datetime.strptime(x['date'], '%Y-%m-%d').month == month,
            data
        ))

        # Группировка по категориям и суммирование сумм
        category_sums = defaultdict(int)
        for transaction in filtered_data:
            category_sums[transaction['category']] += transaction['amount']

        # Преобразование в JSON
        result = {
            category: round(amount * 0.01, 2)  # 1% кешбэка
            for category, amount in category_sums.items()
        }

        logging.info(f"Анализ категорий за {year}-{month} выполнен успешно")
        return json.dumps(result)

    except Exception as e:
        logging.error(f"Ошибка при анализе категорий: {e}")
        return {}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инвесткопилка
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для «Инвесткопилки» путем округления транзакций до заданного предела.

    :param month: Месяц в формате 'YYYY-MM'.
    :param transactions: Список транзакций вида [{'Дата операции': 'YYYY-MM-DD', 'Сумма операции': 100.0}].
    :param limit: Предел округления (10, 50, 100 и т. д.).
    :return: Сумма накоплений.
    """
    try:
        total_savings = 0.0
        year, month_num = map(int, month.split('-'))

        for transaction in transactions:
            date_str = transaction.get('Дата операции', '')
            amount = transaction.get('Сумма операции', 0)

            # Проверяем, что транзакция относится к нужному месяцу
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                if date.year != year or date.month != month_num:
                    continue
            except ValueError:
                logger.warning(f"Неверный формат даты в транзакции: {date_str}")
                continue

            # Округляем сумму и добавляем разницу в копилку
            if amount > 0:
                rounded = ((amount // limit) + 1) * limit
                savings = rounded - amount
                total_savings += savings
                logger.debug(f"Транзакция {amount} ₽ → округлено до {rounded} ₽ (+{savings} ₽)")

        logger.info(f"Итоговая сумма за {month}: {total_savings:.2f} ₽")
        return round(total_savings, 2)

    except Exception as e:
        logger.error(f"Ошибка в функции investment_bank: {e}", exc_info=True)
        return 0.0