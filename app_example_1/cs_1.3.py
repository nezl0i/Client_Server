"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""

EXAMPLE = ['attribute', 'класс', 'функция', 'type']


def to_bytes(args):
    for word in args:
        tmp = "b'" + word + "'"
        try:
            print(eval(tmp))
        except SyntaxError:
            print(f'Слово {word} невозможно представить в байтовом типе.')


to_bytes(EXAMPLE)
