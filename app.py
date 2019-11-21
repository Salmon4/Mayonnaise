from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from utl import dbfunctions

app = Flask(__name__)

app.secret_key = os.urandom(32)


DB_FILE = "mayonnaise.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations

dbfunctions.setup(c)

def checkAuth():
    print(session)
    if "userID" in session:
        return True
    else:
        return False

@app.route("/")
def root():
    if checkAuth():
        #metaweather api added. Trying to add variables now. Only New York.
        u = urllib2.urlopen("https://www.metaweather.com/api/location/2459115/")
        response = u.read()
        data = json.loads(response)
        username = session['username']
        flash("Welcome " + username + ". You have been logged in successfully.")
        redirect(url_for('home'))
    return render_template('homepage.html')


@app.route("/createAccount")
def createAccount():
    if checkAuth():
        redirect(url_for('home'))
    return render_template("createAcc.html")

@app.route("/register", methods=["POST"])
def register():
    print(request)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        c.execute("SELECT username FROM users WHERE username = ?", (username, ))
        a = c.fetchone()
        if a != None:
            flash("Account with that username already exists")
            return redirect(url_for('createAccount'))
        elif password != password2:
            flash("Passwords do not match")
            return redirect(url_for('createAccount'))
        elif len(password) < 8:
            flash("Password must be at least 8 characters in length")
            return redirect(url_for('createAccount'))

        else:
            c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
            db.commit()
            flash("Successfuly created user")
            return redirect(url_for('login'))
    else:
        flash("GET request")
        return redirect(url_for('createAccount'))

@app.route("/login")
def login():
    # if already logged in, don't display login page
    if checkAuth():
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form['username']
    password = request.form['password']
    c.execute("SELECT userID, password FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    if a == None:
        flash("No user found with given username")
        return redirect(url_for('login'))
    elif password != a[1]:
        flash("Incorrect password")
        return redirect(url_for('login'))
    else:
        session['userID'] = a[0]
        session['username'] = username
        flash("Welcome " + username + ". You have been logged in successfully.")
        return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    print(session)
    session.pop('userID')
    session.pop('username')
    return redirect(url_for('root'))


if __name__ == "__main__":
    app.debug = True;
    app.run()

db.commit()
db.close()
