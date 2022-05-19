import select
import sys
import argparse
import socket
import json
import logging
import time

import logs.server_log_config
from log_decorator import log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT
from common.utils import get_message, send_message

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


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
    transport.settimeout(0.8)
    transport.listen(MAX_CONNECTIONS)
    SERVER_LOGGER.info(f'Сервер запущен с параметрами: {listen_address}:{listen_port}')

    clients = []
    messages = []

    while True:
        try:
            client, client_address = transport.accept()
            SERVER_LOGGER.info(f'Установлено соединение с {client_address}')
            clients.append(client)
        except OSError as err:
            print(err.errno)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)

        # try:
        #     message_from_client = get_message(client)
        #     SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
        #     response = process_client_message(message_from_client)
        #     send_message(client, response)
        #     SERVER_LOGGER.info(f'Отправлено сообщение клиенту {response}')
        #     client.close()
        #     SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрыто.')
        # except (ValueError, json.JSONDecodeError):
        #     SERVER_LOGGER.error(f'Ошибка декодирования JSON пакета от {client_address}. Соединение закрыто.')
        #     client.close()


if __name__ == '__main__':
    main()
