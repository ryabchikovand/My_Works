"""использовать список хостов из текстового файла
путь к файлу со списком должен передаваться через аргумент запуска скрипта
запуск скрипта должен работать в рамках одной сессии, по окончанию закрыть сессию авторизации.
Формат текстового файла:

HostName TypeCheck IP Port

Server1 SNMP 10.10.10.10 161

Server2 Agent 10.10.10.11 10051"""
from pyzabbix import ZabbixAPI
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, action='store', help='Input dir for hosts file', required=True)
file_path = str(parser.parse_args().path)
filename = file_path.split('/')


def check_file(filename: str):
    """Return True if file exist, Return FileExistsError if file doesn't exist"""
    if os.path.isfile(filename):
        return True
    else:
        raise FileExistsError


def gen(filename: str):
    """Генератор - для экономии ОЗУ, если файлы будут очень большими, здесь это избыточно, сделал, чтобы показать,
    что в генераторы я тоже могу.
    Здесь можно добвать цикл for и на вход подавать список из файлов."""
    yield open(filename, "r")


def liner(filename: str):
    """Читает по строчно, опять же для экономии ОЗУ."""
    for fname in filename:
        for line in fname:
            yield line.strip('\n')


def create_host_to_zabbix(hostname: str, ip: str, port: str):
    """Функция создает host в zabbix
    Логин/пароль и url оставил в функции, при необходимости можно брать из файла или позволить пользователю вводить через input"""
    url = 'http://192.168.0.38/'
    with ZabbixAPI(url, user='Admin', password='zabbix') as zapi:
        # auth_api = zapi.auth
        # get_host = zapi.host.get()
        # for host in get_host:
        #     print(host['host'])
        data = {
            "host": hostname,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": port
                }
            ],
            "groups": [
                {
                    "groupid": "2"
                }
            ],
        }
        add_host = zapi.host.create(data)


try:
    if check_file(file_path) is True: # Проверка на существование файла
        for line in liner(gen(file_path)): # Генератор
            if len(line) != 0:
                hostname = line.split()[0]
                if hostname == "HostName": # Первая строчка в файле не читается
                    continue
                type_zabbix = line.split()[1]
                ip = line.split()[2]
                port = line.split()[3]
                create_host_to_zabbix(hostname, ip, port)
                print("Сервер добавлен: ", hostname, type_zabbix, ip, port)
            else:
                continue
except FileExistsError:
    print(f"{filename[-1]} doesn't exist")
