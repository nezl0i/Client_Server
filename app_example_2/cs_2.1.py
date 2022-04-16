"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции
создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета
в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также
оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import os
import re
from chardet.universaldetector import UniversalDetector


def get_file(file_name):
    detector = UniversalDetector()
    with open(file_name, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    with open(file_name, encoding=detector.result['encoding']) as f:
        return f.readlines()


def spl_str(line):
    return line.split(":")[1].strip()


def get_data():
    os_prod_list: list = []
    os_name_list: list = []
    os_code_list: list = []
    os_type_list: list = []
    main_data: list = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    dir_name = 'files/'
    files = os.listdir(dir_name)
    for file in files:
        file_name = os.path.join(dir_name, file)
        for line in get_file(file_name):
            if re.findall(r'Название ОС', line):
                os_name_list.append(spl_str(line))
            if re.findall(r'Изготовитель ОС', line):
                os_prod_list.append(spl_str(line))
            if re.findall(r'Код продукта', line):
                os_code_list.append(spl_str(line))
            if re.findall(r'Тип системы', line):
                os_type_list.append(spl_str(line))
                break
    for i in zip(os_prod_list, os_name_list, os_code_list, os_type_list):
        main_data.append(list(i))
    return main_data


def write_to_csv(file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(get_data())


write_to_csv('os_list.csv')
