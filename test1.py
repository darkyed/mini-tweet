from tcp_utills.tcp_client import TCPClient
from UtilFuncs.manageDB import *

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

c1.tweet("peeyush #lodu")
c2.tweet("peeyush #bhadwa")

c1.follow(c2)
c1.feed()
c2.feed()
c2.follow(c1)
c2.feed()










# tweets = ["assadfa ", "peeyush #lodu", "dagsdgsdg"]
# authors_handles = ["peeyu", "saumitra", "rushil"]
# author_names = ['A', 'B', 'C']
# passwords = ['123']*3

# users = []

# for h,n,p in zip(authors_handles, author_names,passwords):
#     u = User(n,h)
#     users.append(u)
#     s.add_user(u,p)

# for u,t in zip(users,tweets):
#     s.add_tweet(u,t)

# s.add_follow(users[0],users[1])
# print("Following List: of %s"%(users[0].handle),s.get_following_list(users[0]))
# print("feed of %s: "%(users[0].handle))
# Interaction.get_feed(users[0],s)
# print("tweets with hashtag #%s"%("lodu"))
# Interaction.getTweetsViaHashtag("lodu",s)
# s.delete_follow(users[0],users[1])
# print("Following List: of %s"%(users[0].handle),s.get_following_list(users[0]))
# print("feed of %s: "%(users[0].handle))
# Interaction.get_feed(users[0],s)
# # command = "select * from tweets"
# # s.cur.execute(command)

# # res = s.cur.fetchall()
# # for r in res:
# #     print(r)