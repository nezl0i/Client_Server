import sys
import argparse
import socket
import json
import logging
import logs.server_log_config
from log_decorator import log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message):
    SERVER_LOGGER.debug(f'Сообщение от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

@log
def check_port(port):
    if port not in range(1024, 65536):
        SERVER_LOGGER.critical(f'Ошибка запуска сервера с портом {port}. Допустимый диапазон портов от 1024 до 65535.')
        sys.exit(1)
    return port


def main():
    parser = argparse.ArgumentParser(description="JIM Client_server application")

    parser.add_argument('-a', dest='address', nargs='?', default='127.0.0.1', help='IP address')
    parser.add_argument('-p', dest='port', nargs='?', default=DEFAULT_PORT, type=int, help='Server port')

    args = parser.parse_args()

    listen_port = check_port(args.port)
    listen_address = args.address

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)
    SERVER_LOGGER.info(f'Сервер запущен с параметрами: {listen_address}:{listen_port}')

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с {client_address}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            response = process_client_message(message_from_client)
            send_message(client, response)
            SERVER_LOGGER.info(f'Отправлено сообщение клиенту {response}')
            client.close()
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрыто.')
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.error(f'Ошибка декодирования JSON пакета от {client_address}. Соединение закрыто.')
            client.close()


if __name__ == '__main__':
    main()
