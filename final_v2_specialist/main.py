"""Трекер задач. Финал первого курса

Создадим персональный трекер задач, который будет общаться с пользователем через стандартные потоки ввода-вывода.
Трекер хранит данные в виде пар: дата - событие.

Дата - строка следующего вида: год-месяц-день,  где год ,месяц и день - целые числа.
Событие - строка из печатных символов без внутренних разделителей. Событие не может быть пустой строкой, а также в одну
и ту же дату может произойти несколько событий. Трекер должен суметь их все сохранить. Одинаковые события произошедшие
в один и тот же день сохранять не нужно, достаточно сохранить только лишь одно из них.

Трекер должен уметь поддерживать следующие команды:
Add Дата Событие - добавление события
Del Дата Событие - удаление события
Del Дата - удаление всех событий за конкретную дату
Find Дата - поиск событий за конкретную дату
Print - печать всех событий за все даты
StartApp - команда, символизирующая начало работы с трекером
Quit - команда завершения работы трекера. Дальнейший ввод становится невозможен и трекер его игнорирует
Все команды, даты и события при вводе разделены пробелами. Команды считываются из стандартного ввода. В одной строке
может быть ровно одна команда, но можно ввести несколько команд в несколько строк. На вход также могут поступать пустые
строки — их следует игнорировать и продолжать обработку новых команд в последующих строках."""
import sqlite3


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
    date event, event, event
    Вывод date:  0000-00-00 (добавляются нули слева)"""
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        # С помощью функции get_list_date() в цикле перебор таблиц
        for date in get_list_date(db_filename):
            sql = f"SELECT * FROM [{date}]"
            cursor.execute(sql)
            events_dirty = cursor.fetchall()  # Список с кортежами event
            events = list(map(lambda x: ', '.join(x), events_dirty))  # Список с events
            # print(date, ', '.join(events))
            date = date.split('-')
            year = str(date[0]).rjust(4, '0')
            month = str(date[1]).rjust(2, '0')
            day = str(date[2]).rjust(2, '0')
            new_date = [year, month, day]
            print('-'.join(new_date), ', '.join(events))



# add_to_db('2019-01-20', 'new balance')
# add_to_db('2019-01-20', 'new balance1')
# add_to_db('2019-01-20', 'new balance1')
# add_to_db('2019-01-21', 'new balance0')
# add_to_db('2019-1-21', 'new balance2')
# add_to_db('2019-1-21', 'new balance3')
# add_to_db('2019-1-21', 'new balance4')
# add_to_db('19-01-02', 'new balance2')
print_all()