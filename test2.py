from tcp_utills.tcp_client import TCPClient
from UtilFuncs.manageDB import *

tables = ["users", "tweets", "hashtags", "follows"]
s = sqliteDB()
for t in tables:
    s.create_table(t)
c2= TCPClient()
c2.start_connection()
handle="saumitra"
name="saum"
password="s"
c2.register_user(handle,name,password)
