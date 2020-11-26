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
        if option==1:
            Interaction.logInScreen()
        if option==2:
            Interaction.registerScreen()
    
    
    @staticmethod
    def loggedInOptions(user):
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
            Interaction.loggedInOptions(user)
        if not (0<option<9):
            print("Invalid choice")
            Interaction.loggedInOptions(user)
        else:
            Authenticate.loggedInChoice(user, option)
    

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



class Authenticate:

    @staticmethod
    def registerUser(user, password):
        s = sqliteDB()
        print("Added user:", user)
        try:
            # makeEntry(user, password)
            s.add_user(user, password)
            Authenticate.redirectToHomeScreen(user,s)

        except Exception as e:
            print("\n" + e)
            Interaction.registerScreen()

    
    @staticmethod
    def logInUser(handle, password):
        if handle=='yo' and password=='oy':
            print("---Logged In---")
            # user = getUserViaHandle(handle)
            # Authenticate.redirectToHomeScreen(user)
        else:
            print("\nSorry wrong credentials, try again!")
            Interaction.logInScreen()

            
        # if (user.handle in db):
        #     if db.user.password == password:
        #         redirectToHomeScreen(user)
        # else:
        #     print("Sorry wrong credentials")
        #     Interaction.logInScreen()
    
    @staticmethod
    def loggedInChoice(user, option):
        if option==7:
            print("\nLOGGED OUT--------")
            pass
        else:
            print('not log out')

    
    @staticmethod
    def redirectToHomeScreen(user, sqldb):
        print("\nHi, %s!" % user.handle)
        print("What would you like to do?")
        Interaction.loggedInOptions(user)
        # if user.loggedIn:
        #     getContents(user)
        # else:
        #     raise "User no Logged In"
    