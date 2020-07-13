""" 1) Add Дата Событие  - добавление события.
При добавлении события трекер должен его запомнить и затем показывать его
при поиске (командой Find) или печати (командой Print). Если указанное событие для данной даты уже существует,
повторное его добавление нужно игнорировать. """
import sqlite3
import os


def check_exist_date(date="", db_filename='todo_db.db'):
    """Функция проверяет существование таблицы в базе данных.
    Выводит True если совпадение найдено.
    Выводит False если совпадение не найдено."""
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        sql = f'SELECT name from sqlite_master where type= "table"'
        cursor.execute(sql)
        result = list(cursor.fetchall())
        for i in result:
            if date in ', '.join(i):
                print(', '.join(i))
                return True
        return False


def get_list_date(db_filename='todo_db.db'):
    """Функция возвращает список с таблицами"""
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        sql = f'SELECT name from sqlite_master where type= "table"'
        cursor.execute(sql)
        result_dirty = cursor.fetchall()  # Список с кортежами
        result = list(map(lambda x: ', '.join(x), result_dirty))  # Преобразует в список
        return result


def add_to_db(date, event, db_filename='todo_db.db'):
    """Функция создает to_do.db
    создает таблицы
    дабавляет события к таблице, если событие имеется - игнорирует"""
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        sql = f"INSERT INTO [{date}] VALUES(?)"
        try:
            cursor.execute(sql, (event,))
            print('Try')
        except sqlite3.OperationalError:
            cursor = conn.cursor()
            sql_newtable = f"CREATE TABLE IF NOT EXISTS [{date}] (events TEXT UNIQUE)"
            cursor.execute(sql_newtable)
            cursor.execute(sql, (event,))
            print('nado dobavit')
        except sqlite3.IntegrityError:
            print('nothing doing')


def get_find(date, event='', db_filename='to_do.db'):
    if event:
        sql = f'SELECT {event} FROM {date}'
        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)


def print_all(db_filename='todo_db.db'):
    """Функция распечатывает все события трекера в формате
    date event, event, event"""
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        # С помощью функции get_list_date() в цикле перебор таблиц
        for date in get_list_date(db_filename):
            sql = f"SELECT * FROM [{date}]"
            cursor.execute(sql)
            events_dirty = cursor.fetchall()  # Список с кортежами event
            events = list(map(lambda x: ', '.join(x), events_dirty))  # Список с events
            print(date, ', '.join(events))





# create_new_db('2011', 'do english')
add_to_db('2019-01-20', 'new balance')
add_to_db('2019-01-20', 'new balance1')
add_to_db('2019-01-20', 'new balance1')
add_to_db('2019-01-21', 'new balance0')
add_to_db('2019-01-21', 'new balance2')
add_to_db('2019-01-21', 'new balance3')
add_to_db('2019-01-21', 'new balance4')
add_to_db('2019-01-22', 'new balance2')
# add_to_db('2020', 'voice')
# print(create_new_db('werer', 'werwerwerer'))
print_all()