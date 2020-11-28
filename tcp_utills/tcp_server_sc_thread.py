import os
import sys
import socket
import logging
from threading import Thread, active_count
from manageDB import *
from screens import Interaction as interact, Authenticate as auth


# from utilfuncs import *

default_buffer = 32768

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


class ThreadServer(object):
    def __init__(self, host="", port=12345, protocol="TCP") -> None:
        print("Server up and running. . .")
        self.host = host
        self.port = port
        self.protocol = protocol
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.threads = []
        self.dbname = "twitter.db"
        self.sqldb = sqliteDB(self.dbname)

    def sendData(self, conn_sock, data: str):
        try:
            conn_sock.send(data.encode('utf-8'))
        except socket.error as e:
            print("Error sending data: %s" % e)
            sys.exit(1)

    def recvData(self, conn_sock, size=default_buffer):
        try:
            data = conn_sock.recv(size)
        except socket.error as e:
            print("Error receiving data: %s" % e)
            sys.exit(1)

        return data.decode('utf-8')

    def listen(self):
        # The 5 is the backlog argument which specifies how many connections
        # can be queued up waiting to be accepted
        self.server_socket.listen(10)
        while True:
            connection_socket, client_address = self.server_socket.accept()
            connection_socket.settimeout(30)

            # listen to the incoming clients
            logging.debug("starting listen")
            self.listenToClient(connection_socket, client_address)

    def login_client(self, conn_sock):
        received_data = self.recvData(conn_sock)
        handle, password = received_data.split("ψ")
        user = auth.logInUser(self.sqldb, handle, password)
        if user:
            self.sendData('y')
            self.sendData(user.name)

            loggedIn_option = self.recvData()
            self.main_page(conn_sock, user, loggedIn_option)

        else:
            self.sendData('n')
            self.login_client(conn_sock)

    # TODO
    def register_client(self, conn_sock):
        handle = self.recvData(conn_sock)
        if self.sqldb.user_exists(handle) == False:
            name, password = self.recvData(conn_sock)
            user = User(name, handle)
            self.sqldb.add_user(user, password)
            self.sendData('y')
        else:
            #User already exists
            self.sendData('n')
            self.register_client(conn_sock)
            


    def send_tweets(self, conn_sock, user, tweets):
        for tweet in tweets:
            tweet = "%s tweeted %s" % (tweet[2], tweet[1])
            self.sendData(conn_sock, tweet)


    def main_page(self, conn_sock, user, option):

        if option == '1':
            self.sendData(conn_sock, 'y')
            text = self.recvData()
            self.sqldb.add_tweet(user, text)
            # TODO to send ack

        elif option == '2':
            self.sendData(conn_sock, 'y')  # send 'y'
            handle = self.recvData(conn_sock)
            exist = self.sqldb.user_exists(handle)

            if exist:
                self.sendData(conn_sock, 'y')  # send 'y' for exist
                option_search = self.recvData(conn_sock)
                res = ""
                if option_search == '1':
                    res = interact.follow_someone(user, handle, self.sqldb)
                    self.sendData(conn_sock, res)

                elif option_search == '2':
                    res = interact.unfollow_someone(user, handle, self.sqldb)
                    self.sendData(conn_sock, res)

                elif option_search == '3':
                    tweets = self.sqldb.get_tweets(handle)
                    for tweet in tweets:
                        tweet = "%s tweeted %s" % (tweet[2], tweet[1])
                        self.sendData(conn_sock, tweet)

            else:
                self.sendData(conn_sock, 'n')  # send 'y' for exist

        elif option == '3':
            # get updates
            tweets = interact.get_feed(user, self.sqldb)
            self.send_tweets(conn_sock, user, tweets)

        elif option in ['4', '5']:
            handle = self.recvData(conn_sock)
            if option == '4':
                res = interact.follow_someone(user, handle, self.sqldb)
            else:
                res = interact.unfollow_someone(user, handle, self.sqldb)

            if 'No' in res:
                self.sendData('n')
            else:
                self.sendData(conn_sock, res)

        elif option == '6':
            # TODO incomplete --- not implemented in Interacttion
            hashtag = input("Enter handle: ")
            self.sendData()

            r = self.recvData()

            print(r)

        elif option == '7':
            hashtag = self.recvData(conn_sock)
            tweets = interact.getTweetsViaHashtag(user, hashtag, self.sqldb)
            if tweets:
                self.send_tweets(conn_sock, user, tweets)
            else:
                message = "No tweets exists with hashatg: %s" % (hashtag)
                self.sendData(conn_sock, message)

        elif option == '8':
            conn_sock.close()
            return

        option = self.recvData()
        self.main_page(option)

    def listenToClient(self, connection_socket, client_address):
        size = default_buffer
        while True:
            try:
                # 1 or 2
                data = self.recvData(connection_socket)
                if data == '1':
                    self.login_client(connection_socket)
                elif data == '2':
                    self.register_client(connection_socket)

                # TODO where to do threading?
                # if data:
                #     file_name = data.decode('utf-8')

                #     # The following thread will heandle the data transfer

                #     t = Thread(target=self.sendFile, args=(connection_socket, client_address, file_name))

                #     t.start()
                #     self.threads.append(t)

                # else:
                #     raise Exception('Client disconnected')
            except:
                connection_socket.close()
                return False


if __name__ == "__main__":
    T = ThreadServer()
    T.listen()
