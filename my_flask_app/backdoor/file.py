#файл только для 
import hashlib  # Импортируем модуль для хэширования паролей
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
status = True
try:
    hard_path1 = r"C:\Users\Lenovo\Pictures\flask v2\my_flask_app\database.db"
    hard_path2 = r"C:\Users\Lenovo\Pictures\flask v2\database.db"
    login = input("Enter login: ")
    password = input("Password: ")
    password = hash_password(password)
    print(password)
    status = True
except:
    status = False
if status:
    pass