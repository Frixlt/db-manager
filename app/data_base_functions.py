import sqlite3
import threading

TABLE_NAME = "acaunts"
COLUMN_NAMES = ["server", "login", "passworld", "email", "lvl", "RP", "kapsules", "last"]
BASE = 'data/general_base.db'

connection = threading.local()


def connect():
    # Подключение к базе данных
    try:
        if not hasattr(connection, "conn"):
            connection.conn = sqlite3.connect(BASE)
        return connection.conn
    except sqlite3.Error as error:
        print(
            "Не удалось подключиться к базе данных:", error)


def disconnect():
    # Отключение от базы данных
    try:
        if hasattr(connection, "conn"):
            connection.conn.close()
            del connection.conn
    except sqlite3.Error as error:
        return ("Не удалось отключиться от базы данных:", error)


def create_table():
    # Создание таблицы
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {' TEXT, '.join(COLUMN_NAMES)} TEXT
        );""")
        conn.commit()
        return (True)
    except sqlite3.Error as error:
        return ("Не удалось создать таблицу:", error)
    finally:
        disconnect()


def add_row(data, colums = COLUMN_NAMES):
    # Добавление новой записи
    try:
        conn = connect()
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(colums))
        cursor.execute(
            f"INSERT INTO {TABLE_NAME} ({','.join(colums)}) VALUES ({placeholders})", data)
        conn.commit()
        return (True)
    except sqlite3.Error as error:
        return ("Не удалось добавить запись:", error)
    finally:
        disconnect()


def get_all_rows():
    # Получение всех записей
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as error:
        return ("Не удалось получить записи:", error)
    finally:
        disconnect()


def get_row_by_id(row_id):
    # Получение записи по ID
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (row_id,))
        row = cursor.fetchone()
        return row
    except sqlite3.Error as error:
        return ("Не удалось получить запись:", error)
    finally:
        disconnect()


def delete_table():
    # Удаление таблицы
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        conn.commit()
        return (True)
    except sqlite3.Error as error:
        return ("Не удалось удалить таблицу:", error)
    finally:
        disconnect()


def delete_row_by_id(row_id):
    # Удаление записи по ID
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (row_id,))
        conn.commit()
        return (True)
    except sqlite3.Error as error:
        return ("Не удалось удалить запись:", error)
    finally:
        disconnect()


def get_column_data(column):
    # Получение данных из указанного столбца
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column} FROM {TABLE_NAME}")
        data = cursor.fetchall()
        return data
    except sqlite3.Error as error:
        return ("Не удалось получить данные из столбца:", error)
    finally:
        disconnect()


def update_row(row_id, data):
    # Обновление записи по ID
    try:
        conn = connect()
        cursor = conn.cursor()
        set_clause = ', '.join(
            [f"{COLUMN_NAMES[i]} = ?" for i in range(len(COLUMN_NAMES))])
        cursor.execute(
            f"UPDATE {TABLE_NAME} SET {set_clause} WHERE id = ?", (*data, row_id))
        conn.commit()
        return (True)
    except sqlite3.Error as error:
        return ("Не удалось обновить запись:", error)
    finally:
        disconnect()


def get_column_names():
    # Получение названий столбцов таблицы
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
        columns = [column[1] for column in cursor.fetchall()]
        conn.commit()
        return columns
    except sqlite3.Error as error:
        return ("Не удалось получить названия столбцов:", error)
    finally:
        disconnect()


if __name__ == "__main__":
    # # Подключение к базе данных
    delete_table()
    # Создание таблицы
    create_table()