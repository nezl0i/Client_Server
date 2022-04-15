"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""

EXAMPLE = ['разработка', 'администрирование', 'protocol', 'standard']


def encode_decode(lst):
    for word in lst:
        _bytes = word.encode('ascii', 'replace')
        print(_bytes)
        print(_bytes.decode('ascii'))


encode_decode(EXAMPLE)
