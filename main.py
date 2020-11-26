from screens import Interaction as interact
from User import User
from manageDB import sqliteDB

db = sqliteDB()

tables = ["users", "tweets", "follows", "hashtags"]

for table in tables:
    db.create_table(table_name=table)

interact.welcome()
