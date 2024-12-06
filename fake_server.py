from flask import Flask, request

app = Flask(__name__) #В данной строке мы создание экземпляра приложения Flask. Имя модуля только такой __name__ иначе ошибка при запуске.

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    # Эмуляция уязвимости для тестирования
    if password in [
        "' OR '1'='1'--",
        "' UNION SELECT NULL, NULL--",
        "' AND 1=1--",
        "'; DROP TABLE users--",
        "'; EXEC xp_cmdshell('ping 127.0.0.1')--"
    ]:
        return "Обнаружена потенциальная SQL-инъекция!", 500
    
    return f"Полученное имя пользователя: {username}, пароль: {password}", 200

@app.route('/xss', methods=['GET'])
def xss():
    user_input = request.args.get('input', '')
    
    # НЕ ЭКРАНИРУЕМ ввод для тестирования уязвимости
    sanitized_input = user_input  # НЕ Экранируем специальный HTML-код
    
    # Эмуляция уязвимости XSS для тестирования
    response = f"""
    <html>
        <body>
            <h1>Ваш ввод:</h1>
            <p>{sanitized_input}</p>
        </body>
    </html>
    """
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)
