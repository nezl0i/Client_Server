import argparse
import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


def process_client_message(message):

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def check_port(port):
    try:
        tmp_port = port
        if tmp_port < 1024 or tmp_port > 65535:
            raise ValueError
        return tmp_port
    except ValueError:
        print('Номер порта должен быть в диапазоне от 1024 до 65535.')
        # sys.exit(1)


def main():

    parser = argparse.ArgumentParser(description="JIM Client_server application")

    parser.add_argument('-a', dest='address', nargs='?', default='', help='IP address')
    parser.add_argument('-p', dest='port',  nargs='?', default=DEFAULT_PORT, type=int, help='Server port')

    args = parser.parse_args()

    listen_port = check_port(args.port)
    listen_address = args.address

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
