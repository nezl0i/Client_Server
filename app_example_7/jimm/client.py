import sys
import json
import socket
import time
import argparse
import logging
from log_decorator import log
import logs.client_log_config
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT
from common.utils import get_message, send_message

CLIENT_LOGGER = logging.getLogger('client')


@log
def check_port(port):
    if port not in range(1024, 65536):
        CLIENT_LOGGER.critical(f'Ошибка запуска с портом {port}. Допустимый диапазон портов от 1024 до 65535.')
        sys.exit(1)
    return port


@log
def check_mode(mode):
    if mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {mode}, '
                               f'допустимые режимы: listen , send')
        sys.exit(1)
    return mode


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
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение для отправки. (\'q\' для завершения работы): ')
    if message == 'q':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        sys.exit()
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение: {message_dict}')
    return message_dict


@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')


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
    parser.add_argument('-s', '--ip', nargs='?', default=DEFAULT_IP_ADDRESS, help='Server IP')
    parser.add_argument('-p', '--port',  nargs='?', default=DEFAULT_PORT, type=int, help='Server port')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    return parser


def main():

    args = create_parser().parse_args()
    server_port = check_port(args.port)
    server_address = args.ip
    client_mode = check_mode(args.mode)
    CLIENT_LOGGER.info(f'Клиент запущен с параметрами: {server_address}:{server_port} режим {client_mode}')

    try:

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOGGER.error(f'Ошибка декодирования JSON пакета от {server_address}.')
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            try:
                if client_mode == 'send':
                    send_message(transport, create_message(transport))
                if client_mode == 'listen':
                    message_from_server(get_message(transport))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f'Соединение с сервером {server_address} потеряно.')
                sys.exit(1)


if __name__ == '__main__':
    main()
