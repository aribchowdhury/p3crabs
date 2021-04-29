# Team Crabs: Karl Hernandez, Arib Chowdhury, Anya Zorin, Saqif Abedin
# Softdev
# P3: ArRESTed Development, JuSt in Time
# 2021-04-23
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, emit
from requests import get
from .db_manager import *
from .player_cpu import PlayerCPU
from .pvp import PlayerVsPlayer
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(32)  # random 32 bit key
socketio = SocketIO(app)
game, correct, incorrect = None, 0, 0
data = {}
createTables()


@app.route("/")
def index():
    if "username" in session:  # <username> dpdt on form submission args
        return redirect("/home")  # dpdt on home.html
    return render_template("login.html")  # dpdt on login.html


@app.route("/cpu")
def cpu():
    global game
    game = PlayerCPU()
    playerSprite, bossSprite = game.getSprites()
    playerHealth, bossHealth = game.healthCheck()
    game.newQuestion()
    print(game.answer)
    print(game.choices)
    return render_template(
        "battle.html",
        name1=session["username"],
        sprite1=playerSprite,
        sprite2=bossSprite,
        hp1=playerHealth,
        hp2=bossHealth,
        question=game.question,
        choices=game.choices,
    )


@app.route("/CPUcheckAnswer", methods=["POST"])
def checkAnswer():
    global game, correct, incorrect
    choice = int(request.form["answer"])
    check = game.checkAnswer(game.choices[choice])  # 1-4
    correct += check
    incorrect += not (check)
    playerSprite, bossSprite = game.getSprites()
    playerHealth, bossHealth = game.healthCheck()
    if float(playerHealth[:-1]) <= 0:
        updateLeaderboardDB(session["username"], correct, incorrect)
        correct = 0
        incorrect = 0
        return render_template("lose.html")
    if float(bossHealth[:-1]) <= 0:
        updateLeaderboardDB(session["username"], correct, incorrect)
        correct = 0
        incorrect = 0
        return render_template("win.html")
    game.newQuestion()
    print(game.answer)
    print(game.choices)
    return render_template(
        "battle.html",
        name1=session["username"],
        sprite1=playerSprite,
        sprite2=bossSprite,
        hp1=playerHealth,
        hp2=bossHealth,
        question=game.question,
        choices=game.choices,
    )


@app.route("/loginRead", methods=["POST"])  # takes info from the login form
def login():
    # <username> & <password> dpdt on form args
    tempUser = request.form["username"]
    tempPass = request.form["password"]
    loginS, issue, user_id = checkLogin(tempUser, tempPass)
    if loginS:  # dpdt on DB methods to match user and pass
        session["username"] = tempUser
        session["password"] = tempPass
        session["user_id"] = user_id
        return redirect("/home")  # dpdt on home.html

    # we will pass issue as an argument
    # vague error
    return render_template(
        "login.html", err="is-invalid", errmsg=issue
    )  # dpdt on error.html


# register func
@app.route("/register")  # this route should be callable on login.html
def register():
    return render_template("register.html")  # dpdt on register.html


@app.route("/battle")  # this route should be callable on login.html
def battle():
    return render_template("battle.html")  # dpdt on register.html


# take you to home page after creating account
@app.route("/registerRead", methods=["POST"])
def registerRedirect():
    # <username> & <password> dpdt on form args
    tempUser = request.form["username"]
    users = []
    for _id in getAllUsers():
        users.append(getUsername(_id))
    if tempUser in users:
        return render_template(
            "register.html", err="is-invalid", errmsg="Username already exists"
        )
    tempPass = request.form["password"]
    registerUser(tempUser, tempPass)
    return redirect("/")  # dpdt on home.html


@app.route("/pvp")
def pvp():
    global pvp_game
    global data
    pvp_game = PlayerVsPlayer()
    playerSprite, bossSprite = pvp_game.getSprites()
    pvp_game.newQuestion()
    player_health, opponent_health = pvp_game.healthCheck()
    data = {"PlayerHealth": player_health, "OpponetHealth": opponent_health}
    print(pvp_game.trivia[-1][0])
    return render_template(
        "cpu.html",
        sprite1=playerSprite,
        sprite2=bossSprite,
        answer=pvp_game.trivia[-1][0],
        super_img=pvp_game.trivia[-1][1],
        answer_len=pvp_game.trivia[-1][2],
        **data
    )


@app.route("/PVPcheckAnswer", methods=["POST"])
def pvp_check_answer():
    global pvp_game
    global data
    pvp_game.checkAnswer(request.form["testing"])
    playerSprite, bossSprite = pvp_game.getSprites()
    pvp_game.newQuestion()
    player_health, opponent_health = pvp_game.healthCheck()
    data = {"PlayerHealth": player_health, "OpponetHealth": opponent_health}
    return render_template(
        "cpu.html",
        sprite1=playerSprite,
        sprite2=bossSprite,
        answer=pvp_game.trivia[-1][0],
        super_img=pvp_game.trivia[-1][1],
        answer_len=pvp_game.trivia[-1][2],
        **data
    )


# annoucment = {"text": "Hello"}

# @socketio.on("join")
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + "has entered the room.", to=room)


# @socketio.on("health has changed")
# def value_changed(message):
#     global data
#     # pvp_game.checkAnswer(request.form["answer"])
#     data[message["who"]] = message["data"]
#     emit("update value", message, broadcast=True)


# @socketio.on('Slider value changed')
# def value_changed(message):
#     values[message['who']] = message['data']
#     emit('update value', message, broadcast=True)


@app.route("/home")
def home():
    board = top5()
    return render_template(
        "home.html",
        user1=board[0][0],
        score1=board[0][1],
        user2=board[1][0],
        score2=board[1][1],
        user3=board[2][0],
        score3=board[2][1],
        user4=board[3][0],
        score4=board[3][1],
        user5=board[4][0],
        score5=board[4][1],
    )


# logout func
@app.route("/logout")
def logout():
    session.pop("username")  # <username> & <password> dpdt on form args
    session.pop("password")
    if "blog_id" in session:
        session.pop("blog_id")
    return redirect("/")  # dpdt on login.html


# @app.route("/test")
# def test():
#     url = "https://pokeapi.co/api/v2/pokemon/1"
#     response = get(url).json()
#     img = response["sprites"]["front_shiny"]
#     return "<img src={}>".format(img)


if __name__ == "__main__":
    socketio.run(app, debug=True)
