# Team Crabs: Karl Hernandez, Arib Chowdhury, Anya Zorin, Saqif Abedin
# Softdev
# P3: ArRESTed Development, JuSt in Time
# 2021-04-23
import sqlite3
import hashlib
# from os import urandom
# salt = urandom(32)
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

    command = "CREATE TABLE IF NOT EXISTS users(username TEXT, password BLOB, id INTEGER PRIMARY KEY AUTOINCREMENT);"
    command += "CREATE TABLE IF NOT EXISTS leaderboard(username TEXT, correct INT, incorrect INT, score INT);"

    # executes the command and commits the change
    c.executescript(command)
    db.commit()


# returns the username and password for a given user_id in a tuple (username,
# password)
# consider case when 2 users have the same username and password. Technically
# would work because they have different ids. Should we make username unique as well?
def getUserId(username: str) -> int:
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    info = 0
    for row in c.fetchall():
        info = row[0]

    return info


# returns a username for any given user_id
def getUsername(user_id: int) -> str:
    c.execute("SELECT username FROM users WHERE id = ?", (str(user_id),))
    user = ""
    for row in c.fetchall():
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
    c.execute(
        "SELECT username, password, id FROM users WHERE username = ?", (username,)
    )
    info = ()
    for row in c.fetchall():
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
    elif (info[0] == username) and (
        info[1] == hashlib.sha256(password.encode()).hexdigest()
    ):
        return (True, None, info[2])
    return (False, "Incorrect username or password", None)


# registers a new user by adding their info to the db
# returns the unique user_id so that it can be added to the session in app.py
def registerUser(username: str, password: str):
    hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users VALUES (?, ?, NULL)", (username, hash))
    c.execute("INSERT INTO leaderboard VALUES (?, 0, 1, 0)", (username,))
    db.commit()


def updateLeaderboardDB(
    username, correct, incorrect
):  # Function to update leaderboard DB after a game ends
    c.execute(
        "UPDATE leaderboard SET correct = correct + ?, incorrect = incorrect + ? WHERE username = ?",
        (correct, incorrect, username),
    )
    c.execute(
        "UPDATE leaderboard SET score = 10000*correct/incorrect WHERE username = ?",
        (username,),
    )
    db.commit()
    print("It has been committed")


def top5():  # Function to return top 5 people in leaderboard along with scores
    c.execute("SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5")
    output = []
    for row in c.fetchall():
        output.append([row[0], row[3]])
    output += [["", ""] for _ in range(5 - len(output))]
    return output


# closes the database (only use if user logging out i think)
def close():
    db.close()
