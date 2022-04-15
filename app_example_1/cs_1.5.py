"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице.
"""

import subprocess
import platform
import locale

default_encoding = locale.getpreferredencoding()


def ping_host(host, count):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, str(count), host]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        line = line.decode(default_encoding).encode('utf-8')
        print(line.decode('utf-8').rstrip())


ping_host('yandex.ru', 4)
ping_host('youtube.com', 4)
