import hashlib  # Импортируем модуль для хэширования паролей
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
# Импортируем необходимые функции и классы из Flask
from database import init_db, add_user, add_client, remove_user, get_all_users, verify_user, get_user_level
# Импортируем функции для работы с базой данных из модуля database.py
from datetime import datetime  # Импортируем класс для работы с датой и временем
import os  # Импортируем модуль для работы с операционной системой
import sqlite3

app = Flask(__name__)  # Создаем экземпляр Flask приложения
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')  # Устанавливаем секретный ключ для сессий

LOG_FILE = "log.txt"  # Указываем имя файла для логирования

def write_log(message):
    """
    Функция для записи сообщений в лог-файл.
    :param message: Текст сообщения для записи в лог.
    """
    with open(LOG_FILE, mode="a", encoding="UTF-8") as log:
        # Открываем файл логов в режиме добавления
        log.write(f"{datetime.now()} - {message}\n")  # Записываем сообщение с текущей датой и временем

@app.route('/')
def login_page():
    """
    Маршрут для отображения страницы входа.
    """
    if 'username' in session:
        # Если пользователь уже вошел в систему, перенаправляем на /home
        return redirect(url_for('home'))
    return render_template('login.html')  # Отображаем шаблон login.html

@app.route('/login', methods=['POST'])
def login():
    """
    Обработка данных формы входа.
    """
    username = request.form.get('username')  # Получаем имя пользователя из формы
    password = request.form.get('password')  # Получаем пароль из формы
    login = (verify_user(username, password))[0]
    if (verify_user(username, password))[1]:
        # Проверяем корректность введенных данных
        session['username'] = username  # Сохраняем имя пользователя в сессии
        session['user_level'] = get_user_level(username)  # Сохраняем уровень пользователя в сессии
        write_log(f"Пользователь {username} вошел в систему.")  # Записываем в лог
        return redirect(url_for('home'))  # Перенаправляем на главную страницу
    else:
        print(login)
        flash("Неверный логин или пароль.")  # Выводим сообщение об ошибке
        return redirect(url_for('login_page'))  # Перенаправляем на страницу входа

@app.route('/logout')
def logout():
    """
    Маршрут для выхода из системы.
    """
    if 'username' in session:
        # Проверяем, что пользователь вошел в систему
        username = session.get('username')  # Получаем имя пользователя из сессии
        session.clear()  # Очищаем сессию
        write_log(f"Пользователь {username} вышел из системы.")  # Записываем в лог
        flash("Вы успешно вышли из системы.")  # Выводим сообщение
    else:
        flash("Вы не были авторизованы.")  # Если пользователь не был авторизован
    return redirect(url_for('login_page'))  # Перенаправляем на страницу входа

@app.route('/home')
def home():
    """
    Главная страница приложения.
    """
    if 'username' not in session:
        # Проверяем, что пользователь вошел в систему
        flash("Пожалуйста, войдите в систему.")
        return redirect(url_for('login_page'))
    users = get_all_users()  # Получаем список всех пользователей
    return render_template('index.html', users=users, user_level=session.get('user_level'))  # Отображаем шаблон с данными

@app.route('/add_user', methods=['GET', 'POST'])
def add_user_route():
    """
    Маршрут для добавления нового пользователя.
    """
    if 'username' not in session:
        # Проверяем, что пользователь вошел в систему
        flash("Пожалуйста, войдите в систему.")
        return redirect(url_for('login_page'))
    if session.get('user_level', 10) > 1:
        # Проверяем, что пользователь является администратором
        flash("Требуется доступ администратора.")
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Обработка данных из формы
        name = request.form.get('name')  # Получаем имя нового пользователя
        level = request.form.get('level', 10)  # Получаем уровень доступа
        password = request.form.get('password')  # Получаем пароль
        
        if not name or not password:
            # Проверяем, что имя и пароль не пустые
            flash("Имя пользователя и пароль обязательны.")
            return redirect(url_for('add_user_route'))  # Перенаправляем обратно на форму
        
        try:
            add_user(name, int(level), password)  # Добавляем пользователя в базу данных
            write_log(f"Добавлен пользователь: {name} с уровнем {level}")  # Записываем в лог
            flash("Пользователь успешно добавлен.")  # Выводим сообщение
            return redirect(url_for('home'))  # Перенаправляем на главную страницу
        except Exception as e:
            write_log(f"Ошибка добавления пользователя: {e}")  # Записываем ошибку в лог
            flash("Не удалось добавить пользователя.")  # Выводим сообщение об ошибке
            return redirect(url_for('add_user_route'))  # Перенаправляем обратно на форму
    else:
        # Отображение формы для добавления пользователя
        return render_template('add_user.html')  # Отображаем шаблон формы

