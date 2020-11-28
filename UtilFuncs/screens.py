from UtilFuncs.User import User
from UtilFuncs.manageDB import sqliteDB


class Interaction:

    @staticmethod
    def welcome():
        print("New user: 1. Log In")
        print("Existing user: 2. Sign Up/ Register")
        # Interaction.welcome_input()

    @staticmethod
    def welcome_input():
        option = int(input("Choose (1) or (2): "))
        return option
        # if option == 1:
        #     Interaction.logInScreen()
        # if option == 2:
        #     Interaction.registerScreen()

    @staticmethod
    def loggedInOptions(handle):
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
            return option
        except:
            print("Invalid choice")
            Interaction.loggedInOptions(handle)
        if not (0 < option < 9):
            print("Invalid choice")
            Interaction.loggedInOptions(handle)
        else:
            Authenticate.loggedInChoice(handle, option)

    @staticmethod
    def logInScreen():
        print("\nLOGIN SCREEN---------")
        handle = input("Enter your handle: ")
        password = input("Enter your password: ")
        return handle, password
        # Authenticate.logInUser(handle, password)

    #TODO - Create method for handle
    @staticmethod
    def getInputHandle():
        print("\nREGISTRATION SCREEN---------")
        handle = input("Enter your handle: ")
        return handle


    @staticmethod
    def registerScreen():
        name = input("Enter just your first name: ")
        password = input("Enter your password: ")
        return name, password
        #Server
        # s = sqliteDB()
        # while s.user_exists(handle):
        #     print("\nThat handle isn't available, try again!")
        #     handle = input("Enter your handle: ")

        # server
        # user = User(name, handle)
        # Authenticate.registerUser(user, password)

    @staticmethod
    def searchscreen(handle):
        print("\nSearch SCREEN---------")
        print("We found " + handle)

        print(
            """
            1. Follow handle
            2. Unfollow handle
            3. Get handle's tweets
            """
        )
        number = int(input("Choose from [1-3]: "))
        return number
        # # server
        # if number == 1:
        #     Interaction.follow_someone(user, handle, s)
        # elif number == 2:
        #     Interaction.unfollow_someone(user, handle, s)
        # elif number == 3:
        #     Interaction.print_tweets(s.get_tweets(handle))
        # else:
        #     print("invalid option")

        # Recurse
        # Interaction.searchscreen(handle, user, s)
        # s.close_connection()

    @staticmethod
    def print_tweets(tweet_list):
        for tweet in tweet_list:
            # print(tweet)
            print("%s tweeted %s" % (tweet[2], tweet[1]))

    @staticmethod
    def tweet(user: User, s: sqliteDB):
        print("\nYou chose to tweet!-----")
        text = input("Enter your text: ")
        return text

        # server part
        # s.add_tweet(user, text)

        # client
        # print("Posted your tweet to timeline: %s. . ." % text[:20])

    # server
    @staticmethod
    def get_feed(user, s, top_tweets=10):
        tweet_list = s.get_all_tweets_of_following(user.handle)
        return tweet_list
        # Interaction.print_tweets(tweet_list)
        # for tweet in tweet_list:
        #     # print(tweet)
        #     print("%s tweeted %s" % (tweet[2],tweet[1]))
        # Interaction.loggedInOptions(user, s)

    # server
    @staticmethod
    def follow_someone(user, follow_handle, s):

        if s.user_exists(follow_handle):
            if not s.following_exists(user, follow_handle):
                s.add_follow(user, follow_handle)
                return "\nYou are now following: %s" % follow_handle
            else:
                return "\nYou already follow him/her"

        else:
            return "\nNo such user exists"
        # Interaction.loggedInOptions(user, s)

    @staticmethod
    def unfollow_someone(user, follow_handle, s: sqliteDB):
        # follow_handle=input("Who do you want to unfollow: ")

        if s.user_exists(follow_handle):
            if s.following_exists(user, follow_handle):
                s.delete_follow(user, follow_handle)
                return "Deleted follower"
            else:
                return "You don't follow him/her"
        else:
            return "No such user exists"
        # Interaction.loggedInOptions(user, s)

    # server
    @staticmethod
    def getTweetsViaHashtag(user, hashtag, s: sqliteDB):
        command = '''SELECT tweets.author,tweets.tweet_text 
        FROM tweets INNER JOIN hashtags ON tweets.tweet_id=hashtags.t_id AND hashtags.tag=?'''
        s.cur.execute(command, (hashtag,))
        tweets = s.cur.fetchall()
        return tweets
        # for tweet in tweets:
        #     print("%s tweeted %s" % (tweet[0], tweet[1]))
        # if not tweets:
        #     return "No tweets exists with hashatg: %s" % (hashtag)
        # else:
        #     return tweets
        # Interaction.loggedInOptions(user, s)

    @staticmethod
    def search_user():
        handle = input("Who do you want to search: ")
        return handle
        # server
        # if s.user_exists(handle):
        #     Interaction.searchscreen(handle, user, s)
        # else:
        #     print("No such user exists")


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
    def logInUser(s: sqliteDB, handle, password):
        if s.verify_login(handle, password):
            # print("---Logged In---") -- client
            user = s.getUserViaHandle(handle)
            user = User(*user)
            return user
            # Authenticate.redirectToHomeScreen(user, s)
        else:
            return False
            # print("\nSorry wrong credentials, try again!")
            # Interaction.logInScreen()

    @staticmethod
    def loggedInChoice(user, option, s: sqliteDB):
        if option == 8:
            print("\nLOGGED OUT--------")
            return

        elif option == 1:
            Interaction.tweet(user, s)

        elif option == 3:
            Interaction.get_feed(user, s)

        elif option == 4:
            follow_handle = input("Who do you want to follow: ")
            Interaction.follow_someone(user, follow_handle, s)

        elif option == 5:
            follow_handle = input("Who do you want to unfollow: ")
            Interaction.unfollow_someone(user, follow_handle, s)

        elif option == 7:
            Interaction.getTweetsViaHashtag(user, s)

        elif option == 2:
            Interaction.search_user(user, s)

        Interaction.loggedInOptions(user, s)

    @staticmethod
    def redirectToHomeScreen(handle):
        print("\nHi, %s!" % handle)
        print("What would you like to do?")

        Interaction.loggedInOptions(handle)
