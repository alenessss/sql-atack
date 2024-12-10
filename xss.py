import os
import requests
from datetime import datetime

# Адрес вашего веб-приложения
url = 'http://localhost:5000/'

# Список полезных нагрузок для тестирования XSS атак
payloads = [
    "<script>alert('XSS')</script>",  # Простейшая XSS атака
    "<img src='x' onerror='alert(1)'>",  # Использование события onerror
    "<script>document.write('<img src=x onerror=alert(1)>');</script>",  # Динамическая загрузка
    "<svg/onload=alert(1)>",  # SVG-based XSS
    "<iframe src='javascript:alert(1)'></iframe>",  # Вставка iframe с JS
]

# Функция для отправки данных на сервер и проверки на XSS
def test_xss():
    results = []
    for payload in payloads:
        # Подготовка данных формы для тестирования
        data = {'message': payload}
        
        # Отправляем запрос POST на главную страницу
        response = requests.post(url, data=data)

        # Проверяем, присутствует ли наша нагрузка в ответе
        if payload in response.text:
            results.append({
                'payload': payload,
                'response': response.text[:500]  # Ограничиваем размер ответа, чтобы не перегружать отчет
            })
            print(f"Тестирование с полезной нагрузкой: {payload}")
            print("[+] Уязвимость обнаружена.")
        else:
            print(f"Тестирование с полезной нагрузкой: {payload}")
            print("[+] Уязвимость не обнаружена.")
    return results

# Генерация отчета
def generate_report(results):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Создаём папку для отчетов "Отчеты", если она не существует
    if not os.path.exists('Отчеты'):
        os.makedirs('Отчеты')

    # Формируем контент отчета
    report_content = f"Отчет о тестировании XSS атак\n{'='*40}\n"
    report_content += f"Дата проверки: {now}\n"
    report_content += f"Всего тестов: {len(payloads)}\n"
    report_content += f"Количество уязвимостей: {len(results)}\n\n"

    # Добавляем только те полезные нагрузки, которые прошли тест
    if results:
        report_content += "Подробности о найденных уязвимостях:\n"
        report_content += "-" * 40 + "\n"
        for result in results:
            report_content += f"Полезная нагрузка: {result['payload']}\n"
            report_content += f"Ответ сервера: {result['response']}\n\n"
    else:
        report_content += "Уязвимости не обнаружены.\n"
    
    # Сохраняем отчет в файл в папке "Отчеты"
    report_filename = f"XSS_Отчет.txt"
    with open(f'Отчеты/{report_filename}', 'w') as report_file:
        report_file.write(report_content)

    print(f"[INFO] Отчет сохранен в: Отчеты/{report_filename}")

# Главная функция для тестирования
if __name__ == '__main__':
    results = test_xss()
    generate_report(results)