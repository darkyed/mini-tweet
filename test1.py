from User import User
from manageDB import sqliteDB

s = sqliteDB()

s.create_table()
s.create_table("tweets")

tweets = ["assadfa", "dgsdgsdg", "dagsdgsdg"]
authors_handles = ["fds", "das", "hre"]
author_names = ['A', 'B', 'C']
passwords = ['123']*3

users = []

for h,n,p in zip(authors_handles, author_names,passwords):
    u = User(n,h)
    users.append(u)
    s.add_user(u,p)

for u,t in zip(users,tweets):
    s.add_tweet(u,t)

command = "select * from tweets"
s.cur.execute(command)

res = s.cur.fetchall()
for r in res:
    print(r)