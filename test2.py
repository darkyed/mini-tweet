from tcp_utills.tcp_client import TCPClient
from UtilFuncs.manageDB import *

tables = ["users", "tweets", "hashtags", "follows"]
s = sqliteDB()
for t in tables:
    s.create_table(t)

s.close_connection()

cl = TCPClient()

cl.start_connection()

cl.welcome_screen()