from User import User
from manageDB import sqliteDB
from screens import Interaction
s = sqliteDB()

s.create_table()

s.create_table("tweets")
s.create_table("follows")
s.create_table("hashtags")

tweets = ["assadfa ", "peeyush #lodu", "dagsdgsdg"]
authors_handles = ["peeyu", "saumitra", "rushil"]
author_names = ['A', 'B', 'C']
passwords = ['123']*3

users = []

for h,n,p in zip(authors_handles, author_names,passwords):
    u = User(n,h)
    users.append(u)
    s.add_user(u,p)

for u,t in zip(users,tweets):
    s.add_tweet(u,t)

s.add_follow(users[0],users[1])
print("Following List: ",s.get_following_list(users[0]),users[1].handle)
print("tweets: ")
Interaction.get_feed(users[0],s)
Interaction.getTweetsViaHashtag("lodu",s)
s.delete_follow(users[0],users[1])
print(s.get_following_list(users[0]),users[1].handle)
Interaction.get_feed(users[0],s)
# command = "select * from tweets"
# s.cur.execute(command)

# res = s.cur.fetchall()
# for r in res:
#     print(r)