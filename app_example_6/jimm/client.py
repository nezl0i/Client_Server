import sys
import json
import socket
import time
import argparse
import logging
from log_decorator import log
import logs.client_log_config
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message

CLIENT_LOGGER = logging.getLogger('client')


@log
def check_port(port):
    if port not in range(1024, 65536):
        CLIENT_LOGGER.critical(f'Ошибка запуска с портом {port}. Допустимый диапазон портов от 1024 до 65535.')
        sys.exit(1)
    return port


@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_ans(message):
    CLIENT_LOGGER.debug(f'Обработка сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


@log
def create_parser():
    parser = argparse.ArgumentParser(description="JIM Client_server application")
    parser.add_argument("ip", nargs='?', default=DEFAULT_IP_ADDRESS, help='Server IP')
    parser.add_argument("port", nargs='?', default=DEFAULT_PORT, type=int, help='Server port')
    return parser


def main():

    args = create_parser().parse_args()
    server_port = check_port(args.port)
    server_address = args.ip
    CLIENT_LOGGER.info(f'Клиент запущен с параметрами: {server_address}:{server_port}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        CLIENT_LOGGER.info(f'Отправлен запрос на сервер {message_to_server}')
        answer = process_ans(get_message(transport))
        transport.close()
        CLIENT_LOGGER.info(f'Получен ответ от сервера {answer}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOGGER.error(f'Ошибка декодирования JSON пакета от {server_address}.')


if __name__ == '__main__':
    main()
