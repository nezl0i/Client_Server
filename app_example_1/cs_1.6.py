"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл в неизвестной
кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""

from chardet import detect

with open('test_file.txt', 'w+', encoding='utf-8') as f:
    f.write('сетевое программирование\nсокет\nдекоратор')

with open('test_file.txt', 'rb') as f:
    content = f.read()

encoding = detect(content)['encoding']

with open('test_file.txt', encoding=encoding) as fr:
    for word in fr:
        print(word.rstrip())


