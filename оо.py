import json
from datetime import datetime
import os

class AnalysisAndReporting:
    def __init__(self, log_file='scan_log.json', report_file='report.txt'):
        self.log_file = log_file
        self.report_file = report_file

    def log_scan(self, url, payload, params, response):
        
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'url': url,
            'payload': payload,
            'params': params,
            'status_code': response.status_code,
            'response_length': len(response.text),
            'is_error': response.status_code == 500 or 'error' in response.text.lower() or 'syntax' in response.text.lower(),
            'response_snippet': response.text[:200]  # Сохраняем только первые 200 символов
        }
        
        # Запись данных в лог-файл
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            print(f'[LOGGED] Payload: {payload} -> Status: {response.status_code}')
        except Exception as e:
            print(f'[ERROR] Failed to log scan data: {e}')

    def analyze_logs(self):
        try:
            with open(self.log_file, 'r') as f:
                logs = [json.loads(line) for line in f.readlines()]
        except FileNotFoundError:
            print('[ERROR] Log file not found.')
            return []

        vulnerabilities = []
        for log in logs:
            if log['is_error']:
                vulnerabilities.append(log)

        return vulnerabilities

    def generate_report(self, report_dir='отчет'):
        
        vulnerabilities = self.analyze_logs()
        if not vulnerabilities:
            print('[INFO] No vulnerabilities found.')
            return


        os.makedirs(report_dir, exist_ok=True)

        # Формируем полный путь к файлу отчета
        report_path = os.path.join(report_dir, self.report_file)

        try:
            with open(report_path, 'w') as f:
                f.write('SQL Injection Vulnerability Report\n')
                f.write('=' * 40 + '\n\n')
                f.write(f'Total Vulnerabilities Found: {len(vulnerabilities)}\n\n')
                
                for i, vuln in enumerate(vulnerabilities, start=1):
                    f.write(f'Vulnerability #{i}\n')
                    f.write('-' * 40 + '\n')
                    f.write(f"URL: {vuln['url']}\n")
                    f.write(f"Payload: {vuln['payload']}\n")
                    f.write(f"Parameters: {vuln['params']}\n")
                    f.write(f"Status Code: {vuln['status_code']}\n")
                    f.write(f"Response Snippet: {vuln['response_snippet']}\n")
                    f.write('-' * 40 + '\n\n')
            
            print(f'[INFO] Report generated: {report_path}')
        except Exception as e:
            print(f'[ERROR] Failed to generate report: {e}')


# Пример использования модуля
if __name__ == '__main__':
    from requests.models import Response

    # Пример симуляции вызовов
    analyzer = AnalysisAndReporting()

    # Пример использования модуля с поддельными ответами
    fake_responses = [
        {'status_code': 500, 'text': 'SQL syntax error near ...'},
        {'status_code': 200, 'text': 'Welcome, user!'},
        {'status_code': 500, 'text': 'Error: unexpected token in query'}
    ]

    fake_url = 'http://example.com/login'
    fake_params = {'username': 'admin', 'password': 'password'}
    fake_payloads = ["' OR '1'='1'--", "' UNION SELECT NULL--", "'; DROP TABLE users--"]

    # Логируем и анализируем данные
    for payload, fake_resp in zip(fake_payloads, fake_responses):
        fake_response = Response()
        fake_response.status_code = fake_resp['status_code']
        fake_response._content = fake_resp['text'].encode('utf-8')
        
        # Логирование попытки
        analyzer.log_scan(fake_url, payload, fake_params, fake_response)

    # Генерация отчета
    analyzer.generate_report()