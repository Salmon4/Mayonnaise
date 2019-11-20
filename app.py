from flask import Flask, render_template, request, redirect, url_for, session
import os


app = Flask(__name__)

app.secret_key = os.urandon(32)


DB_FILE = "mayonnaise.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations

def checkAuth():
    if "userID" in session:
        return True
    else:
        return False

@app.route("/")
def root():
    return render_template('homepage.html')


@app.route("/createAccount")
def createAccount():
    return render_template("createAcc.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")
    
    
if __name__ == "__main__":
    app.debug = True;
    app.run()

