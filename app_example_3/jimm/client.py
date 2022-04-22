import sys
import json
import socket
import time
import argparse
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message


def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    parser = argparse.ArgumentParser(description="JIM Client_server application")

    parser.add_argument("ip", nargs='?', default=DEFAULT_IP_ADDRESS, help='Server IP')
    parser.add_argument("port", nargs='?', default=DEFAULT_PORT, type=int, help='Server port')

    args = parser.parse_args()

    try:
        server_port = args.port
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    server_address = args.ip

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_ans(get_message(transport))
        print(answer)
    except ConnectionRefusedError:
        print('Сервер не запущен.')
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
