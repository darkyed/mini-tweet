from tcp_utills.tcp_client import TCPClient
from UtilFuncs.manageDB import *
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

tables = ["users", "tweets", "hashtags", "follows"]
s = sqliteDB()
for t in tables:
    s.create_table(t)

s.close_connection()

c1 = TCPClient()

c1.start_connection()
c1.login_user("James","James")
c1.getallfollowers()
