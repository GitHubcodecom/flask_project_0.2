import sqlite3  # Импортируем модуль для работы с SQLite
import hashlib  # Импортируем модуль для хэширования паролей

DB_PATH = r"C:\Users\Lenovo\Pictures\flask v2\database.db"  # Указываем путь к файлу базы данных

import bcrypt

def hash_password(password):
    """
    Функция для безопасного хэширования пароля с использованием bcrypt.
    :param password: Пароль в виде строки.
    :return: Хэш пароля в виде строки (форматируемый bcrypt-хэш).
    """
    # Генерация соли и хэширование пароля
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')




def get_db_connection():
    """
    Функция для получения соединения с базой данных.
    :return: Объект соединения с базой данных.
    """
    conn = sqlite3.connect(DB_PATH)  # Подключаемся к базе данных
    conn.row_factory = sqlite3.Row  # Устанавливаем формат результатов в виде словарей
    return conn  # Возвращаем соединение

def init_db():
    """
    Функция для инициализации базы данных.
    Создает таблицу users, если она не существует.
    """
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор для выполнения SQL запросов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        level INTEGER DEFAULT 10,
        password TEXT NOT NULL
    )
    """)  # Создаем таблицу users
    conn.commit()  # Фиксируем изменения
    conn.close()  # Закрываем соединение

def init_db_clients():
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор для выполнения SQL запросов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        info TEXT NOT NULL
    )
    """)  # Создаем таблицу users
    conn.commit()  # Фиксируем изменения
    conn.close()  # Закрываем соединение
    


def add_user(name, level=10, password=None):
    """
    Функция для добавления нового пользователя в базу данных.
    :param name: Имя пользователя.
    :param level: Уровень доступа пользователя.
    :param password: Пароль пользователя.
    """
    if password is None:
        raise ValueError("Пароль обязателен.")  # Проверяем, что пароль не пустой
    hashed_password = hash_password(password)  # Хэшируем пароль
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("INSERT INTO users (name, level, password) VALUES (?, ?, ?)", (name, level, hashed_password))
    # Выполняем SQL запрос на вставку нового пользователя
    conn.commit()  # Фиксируем изменения
    conn.close()  # Закрываем соединение

def remove_user(user_id):
    """
    Функция для удаления пользователя из базы данных.
    :param user_id: Идентификатор пользователя для удаления.
    :return: True, если пользователь был удален, иначе False.
    """
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))  # Выполняем SQL запрос на удаление
    rows_deleted = cursor.rowcount  # Получаем количество удаленных строк
    conn.commit()  # Фиксируем изменения
    conn.close()  # Закрываем соединение
    return rows_deleted > 0  # Возвращаем результат

def get_all_users():
    """
    Функция для получения списка всех пользователей.
    :return: Список пользователей в виде словарей.
    """
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("SELECT id, name, level FROM users")  # Выполняем SQL запрос
    users = [dict(row) for row in cursor.fetchall()]  # Преобразуем результаты в список словарей
    conn.close()  # Закрываем соединение
    return users  # Возвращаем список пользователей

    
    
def verify_user(name, password):
    """
    Функция для проверки имени пользователя и пароля.
    :param name: Имя пользователя.
    :param password: Пароль пользователя.
    :return: True, если данные верны, иначе False.
    """
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("SELECT password FROM users WHERE name = ?", (name,))  # Получаем хэш пароля из базы данных
    result = cursor.fetchone()  # Получаем результат
    conn.close()  # Закрываем соединение
    if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
        # Сравниваем хэшированный пароль с введенным паролем
        return result, True
    return result, False


def get_user_level(name):
    """
    Функция для получения уровня доступа пользователя.
    :param name: Имя пользователя.
    :return: Уровень доступа пользователя или None.
    """
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("SELECT level FROM users WHERE name = ?", (name,))  # Выполняем SQL запрос
    result = cursor.fetchone()  # Получаем результат
    conn.close()  # Закрываем соединение
    if result:
        return result['level']  # Возвращаем уровень пользователя
    return None  # Если пользователь не найден, возвращаем None

def add_client(name, info):
    conn = get_db_connection()  # Получаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("INSERT INTO clients (name, info) VALUES (?, ?)", (name, info))
    # Выполняем SQL запрос на вставку нового пользователя
    conn.commit()  # Фиксируем изменения
    conn.close()  # Закрываем соединение

if __name__ == "__main__":
    init_db()  # Инициализируем базу данных
    # Пример добавления администратора
    init_db_clients()
    add_client("marsik", "meow, hochu est'")
    """
    try:
        add_user("admin", level=0, password="1234")  # Добавляем администратора
        print("Администратор успешно добавлен.")  # Выводим сообщение
    except Exception as e:
        print(f"Ошибка при добавлении администратора: {e}")  # Выводим ошибку
"""