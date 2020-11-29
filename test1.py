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
c2= TCPClient()

c1.start_connection()
c2.start_connection()

# cl.welcome_screen()
handle="rushil"
name="rush"
password="r"
c1.register_user(handle,name,password)

handle="saumitra"
name="saum"
password="s"
c2.register_user(handle,name,password)

c1.tweet("peeyush #great")
c2.tweet("peeyush #good")

c1.follow("saumitra")
logging.debug("Rushil's feed")
c1.feed()
logging.debug("Saumitra's feed")
c2.feed()
c2.follow("rushil")
logging.debug("Saumitra's feed")
c2.feed()
c2.unfollow("rushil")
logging.debug("Saumitra's feed")
c2.feed()
logging.debug("#great tweets")
c1.searchviahshtag("great")
logging.debug("#good tweets")
c1.searchviahshtag("good")






