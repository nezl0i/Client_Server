"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом,
а не ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в коем случае не используя методы
encode, decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.
"""

BYTES_EXAMPLE = ['class', 'function', 'method']


def to_bytes(lst):
    for word in lst:
        tmp = "b'" + word + "'"
        print(eval(tmp))
        print(type(eval(tmp)))
        print(len(eval(tmp)))


to_bytes(BYTES_EXAMPLE)
