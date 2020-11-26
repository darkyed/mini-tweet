import sqlite3 as sql
from User import User


# User: 
#     primary key ---> unique handle
#     name
#     password

# Tweets:
#     tweet_id: (unique) primary key
#     by: handle(foreign-key)
#     tweet_text: 

# Follows:
#     A(follower): handle
#     B(following): handle

# Hashtags:
#     tweet_id: id ----> correspoding hashtag
    




class sqliteDB:
    def __init__(self, dbName='twitter.db') -> None:
        self.db = dbName
        self.conn = sql.connect(dbName)
        self.cur = self.conn.cursor()
    
    def create_table(self, table_name="users"):
        if table_name=="users":
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    name text,
                    handle text,
                    password text)
                """)
        
        if table_name=="tweets":
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    tweet_id text,
                    tweet_text text,
                    author text)
                """)
        
        self.commit_changes()
    
    def user_exists(self, handle):
        select_command = "SELECT handle FROM users WHERE handle=?"
        t = (handle,)
        self.cur.execute(select_command,t)
        if self.cur.fetchone():
            return True
        
        return False
    
    def add_user(self, user:User, password):
        h = user.handle

        insert_command = "INSERT INTO users VALUES (?, ?, ?)"
            
        self.cur.execute(insert_command,(user.name, user.handle, password))
        self.commit_changes()

        
    
    def commit_changes(self):
        self.conn.commit()
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()
    
    