from tcp_utills.tcp_client import TCPClient
from UtilFuncs.manageDB import *
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

from random_words import RandomWords
import random
from names import get_first_name
random.seed(42)
rw=RandomWords()
words=rw.random_words(count=32)

tables = ["users", "tweets", "hashtags", "follows"]
s = sqliteDB()
for t in tables:
    s.create_table(t)
random.seed(42)

s.close_connection()
names=[get_first_name() for i in range(32)]

for i in range(32):
    c=TCPClient()
    c.start_connection()
    handle=names[i]
    c.register_user(handle,handle,handle)
    c.tweet(words[i]+" #"+words[(i+1)%32])
    for j in range(i):
        c.follow(names[j])
    

# c1 = TCPClient()
# c2= TCPClient()

# c1.start_connection()
# c2.start_connection()

# # cl.welcome_screen()
# handle="rushil"
# name="rush"
# password="r"
# c1.register_user(handle,name,password)

# handle="saumitra"
# name="saum"
# password="s"
# c2.register_user(handle,name,password)

# c1.tweet("peeyush #great")
# c2.tweet("peeyush #good")

# c1.follow("saumitra")
# logging.debug("Rushil's feed")
# c1.feed()
# logging.debug("Saumitra's feed")
# c2.feed()
# c2.follow("rushil")
# logging.debug("Saumitra's feed")
# c2.feed()
# c2.unfollow("rushil")
# logging.debug("Saumitra's feed")
# c2.feed()
# logging.debug("#great tweets")
# c1.searchviahshtag("great")
# logging.debug("#good tweets")
# c1.searchviahshtag("good")






