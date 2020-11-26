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
#     A(follower): handle : both foreign-key
#     B(following): handle : both foreign-key

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
                    handle text PRIMARY KEY,
                    password text)
                """)
        
        if table_name=="tweets":
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    tweet_id integer PRIMARY KEY AUTOINCREMENT,
                    tweet_text text,
                    author text,
                    FOREIGN KEY(author) REFERENCES users(handle))
                """)

        if table_name=="follows":
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS follows (
                    follower text,
                    gawd text,
                    FOREIGN KEY(follower) REFERENCES users(handle),
                    FOREIGN KEY(gawd) REFERENCES users(handle))
                """)
        
        if table_name=="hashtags":
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS hashtags (
                    tag text,
                    t_id integer,
                    FOREIGN KEY(t_id) REFERENCES tweets(tweet_id))
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
    
    def get_following_list(self,user):
        self.cur.execute("SELECT gawd FROM follows where follower=?", (user.handle,))
        return self.cur.fetchall()
    
    def get_tweets(self,handle):
        select_command = "SELECT * FROM tweets WHERE author=?"
        t = (handle,)
        self.cur.execute(select_command,t)
        return  self.cur.fetchall()
    
    def delete_follow(self,user:User, following:User):
        self.cur.execute("DELETE FROM follows where gawd=? and follower=?", (following.handle, user.handle,))
        self.commit_changes()
        
    def add_follow(self,user:User, following:User):
        if not self.following_exists(user,following):
            self.cur.execute("INSERT into follows VALUES (?, ?)", (user.handle,following.handle,))    
            self.commit_changes()
        else:
            print("Already following")
    
    def following_exists(self,user:User,following:User):
        handle=user.handle
        following_handle=following.handle
        select_command = "SELECT * FROM follows WHERE gawd=? and follower=?"
        t = (following_handle,handle,)
        self.cur.execute(select_command,t)
        if self.cur.fetchone():
            return True
        
        return False


    def add_tweet(self, user:User, tweet_text):

        insert_command = "INSERT INTO tweets (tweet_text, author) VALUES (?, ?)"
            
        self.cur.execute(insert_command,(tweet_text, user.handle))
        self.commit_changes()
    
        
    
    def commit_changes(self):
        self.conn.commit()
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()
    
    