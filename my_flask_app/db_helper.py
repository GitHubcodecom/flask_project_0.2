import sqlite3

def show_tables_and_data(db_file):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Получение всех названий таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("В базе данных нет таблиц.")
            return

        print("Таблицы в базе данных:")
        for table in tables:
            print(f"- {table[0]}")

        # Вывод данных из каждой таблицы
        for table in tables:
            table_name = table[0]
            print(f"\nДанные из таблицы '{table_name}':")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Получение названий колонок
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]
            print(" | ".join(columns))

            # Печать строк
            if rows:
                for row in rows:
                    print(row)
            else:
                print("Таблица пуста.")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        if conn:
            conn.close()

import sqlite3

def delete_table(db_file, table_name):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Проверяем, существует ли таблица
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        if not cursor.fetchone():
            print(f"Таблица '{table_name}' не найдена в базе данных.")
            return

        # Удаление таблицы
        cursor.execute(f"DROP TABLE {table_name};")
        conn.commit()
        print(f"Таблица '{table_name}' успешно удалена.")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        if conn:
            conn.close()

# Укажите путь к вашему файлу базы данных и имя таблицы для удаления
if input() == "1":
    db_file_path = "database.db"
    table_to_delete = "clients"
    delete_table(db_file_path, table_to_delete)

# Укажите путь к вашему файлу базы данных
db_file_path = "database.db"
show_tables_and_data(db_file_path)
