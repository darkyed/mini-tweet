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
    def tweet(user: User, s: sqliteDB):
        print("\nYou chose to tweet!-----")
        text = input("Enter your text: ")
        s.add_tweet(user, text)
        print("Posted your tweet to timeline: %s. . ." % text[:20])
        Interaction.loggedInOptions(user, s)

    @staticmethod
    def get_feed(user, s, top_tweets=10):
        following_list = s.get_following_list(user)
        print(following_list)
        tweets = []
        for following in following_list:
            tweets.append(s.get_tweets(following[0]))
        # TODO print sth
        print(tweets)
        Interaction.loggedInOptions(user, s)

    @staticmethod
    def follow_someone(user, follow_handle, s):
        if s.user_exists(follow_handle):
            if not s.following_exists(user, follow_handle):
                s.add_follow(user, follow_handle)
                print("\nYou are now following: %s" % follow_handle)
                Interaction.loggedInOptions(user, s)
            else:
                print("\nYou already follow him/her")
                Interaction.loggedInOptions(user, s)
        else:
            print("\nNo such user exists")
            Interaction.loggedInOptions(user, s)

    @staticmethod
    def unfollow_someone(user, follow_handle, s):
        if s.user_exists(follow_handle):
            if s.following_exists(user, follow_handle):
                s.delete_follow(user, follow_handle)
                # TODO print status
            else:
                # TODO replace return by print
                # TODO redirect to loggedin
                return "You don't follow him/her"
        else:
            # TODO replace return by print
            return "No such user exists"

    # TODO - Peeyush
    # def getTweetsViaHashtag(hashtag,s):
    #     if


class Authenticate:

    @staticmethod
    def registerUser(user, password):
        s = sqliteDB()
        print("Added user:", user)
        try:
            # makeEntry(user, password)
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

        elif option == 1:
            Interaction.tweet(user, s)

        elif option == 3:
            Interaction.get_feed(user, s)

        # TODO rest of features [1-7] to be  completed by Peeyush/Rushil
        # else:
        #     print('not log out')

    @staticmethod
    def redirectToHomeScreen(user, sqldb):
        print("\nHi, %s!" % user.handle)
        print("What would you like to do?")

        Interaction.loggedInOptions(user, sqldb)