@app.route('/add_client', methods=['GET', 'POST'])
def add_client_route():
    """
    Маршрут для добавления нового пользователя.
    """
    if 'username' not in session:
        # Проверяем, что пользователь вошел в систему
        flash("Пожалуйста, войдите в систему.")
        return redirect(url_for('login_page'))
    if session.get('user_level', 10) > 4:
        # Проверяем, что пользователь является администратором
        flash("Требуется доступ администратора.")
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Обработка данных из формы
        name = request.form.get('name')  # Получаем имя нового пользователя
        info = request.form.get('info')  
        """
        if not name or not info:
            # Проверяем, что имя и пароль не пустые
            flash("Имя пользователя и информация обязательны.")
            return redirect(url_for('add_client_route'))  # Перенаправляем обратно на форму
        """
        try:
            add_client(name, info)  # Добавляем пользователя в базу данных
            write_log(f"Добавлен клиент: {name}. Информация:{info}")  # Записываем в лог
            flash("Kлиент успешно добавлен.")  # Выводим сообщение
            return redirect(url_for('home'))  # Перенаправляем на главную страницу
        except Exception as e:
            write_log(f"Ошибка добавления клиента: {e}")  # Записываем ошибку в лог
            flash("Не удалось добавить клиента.")  # Выводим сообщение об ошибке
            return redirect(url_for('add_client_route'))  # Перенаправляем обратно на форму
    else:
        # Отображение формы для добавления пользователя
        return render_template('add_client.html')  # Отображаем шаблон формы

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    """
    Маршрут для удаления пользователя.
    :param user_id: Идентификатор пользователя для удаления.
    """
    if 'username' not in session:
        # Проверяем, что пользователь вошел в систему
        flash("Пожалуйста, войдите в систему.")
        return redirect(url_for('login_page'))
    if session.get('user_level', 10) > 1:
        # Проверяем, что пользователь является администратором
        flash("Требуется доступ администратора.")
        return redirect(url_for('home'))
        
    try:
        if remove_user(user_id):
            # Если пользователь успешно удален
            write_log(f"Пользователь с ID {user_id} удален")  # Записываем в лог
            flash("Пользователь успешно удален.")  # Выводим сообщение
            return redirect(url_for('home'))  # Перенаправляем на главную страницу
        else:
            flash("Пользователь не найден.")  # Выводим сообщение об ошибке
            return redirect(url_for('home'))  # Перенаправляем на главную страницу
    except Exception as e:
        write_log(f"Ошибка удаления пользователя: {e}")  # Записываем ошибку в лог
        flash("Не удалось удалить пользователя.")  # Выводим сообщение об ошибке
        return redirect(url_for('home'))  # Перенаправляем на главную страницу

@app.route('/api/users', methods=['GET'])
def api_get_users():
    """
    API маршрут для получения списка пользователей.
    """
    if 'username' not in session:
        # Проверяем, что пользователь вошел в систему
        return jsonify({"error": "Unauthorized"}), 401
    if session.get('user_level', 10) > 1:
        # Проверяем, что пользователь является администратором
        return jsonify({"error": "Forbidden"}), 403
    users = get_all_users()  # Получаем список пользователей
    return jsonify(users)  # Возвращаем данные в формате JSON

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Маршрут для регистрации нового пользователя.
    """
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Проверяем введенные данные
        if not username or not password:
            flash("Имя пользователя и пароль обязательны.")
            return redirect(url_for('register'))
        if password != confirm_password:
            flash("Пароли не совпадают.")
            return redirect(url_for('register'))
        
        try:
            # Добавляем нового пользователя
            add_user(username, password=password)
            write_log(f"Зарегистрирован новый пользователь: {username}")
            flash("Регистрация прошла успешно. Теперь вы можете войти в систему.")
            return redirect(url_for('login_page'))
        except sqlite3.IntegrityError:
            flash("Пользователь с таким именем уже существует.")
        except Exception as e:
            write_log(f"Ошибка регистрации пользователя: {e}")
            flash("Произошла ошибка при регистрации.")
        return redirect(url_for('register'))
    
    # Отображаем форму регистрации
    return render_template('register.html')


if __name__ == '__main__':
    init_db()  # Инициализируем базу данных при запуске приложения
    app.run(port = "12341",debug=True)  # Запускаем приложение Flask


