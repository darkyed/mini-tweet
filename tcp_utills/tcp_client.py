import sys
import os
sys.path.append(os.getcwd())
from UtilFuncs.screens import Interaction as interact, Authenticate as auth
from socket import *
from UtilFuncs.User import User
import logging
import time
import os


class TCPClient:
    def __init__(self, protocol="TCP", server_address="127.0.0.1", port=12345) -> None:
        self.protocol = protocol
        self.server_address = server_address
        self.port = port
        self.client_socket = None
        self.user = None

    def start_connection(self):

        logging.debug("trying to connect")

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        # establish the connection // 3-way handshake
        self.client_socket.connect((self.server_address, self.port))

        logging.debug("connected!")

    def welcome_screen(self):
        option = interact.welcome()
        self.sendData(str(option))
        if option == 1:
            self.login_user()
        if option == 2:
            self.register_user()

    def sendData(self, data: str):
        try:
            data = data.encode("UTF-8")
            self.client_socket.send(len(data).to_bytes(7, 'big'))
            self.client_socket.send(data)
        except error as e:
            print("Error sending data: %s" % e)
            sys.exit(1)

    def recvData(self, size=32768):
        """
        Receive data of size 'size' from the server using socket 'sock'
        """
        try:
            data_size = self.client_socket.recv(7)
            data_size = int.from_bytes(data_size, 'big')
            data = self.client_socket.recv(data_size)
        except error as e:
            print("Error receiving data: %s" % e)
            sys.exit(1)

        return data.decode('utf-8')

    def register_user(self):
        handle = interact.getInputHandle()
        # print(handle)
        self.sendData(handle)
        message = self.recvData()
        if message == 'n':
            time.sleep(1)
            print("User handle already exists! Please try with a new handle")
            self.register_user()
        else:
            name, password = interact.registerScreen()
            self.user = User(name, handle)
            self.sendData(name + "\r" + password)
            print("Sent")

            ack = self.recvData()

            if ack == 'y':
                print("You are registered!")
                option = auth.redirectToHomeScreen(handle)
                option = str(option)
                print("you chose:", option)
                self.main_page(option)

            # FIXME else

    def login_user(self):
        # username
        handle, password = interact.logInScreen()

        self.sendData(handle + "\r" + password)
        # y n
        received_data = self.recvData(1)

        if received_data == 'y':
            # log them in
            print("---Logged In---")
            name = self.recvData()
            self.user = User(name, handle)
            option = auth.redirectToHomeScreen(handle)
            option = str(option)
            self.main_page(option)

        else:
            print("\nSorry wrong credentials, try again!")
            time.sleep(1)
            self.login_user()

    def main_page(self, option: str):
        # 1
        print(option)
        self.sendData(option)

        if option == '1':
            received_data = self.recvData()
            if received_data == 'y':
                text = interact.tweet()
                self.sendData(text)

                # TODO acked by server
                time.sleep(1)
                print("Post was added. . .")

        elif option == '2':
            received_data = self.recvData()
            
            if received_data == 'y':
                while True:
                    res = self.recvData()
                    if res == '\r': 
                        break
                    if res != self.user.handle:
                        print(res)
                
                handle = interact.search_user()
                self.sendData(handle)
                exist = self.recvData()

                # found user
                if exist == 'y':
                    option_search = interact.searchscreen(handle)
                    self.sendData(option_search)

                    r = self.recvData()

                    # 1 -> follow
                    # 2 -> unfollow
                    # 3 -> tweets
                    while r and (r != "\r"):
                        print(r)
                        r = self.recvData()

                else:
                    print("User not found!")
                    # Recurse
                    self.main_page(option)

        elif option == '3':
            # get updates
            r = self.recvData()
            while r and (r != "\r"):
                print(r)
                r = self.recvData()

        elif option in ['4', '5']:
            handle = input("Enter the handle of user: ")
            self.sendData(handle)

            # get updates
            r = self.recvData()
            if r == 'n':
                print("No such user exists, try again!")
                self.main_page(option)
            else:
                print(r)

        elif option == '6':
            # TODO incomplete --- not implemented in Interacttion
            hashtag = input("Enter handle: ")
            self.sendData()

            r = self.recvData()

            print(r)

        elif option == '7':
            hashtag = input("Enter hashtag: #")
            self.sendData(hashtag)
            r = self.recvData()
            while r and (r != "\r"):
                print(r)
                r = self.recvData()

        elif option == '8':
            print("\nLOGGED OUT--------")
            self.client_socket.close()
            return

        option = auth.redirectToHomeScreen(self.user.handle)
        self.main_page(option)
