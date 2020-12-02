import os
import sys
sys.path.append(os.getcwd())
from UtilFuncs.screens import Interaction as interact, Authenticate as auth
from UtilFuncs.manageDB import *
from threading import Thread, active_count
import logging
import socket


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
            data = data.encode("UTF-8")
            conn_sock.send(len(data).to_bytes(7, 'big'))
            conn_sock.send(data)
        except socket.error as e:
            logging.warning("Error sending data: %s" % e)
            sys.exit(1)

    def recvData(self, conn_sock, size=default_buffer):

        try:
            data_size = conn_sock.recv(7)
            data_size = int.from_bytes(data_size, 'big')
            data = conn_sock.recv(size)
        except socket.error as e:
            logging.warning("Error receiving data: %s" % e)
            sys.exit(1)

        return data.decode('utf-8')

    def listen(self):
        # The 5 is the backlog argument which specifies how many connections
        # can be queued up waiting to be accepted
        self.server_socket.listen(10)
        while True:
            connection_socket, client_address = self.server_socket.accept()
            connection_socket.settimeout(60)

            # listen to the incoming clients
            logging.debug("starting listen")
            # self.listenToClient(connection_socket, client_address)
            t = Thread(target=self.listenToClient, args=(connection_socket, client_address))

            t.start()
            self.threads.append(t)

    def login_client(self, conn_sock):
        received_data = self.recvData(conn_sock)
        handle, password = received_data.split("\r")
        user = auth.logInUser(self.sqldb, handle, password)
        if user:
            self.sendData(conn_sock, 'y')
            self.sendData(conn_sock, user.name)

            loggedIn_option = self.recvData(conn_sock)
            self.main_page(conn_sock, user, loggedIn_option)

        else:
            self.sendData(conn_sock, 'n')
            self.login_client(conn_sock)

    def register_client(self, conn_sock):
        handle = self.recvData(conn_sock)
        logging.debug("Received registration: "+handle)
        user_in_db = self.sqldb.user_exists(handle)

        if not user_in_db:
            logging.debug("unique user found")
            self.sendData(conn_sock, 'y')

            namepass = self.recvData(conn_sock)
            logging.debug("got name and password")

            name, password = namepass.split('\r')
            user = User(name, handle)

            self.sqldb.add_user(user, password)

            self.sendData(conn_sock, 'y')

            logging.debug("Registered new user: %s" % user.handle)
            register_option = self.recvData(conn_sock)
            logging.debug("got register option: " + register_option)
            self.main_page(conn_sock, user, register_option)

        else:
            # User already exists
            logging.debug("Already exists")
            self.sendData(conn_sock, 'n')
            logging.debug("set ack: n")
            self.register_client(conn_sock)

    def send_tweets(self, conn_sock, user, tweets):
        for tweet in tweets:
            tweet = "%s tweeted %s" % (tweet[2], tweet[1])
            self.sendData(conn_sock, tweet)
    
    def send_followers(self, conn_sock, user, follower_lis):
        for f in follower_lis:
            # tweet = "%s tweeted %s" % (tweet[2], tweet[1])
            self.sendData(conn_sock, f[0])

    def main_page(self, conn_sock, user: User, option):

        if option == '1':

            self.sendData(conn_sock, 'y')
            logging.debug('sent ack')

            text = self.recvData(conn_sock)
            logging.debug("received tweet")

            self.sqldb.add_tweet(user, text)

            logging.debug("New Tweet by %s: %s. . ." %
                          (user.handle, text[:20]))
            # TODO to send ack

        elif option == '2':
            self.sendData(conn_sock, 'y')  # send 'y'
            
            res = self.sqldb.getAllHandles()
            for i in res:
                self.sendData(conn_sock, i[0])
            self.sendData(conn_sock, "\r")
            # print()
            handle = self.recvData(conn_sock)
            logging.debug("searching for user")
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
                    self.send_tweets(conn_sock, user, tweets)

                self.sendData(conn_sock, "\r")

            else:
                self.sendData(conn_sock, 'n')  # send 'y' for exist

        elif option == '3':
            # get updates
            tweets = interact.get_feed(user, self.sqldb)
            logging.debug("fetched tweets")

            self.send_tweets(conn_sock, user, tweets)
            self.sendData(conn_sock, "\r")

        elif option in ['4', '5']:
            handle = self.recvData(conn_sock)
            if option == '4':
                res = interact.follow_someone(user, handle, self.sqldb)
            else:
                res = interact.unfollow_someone(user, handle, self.sqldb)

            if 'No' in res:
                self.sendData(conn_sock, 'n')
            else:
                self.sendData(conn_sock, res)

        elif option == '6':
            # TODO incomplete --- not implemented in Interacttion
            # handle = self.recvData(conn_sock)
            follower_list=self.sqldb.show_followers(user)
            print(follower_list)
            self.send_followers(conn_sock,user,follower_list)
            # print("Follower list")
            # for name in follower_list:
            #     print(name)
            self.sendData(conn_sock,'\r')    
            # res = interact.delete_follower(user, handle, self.sqldb)

            # if 'No' in res:
            #     self.sendData(conn_sock, 'n')
            # else:
            #     self.sendData(conn_sock, res)

        elif option == '7':
            hashtag = self.recvData(conn_sock)
            logging.debug("got: #%s" % hashtag)

            tweets = interact.getTweetsViaHashtag(user, hashtag, self.sqldb)

            if tweets:
                self.send_tweets(conn_sock, user, tweets)
            else:
                message = "No tweets exists with hashatg: %s" % (hashtag)
                self.sendData(conn_sock, message)

            self.sendData(conn_sock, "\r")

        elif option == '8':
            conn_sock.close()
            return

        logging.debug("out of conditions")
        option = self.recvData(conn_sock)
        logging.debug("option")
        self.main_page(conn_sock, user, option)

    def listenToClient(self, connection_socket, client_address):
        size = default_buffer
        while True:
            try:
                # 1 or 2
                data = self.recvData(connection_socket)
                if data == '1':
                    logging.debug("going to login")
                    self.login_client(connection_socket)
                elif data == '2':
                    logging.debug("going to register")
                    self.register_client(connection_socket)

            except:
                connection_socket.close()
                return False


if __name__ == "__main__":
    T = ThreadServer()
    T.listen()
