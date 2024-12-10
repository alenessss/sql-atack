from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import logging

app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), 'site.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Настроим логирование
logging.basicConfig(level=logging.DEBUG)

# Определение модели базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Создание всех таблиц в базе данных
with app.app_context():
    db.create_all()  # Создаем таблицы

# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        message = request.form.get('message', '')
    
    users = db.session.execute(text("SELECT * FROM user")).fetchall()  # Используем сырые SQL-запросы
    return render_template('index.html', users=users, message=message)  # Отправляем сообщение в шаблон

# Страница добавления пользователя
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        if username and email:
            try:
                # Добавляем пользователя в базу данных
                new_user = User(username=username, email=email)
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                app.logger.error(f"Error adding user: {e}")
                db.session.rollback()

        return redirect(url_for('index'))  # Перенаправляем на главную страницу

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)