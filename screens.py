from User import User
from manageDB import sqliteDB


class Interaction:

    @staticmethod
    def welcome():
        print("New user: 1. Log In")
        print("Existing user: 2. Sign Up/ Register")
        Interaction.welcome_input()

    @staticmethod
    def welcome_input():
        option = int(input("Choose (1) or (2): "))
        if option == 1:
            Interaction.logInScreen()
        if option == 2:
            Interaction.registerScreen()

    @staticmethod
    def loggedInOptions(user, sqldb):
        print(
            """
            1. Tweet
            2. Find someone via handle
            3. Get Updates
            4. Follow users via handle
            5. Unfollow users via handle
            6. Delete a follower via handle
            7. Search tweets using hashtag
            8. LOG-OUT
            """
        )

        option = 0
        try:
            option = int(input("Choose from [1-8]: "))
        except:
            print("Invalid choice")
            Interaction.loggedInOptions(user, sqldb)
        if not (0 < option < 9):
            print("Invalid choice")
            Interaction.loggedInOptions(user, sqldb)
        else:
            Authenticate.loggedInChoice(user, option, sqldb)

    @staticmethod
    def logInScreen():
        print("\nLOGIN SCREEN---------")
        handle = input("Enter your handle: ")
        password = input("Enter your password: ")
        Authenticate.logInUser(handle, password)

    @staticmethod
    def registerScreen():
        print("\nREGISTRATION SCREEN---------")
        name = input("Enter just your first name: ")
        handle = input("Enter your handle: ")
        s = sqliteDB()
        while s.user_exists(handle):
            print("\nThat handle isn't available, try again!")
            handle = input("Enter your handle: ")

        password = input("Enter your password: ")
        user = User(name, handle)
        Authenticate.registerUser(user, password)
    
    @staticmethod
    def searchscreen(handle,user,s):
        print("\nSearch SCREEN---------")
        print("We found "+ handle)

        number = int(input(
            """
            1. Follow handle
            2. Unfollow handle
            3. Get handle's tweets
            """
        ))

        if number==1:
            Interaction.follow_someone(user,handle,s)
        elif number==2:
            Interaction.follow_someone(user,handle,s)
        elif number==3:
            Interaction.print_tweets(s.get_tweets(handle))
        else:
            print("invalid option")
            Interaction.searchscreen(handle,user,s)

    @staticmethod
    def print_tweets(tweet_list):
        for tweet in tweet_list:
            # print(tweet)
            print("%s tweeted %s" % (tweet[2],tweet[1]))

    @staticmethod
    def tweet(user: User, s: sqliteDB):
        print("\nYou chose to tweet!-----")
        text = input("Enter your text: ")
        s.add_tweet(user, text)
        print("Posted your tweet to timeline: %s. . ." % text[:20])
        # Interaction.loggedInOptions(user, s)

    @staticmethod
    def get_feed(user, s, top_tweets=10):
        tweet_list = s.get_all_tweets_of_following(user.handle)
        print_tweets(tweet_list)
        # for tweet in tweet_list:
        #     # print(tweet)
        #     print("%s tweeted %s" % (tweet[2],tweet[1]))
        # Interaction.loggedInOptions(user, s)

    @staticmethod
    def follow_someone(user,follow_handle, s):
        
        if s.user_exists(follow_handle):
            if not s.following_exists(user, follow_handle):
                s.add_follow(user, follow_handle)
                print("\nYou are now following: %s" % follow_handle)
            else:
                print("\nYou already follow him/her")
                
        else:
            print("\nNo such user exists")
        # Interaction.loggedInOptions(user, s)

    @staticmethod
    def unfollow_someone(user,follow_handle, s):
        # follow_handle=input("Who do you want to unfollow: ")

        if s.user_exists(follow_handle):
            if s.following_exists(user, follow_handle):
                s.delete_follow(user, follow_handle)
                print("Deleted follower")
            else:
                print("You don't follow him/her")
        else:
            print("No such user exists")
        # Interaction.loggedInOptions(user, s)

    @staticmethod
    def getTweetsViaHashtag(user,s):
        hashtag=input("Type the hashtag to search for the tweets: ")
        command = '''SELECT tweets.author,tweets.tweet_text 
        FROM tweets INNER JOIN hashtags ON tweets.tweet_id=hashtags.t_id AND hashtags.tag=?'''
        s.cur.execute(command, (hashtag,))
        tweets=s.cur.fetchall()
        for tweet in tweets:
            print("%s tweeted %s"%(tweet[0],tweet[1]))
        if not len(tweets):
            print("No tweets exists with hashatg: %s"%(hashtag))
        # Interaction.loggedInOptions(user, s)

    @staticmethod
    def search_user(user,s):
        handle=input("Who do you want to search: ")
        if s.user_exists(handle):
            Interaction.searchscreen(handle,user,s)
        else:
            print("No such user exists")
        
        


class Authenticate:

    @staticmethod
    def registerUser(user, password):
        s = sqliteDB()
        print("Added user:", user)
        try:
            s.add_user(user, password)
            Authenticate.redirectToHomeScreen(user, s)

        except Exception as e:
            print("\n" + e)
            s.close_connection()
            Interaction.registerScreen()

    @staticmethod
    def logInUser(handle, password):
        s = sqliteDB()
        if s.verify_login(handle, password):
            print("---Logged In---")
            user = s.getUserViaHandle(handle)
            user = User(*user)
            Authenticate.redirectToHomeScreen(user, s)
        else:
            print("\nSorry wrong credentials, try again!")
            Interaction.logInScreen()

    @staticmethod
    def loggedInChoice(user, option, s: sqliteDB):
        if option == 8:
            print("\nLOGGED OUT--------")
            s.close_connection()
            return

        elif option == 1:
            Interaction.tweet(user, s)

        elif option == 3:
            Interaction.get_feed(user, s)
        
        elif option ==4:
            follow_handle=input("Who do you want to follow: ")
            Interaction.follow_someone(user,follow_handle,s)

        elif option==5:
            follow_handle=input("Who do you want to unfollow: ")
            Interaction.unfollow_someone(user,follow_handle,s)
        
        elif option==7:
            Interaction.getTweetsViaHashtag(user,s)
        
        elif option==2:
            Interaction.search_user(user,s)

        Interaction.loggedInOptions(user,s)

    @staticmethod
    def redirectToHomeScreen(user, sqldb):
        print("\nHi, %s!" % user.handle)
        print("What would you like to do?")

        Interaction.loggedInOptions(user, sqldb)
