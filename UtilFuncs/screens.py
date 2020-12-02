from UtilFuncs.User import User
from UtilFuncs.manageDB import sqliteDB
import getpass

class Interaction:

    @staticmethod
    def welcome():
        print("New user: 1. Log In")
        print("Existing user: 2. Sign Up/ Register")
        return Interaction.welcome_input()

    @staticmethod
    def welcome_input():
        option = int(input("Choose (1) or (2): "))
        return option

    @staticmethod
    def loggedInOptions(handle):
        print(
            """
            1. Tweet
            2. Find someone via handle
            3. Get Updates
            4. Follow users via handle
            5. Unfollow users via handle
            6. Show all followers
            7. Search tweets using hashtag
            8. LOG-OUT
            """
        )

        option = 0
        try:
            option = int(input("Choose from [1-8]: "))
        except:
            print("Invalid choice")
            return Interaction.loggedInOptions(handle)
        if not (0 < option < 9):
            print("Invalid choice")
            return Interaction.loggedInOptions(handle)
        else:
            return str(option)


    @staticmethod
    def logInScreen():
        print("\nLOGIN SCREEN---------")
        handle = input("Enter your handle: ")
        password = getpass.getpass("Enter your Password: ")
        return handle, password


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
        if not (0 < number < 4):
            print("invalid option, try again!")
            Interaction.searchscreen(handle)
        else:
            return str(number)

    @staticmethod
    def print_tweets(tweet_list):
        for tweet in tweet_list:
            print("%s tweeted %s" % (tweet[2], tweet[1]))

    @staticmethod
    def tweet():
        print("\nYou chose to tweet!-----")
        text = input("Enter your text: ")
        return text

    @staticmethod
    def get_feed(user, s: sqliteDB, top_tweets=10):
        tweet_list = s.get_all_tweets_of_following(user.handle)
        return tweet_list

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

    @staticmethod
    def unfollow_someone(user, follow_handle, s: sqliteDB):
        if s.user_exists(follow_handle):
            if s.following_exists(user, follow_handle):
                s.delete_follow(user.handle, follow_handle)
                return "Deleted follower"
            else:
                return "You don't follow him/her"
        else:
            return "No such user exists"

    @staticmethod
    def delete_follower(user, follow_handle, s: sqliteDB):
        if s.user_exists(follow_handle):
            if s.following_exists_delete(follow_handle,user):
                s.delete_follow(follow_handle, user.handle)
                print("Deleted")
                return "Deleted following"
            else:
                return "That handle doesn't don't follow you"
        else:
            return "No such user exists"


    @staticmethod
    def getTweetsViaHashtag(user, hashtag, s: sqliteDB):
        command = '''SELECT tweets.tweet_id, tweets.tweet_text, tweets.author 
        FROM tweets INNER JOIN hashtags ON tweets.tweet_id=hashtags.t_id AND hashtags.tag=?'''
        s.cur.execute(command, (hashtag,))
        tweets = s.cur.fetchall()
        return tweets

    @staticmethod
    def search_user():
        handle = input("Who do you want to search: ")
        return handle


class Authenticate:

    @staticmethod
    def logInUser(s: sqliteDB, handle: str, password: str):
        if s.verify_login(handle, password):
            user = s.getUserViaHandle(handle)
            user = User(*user)
            return user
        else:
            return False

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

        return Interaction.loggedInOptions(handle)
