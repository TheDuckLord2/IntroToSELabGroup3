import random
import sys
from datetime import datetime
import random

import mysql.connector


def create_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )

        if connection.is_connected():
            print("Connection to MySQL DB successful")
            return connection

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None  # Ensure this returns None on error


class User:

    # functional requirement functions
    def login(self):
        email = input("Email: ")
        password = input("Password: ")

        # setup database and query the database
        try:
            connection = create_connection("localhost", "root", "Shale951", "ecommerce_store")

        except:
            print("Failed database connection.")

            # exits the program if unsuccessful
            sys.exit()

        # cursor to send queries through
        cursor = connection.cursor()

        # sets up query and uses user input for the constraint
        # selects password to compare against user input password
        query = "SELECT id, password FROM user WHERE email=%s"
        data = (email,)

        cursor.execute(query, data)
        result = cursor.fetchall()

        # nothing was grabbed
        if (len(result) == 0):
            print("\nUser/Password combination is not in the system.")

            # these are mainly set for safety's sake
            self.userID = ""
            self.loggedIn = False

            return False

        # grabs result
        # --> [0][0] UserID
        # --> [0][1] Password
        userID = result[0][0]
        token = result[0][1]

        # closes connection
        cursor.close()
        connection.close()

        # successful login
        if (password == token):
            print("\nLogging user in...")

            ## set the class variables
            self.userID = userID
            self.loggedIn = True

            return True

        # unsuccessful login
        else:
            print("\nUser/Password combination is not in the system.")

            ## these are mainly set for safety's sake
            self.userID = ""
            self.loggedIn = False

            return False

    def logout(self):
        self.userID = ""
        self.loggedIn = False

        return False

    def viewAccountInformation(self):
        # setup database and query the database
        try:
            connection = create_connection("localhost", "root", "Shale951", "ecommerce_store")

        except:
            print("Failed database connection.")

            # exits the program if unsuccessful
            sys.exit()

        # cursor to send queries through
        cursor = connection.cursor()

        # sets up query and uses UserID from the currently logged in user
        # does NOT display the password or userID
        query = "SELECT email, first_name, last_name FROM user WHERE id=%s"
        data = (self.userID,)

        cursor.execute(query, data)
        result = cursor.fetchall()

        # grabs results
        # --> [0][0] Email
        # --> [0][0] FirstName
        # --> [0][1] LastName
        # --> [0][2] Address
        # --> [0][3] City
        # --> [0][4] State
        # --> [0][5] Zip
        # --> [0][6] Payment
        email = result[0][0]
        first = result[0][1]
        last = result[0][2]

        # displays results
        print("Name:", first, last)
        print("Email:", email, end='\n\n')


        # closes connection
        cursor.close()
        connection.close()

    def createAccount(self):
        # database connection
        try:
            connection = create_connection("localhost", "root", "Shale951", "ecommerce_store")

        except:
            print("Failed database connection.")

            # exits the program if unsuccessful
            sys.exit()

        # cursor to send queries through
        cursor = connection.cursor()

        # woefully inefficient ID creation
        # shouldn't need to actually loop because our sample set is so small
        # but just in case...
        while (1):
            # creates ID
            newID = str(random.randint(10, 99)) + "-" + str(random.randint(1000, 9999))

            # checks if it's in the database already
            query = "SELECT * FROM user WHERE id=%s"
            data = (newID,)

            cursor.execute(query, data)
            result = cursor.fetchall()

            # nothing was grabbed
            if (len(result) == 0):
                # we're free!
                break

        # continue with account creation

        print("Welcome to account creation!")
        print("Please type in your items for the prompts, hitting enter when you're done with each one.\n")



        id = random.randint(1,1000)
        password = input("Password: ")
        last_login = datetime.now()
        is_superuser = 0
        username = input("username: ")
        first_name = input("first name: ")
        last_name = input("Last name: ")
        email = input("email: ")
        is_staff = 0
        is_active = 1
        date_joined = datetime.now()
        account_type = "User"

        # tries to insert into the database
        query = "INSERT INTO user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, account_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, account_type)

        cursor.execute(query, data)
        connection.commit()

        print("\nAccount created.")

    # getters
    def getLoggedIn(self):
        return self.loggedIn

    #def getUserID(self):
     #   return self.userID

    #def create_connection(self, param, param1, param2, param3):
     #   pass
