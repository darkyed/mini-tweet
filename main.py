from screens import Interaction as interact
from User import User
from manageDB import sqliteDB

db = sqliteDB()

db.create_table()

interact.welcome()
