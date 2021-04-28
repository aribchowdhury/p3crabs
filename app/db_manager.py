# Team Crabs: Karl Hernandez, Arib Chowdhury, Anya Zorin, Saqif Abedin
# Softdev
# P3: ArRESTed Development, JuSt in Time
# 2021-04-23
import sqlite3

# for testing only
# import os
# os.remove("../blogdata.db")

DB_FILE = "./app/leaderboard.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# creates the tables
def createTables():

    # command to create the table of all users.
    # Columns:
    # username (str)
    # password (str)
    # unique id (int primary key)

    command = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);"
    command += "CREATE TABLE IF NOT EXISTS leaderboard(username TEXT, correct INT, incorrect INT, score INT);"

    # executes the command and commits the change
    c.executescript(command)
    db.commit()


# returns the username and password for a given user_id in a tuple (username,
# password)
# consider case when 2 users have the same username and password. Technically
# would work because they have different ids. Should we make username unique as well?
def getUserId(username: str) -> int:
    command = 'SELECT id FROM users WHERE username = "{}";'.format(username)
    info = 0
    for row in c.execute(command):
        info = row[0]

    return info


# returns a username for any given user_id
def getUsername(user_id: int) -> str:
    command = 'SELECT username FROM users WHERE id = "{}";'.format(user_id)
    user = ""
    for row in c.execute(command):
        user = row[0]
    return user


# returns a list of all the user_ids in the db
def getAllUsers():
    command = "SELECT id FROM users"
    ids = []
    for row in c.execute(command):
        ids.append(row[0])
    return ids


# returns (username, password, user_id) for a given username. Returns None
# if argument username is not present in the database
def getUserInfo(username: str):
    command = 'SELECT username, password, id FROM users WHERE username = "{}";'.format(
        username
    )
    info = ()
    for row in c.execute(command):
        info += (row[0], row[1], row[2])
    if info == ():
        return None
    return info


# returns a tuple in the following format: (login_successful, issue, user_id)
# login_successful will be either True (correct info) or False
# issue will be None if login_successful is True. Otherwise will be "user not found" or
# "incorrect username or password"
# user_id will be returned if login_successful. None if not login_successful
def checkLogin(username: str, password: str) -> tuple:
    info = getUserInfo(username)
    if info == None:
        return (False, "User not found", None)
    elif (info[0] == username) and (info[1] == password):
        return (True, None, info[2])
    return (False, "Incorrect username or password", None)


# registers a new user by adding their info to the db
# returns the unique user_id so that it can be added to the session in app.py
def registerUser(username: str, password: str):
    command = 'INSERT INTO users VALUES ("{}", "{}", NULL);'.format(username, password)

    c.execute(command)
    db.commit()

def updateLeaderboardDB(username, correct, incorrect): #Function to update leaderboard DB after a game ends
    command = 'UPDATE leaderboard SET correct = correct + {}, incorrect = incorrect + {} WHERE username = "{}";'.format(
        correct, incorrect, username)
    c.execute(command)
    command = 'UPDATE leaderboard SET score = CAST((correct/incorrect)*10000 AS INT) WHERE username = "{}";'.format(
        correct, incorrect, username)
    c.execute(command)
    db.commit()

def top5(): #Function to return top 5 people in leaderboard along with scores
    c.execute('SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5')
    for row in c.fetchall(): yield [row[0],row[3]]


# closes the database (only use if user logging out i think)
def close():
    db.close()


# For testing only
# if __name__ == "__main__":
#     createTables()

#     print(getUserId("ben"))
#     # createBlog(getUserId("ben"), "ben", "Doodoo",
#     #            "10/12/2020", "This is my blog.")

#     command = 'SELECT * FROM blogs'
#     for row in c.execute(command):
#         print(row)

#     print(checkLogin("benn", "dover"))

#     blogs = getUserBlogs(getUserId("ben"))

#     for blog in blogs:
#         title, bio, date = getBlogBasic(blog)
#         print(title)
#         print(bio)
#         print(date)
