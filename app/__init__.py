from flask import Flask, render_template, request, session, redirect
from requests import get
from .db_manager import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)  # random 32 bit key
createTables()


@app.route("/")
def index():
    if "username" in session:  # <username> dpdt on form submission args
        return redirect("/home")  # dpdt on home.html
    return render_template("login.html")  # dpdt on login.html


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
    return render_template("error.html", error=issue)  # dpdt on error.html


# register func
@app.route("/register")  # this route should be callable on login.html
def register():
    return render_template("register.html")  # dpdt on register.html


# take you to home page after creating account
@app.route("/registerRead", methods=["POST"])
def registerRedirect():
    # <username> & <password> dpdt on form args
    tempUser = request.form["username"]
    users = []
    for _id in getAllUsers():
        users.append(getUsername(_id))
    if tempUser in users:
        return render_template("error.html", error="Username already exists")
    tempPass = request.form["password"]
    registerUser(tempUser, tempPass)
    return redirect("/")  # dpdt on home.html


@app.route("/home")
def home():
    return "you are home"


# logout func
@app.route("/logout")
def logout():
    session.pop("username")  # <username> & <password> dpdt on form args
    session.pop("password")
    if "blog_id" in session:
        session.pop("blog_id")
    return redirect("/")  # dpdt on login.html


@app.route("/test")
def test():
    url = "https://pokeapi.co/api/v2/pokemon/1"
    response = get(url).json()
    img = response["sprites"]["front_shiny"]
    return "<img src={}>".format(img)


if __name__ == "__main__":
    app.run(debug=True)
