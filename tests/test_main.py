import pytest
from unittest.mock import patch, MagicMock
from src.main import main
from src.processing import filter_by_state, sort_by_date


# Моки для функций open_json, open_csv, open_excel
@pytest.fixture
def mock_open_json():
    with patch("src.main.open_json") as mock:
        mock.return_value = [
            {"id": 1, "state": "EXECUTED", "date": "2023-10-01", "currency": "RUB", "description": "Payment"},
            {"id": 2, "state": "CANCELED", "date": "2023-09-15", "currency": "USD", "description": "Transfer"},
        ]
        yield mock


@pytest.fixture
def mock_open_csv():
    with patch("src.main.open_csv") as mock:
        mock.return_value = [
            {"id": 3, "state": "PENDING", "date": "2023-08-20", "currency": "RUB", "description": "Deposit"},
        ]
        yield mock


@pytest.fixture
def mock_open_excel():
    with patch("src.main.open_excel") as mock:
        mock.return_value = [
            {"id": 4, "state": "EXECUTED", "date": "2023-07-10", "currency": "EUR", "description": "Withdrawal"},
        ]
        yield mock


# Моки для функций filter_by_state и sort_by_date
@pytest.fixture
def mock_filter_by_state():
    with patch("src.main.filter_by_state") as mock:
        mock.side_effect = lambda transactions, state: [t for t in transactions if t["state"] == state]
        yield mock


@pytest.fixture
def mock_sort_by_date():
    with patch("src.main.sort_by_date") as mock:
        mock.side_effect = lambda transactions, reverse=False: sorted(
            transactions, key=lambda x: x["date"], reverse=reverse
        )
        yield mock


# Тесты
def test_main_json(mock_open_json, mock_filter_by_state, mock_sort_by_date, capsys):
    # Эмулируем ввод пользователя: 1 (JSON), 1 (EXECUTED), 1 (ДА), 2 (По убыванию), 2 (НЕТ), 2 (НЕТ)
    with patch("builtins.input", side_effect=["1", "1", "1", "2", "2", "2"]):
        result = main()

    # Проверяем, что функция вернула правильный результат
    assert result == [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01", "currency": "RUB", "description": "Payment"}
    ]

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Вы выбрали JSON-файл. Обработка JSON-файла..." in captured.out
    assert "Не найдено ни одной транзакции" not in captured.out


def test_main_csv(mock_open_csv, mock_filter_by_state, mock_sort_by_date, capsys):
    # Эмулируем ввод пользователя: 2 (CSV), 2 (CANCELED), 2 (НЕТ), 2 (НЕТ), 2 (НЕТ)
    with patch("builtins.input", side_effect=["2", "2", "2", "2", "2"]):
        result = main()

    # Проверяем, что функция вернула правильный результат
    assert result == []

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Вы выбрали CSV-файл. Обработка CSV-файла..." in captured.out
    assert "Не найдено ни одной транзакции" in captured.out


def test_main_excel(mock_open_excel, mock_filter_by_state, mock_sort_by_date, capsys):
    # Эмулируем ввод пользователя: 3 (XLSX), 1 (EXECUTED), 1 (ДА), 1 (По возрастанию), 1 (ДА), 1 (ДА), "Withdrawal"
    with patch("builtins.input", side_effect=["3", "1", "1", "1", "1", "1", "Withdrawal"]):
        result = main()

    # Проверяем, что функция вернула правильный результат
    assert result == [
        {"id": 4, "state": "EXECUTED", "date": "2023-07-10", "currency": "EUR", "description": "Withdrawal"}
    ]

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Вы выбрали XLSX-файл. Обработка XLSX-файла..." in captured.out
    assert "Не найдено ни одной транзакции" not in captured.out


def test_main_empty_list(mock_open_json, mock_filter_by_state, mock_sort_by_date, capsys):
    # Эмулируем ввод пользователя: 1 (JSON), 1 (EXECUTED), 1 (ДА), 1 (По возрастанию), 1 (ДА), 1 (ДА), "NonExistent"
    with patch("builtins.input", side_effect=["1", "1", "1", "1", "1", "1", "NonExistent"]):
        result = main()

    # Проверяем, что функция вернула пустой список
    assert result == []

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out


def test_main_invalid_input(mock_open_json, capsys):
    # Эмулируем неверный ввод пользователя: "abc", затем 0 (Завершить работу)
    with patch("builtins.input", side_effect=["abc", "0"]):
        result = main()

    # Проверяем, что функция завершилась без ошибок
    assert result is None

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Пожалуйста, введите только цифры." in captured.out
    assert "Программа завершена." in captured.out