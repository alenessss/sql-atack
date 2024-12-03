from flask import Flask, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)