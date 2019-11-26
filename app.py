from flask import Flask, render_template, request, redirect, url_for, session, flash
from urllib.request import urlopen
import json
import sqlite3, os
from utl import dbfunctions, sportsfunctions

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
        username = session['username']
        flash("Welcome " + username + ". You have been logged in successfully.")
        redirect(url_for('home', currentTab = 1))
    return render_template('homepage.html')


@app.route("/createAccount")
def createAccount():
    if checkAuth():
        redirect(url_for('home', currentTab = 1))
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
        elif " " in username:
            flash("Username cannot contain spaces")
            return redirect(url_for('createAccount'))
        elif password != password2:
            flash("Passwords do not match")
            return redirect(url_for('createAccount'))
        elif len(password) < 8:
            flash("Password must be at least 8 characters in length")
            return redirect(url_for('createAccount'))

        else:
            c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
            dbfunctions.newUserTable(c, username)
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
        return redirect(url_for('home', currentTab = 1))
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
        return redirect(url_for('home',currentTab = 1))

@app.route("/home/<currentTab>")
def home(currentTab):

    t1class = "tabs-panel"
    t2class = "tabs-panel"
    t3class = "tabs-panel"
    t4class = "tabs-panel"
    if (currentTab == '1'): #news
        t1class = "tabs-panel is-active"
        t2class = "tabs-panel"
        t3class = "tabs-panel"
        t4class = "tabs-panel"
        url = urlopen(
            "https://newsapi.org/v2/top-headlines?country=us&apiKey=c10b74d97ec44a1f861474546fd3fc27"
            )
        response = url.read()
        data = json.loads(response)['articles']
        return render_template("home.html", t1=t1class,t2=t2class,t3=t3class,t4=t4class, articles=data)
    if (currentTab == '2'):
        t1class = "tabs-panel" #weather
        t2class = "tabs-panel is-active"
        t3class = "tabs-panel"
        t4class = "tabs-panel"
        weatherUrl = urlopen("https://www.metaweather.com/api/location/2459115/")
        weatherResponse = weatherUrl.read()
        weatherData = json.loads(weatherResponse)
        return render_template("home.html", t1=t1class,t2=t2class,t3=t3class,t4=t4class,
                                pic=weatherData["consolidated_weather"][0]["weather_state_abbr"],DateToday=weatherData["consolidated_weather"][0]["applicable_date"],
                                TempToday='%.7s' % weatherData["consolidated_weather"][0]["the_temp"], HighestTemp='%.7s' % weatherData["consolidated_weather"][0]["max_temp"],
                                LowestTemp='%.7s' % weatherData["consolidated_weather"][0]["min_temp"],
                                pic1=weatherData["consolidated_weather"][1]["weather_state_abbr"],DateToday1=weatherData["consolidated_weather"][1]["applicable_date"],
                                TempToday1='%.7s' % weatherData["consolidated_weather"][1]["the_temp"], HighestTemp1='%.7s' % weatherData["consolidated_weather"][1]["max_temp"],
                                LowestTemp1='%.7s' % weatherData["consolidated_weather"][1]["min_temp"],
                                pic2=weatherData["consolidated_weather"][2]["weather_state_abbr"],DateToday2=weatherData["consolidated_weather"][2]["applicable_date"],
                                TempToday2='%.7s' % weatherData["consolidated_weather"][2]["the_temp"], HighestTemp2='%.7s' % weatherData["consolidated_weather"][2]["max_temp"],
                                LowestTemp2='%.7s' % weatherData["consolidated_weather"][2]["min_temp"],
                                pic3=weatherData["consolidated_weather"][3]["weather_state_abbr"],DateToday3=weatherData["consolidated_weather"][3]["applicable_date"],
                                TempToday3='%.7s' % weatherData["consolidated_weather"][3]["the_temp"], HighestTemp3='%.7s' % weatherData["consolidated_weather"][3]["max_temp"],
                                LowestTemp3='%.7s' % weatherData["consolidated_weather"][3]["min_temp"],
                                pic4=weatherData["consolidated_weather"][4]["weather_state_abbr"],DateToday4=weatherData["consolidated_weather"][4]["applicable_date"],
                                TempToday4='%.7s' % weatherData["consolidated_weather"][4]["the_temp"], HighestTemp4= '%.7s' % weatherData["consolidated_weather"][4]["max_temp"] ,
                                LowestTemp4='%.7s' % weatherData["consolidated_weather"][4]["min_temp"],
                                pic5=weatherData["consolidated_weather"][5]["weather_state_abbr"],DateToday5=weatherData["consolidated_weather"][5]["applicable_date"],
                                TempToday5='%.7s' % weatherData["consolidated_weather"][5]["the_temp"], HighestTemp5='%.7s' % weatherData["consolidated_weather"][5]["max_temp"],
                                LowestTemp5='%.7s' % weatherData["consolidated_weather"][5]["min_temp"]
                                )
    if (currentTab == '3'): #sports
        t1class = "tabs-panel"
        t2class = "tabs-panel"
        t3class = "tabs-panel is-active"
        t4class = "tabs-panel"
        u = urlopen("https://statsapi.web.nhl.com/api/v1/teams")
        response = u.read()
        data = json.loads(response)
        # username = session['username']
        if checkAuth():
            username = session['username']
            userteams= sportsfunctions.getTeamsAdded(c, username)
            allteams=data['teams']
            userteamsdata = sportsfunctions.getUserTeamData(c, username,userteams, allteams)
            userteamsdata = sportsfunctions.addMostRecentGame(userteamsdata)
		    # print(userteamsdata)
            teamsnotadded= sportsfunctions.getTeamsNotAdded(c, username, allteams)
		    # print(teamsnotadded)
            return render_template("home.html", t1=t1class,t2=t2class,t3=t3class,t4=t4class, loggedin=True, teams=teamsnotadded, user_teams=userteams, user_team_data=userteamsdata)
        else:
            return render_template("home.html", t1=t1class,t2=t2class,t3=t3class,t4=t4class, logeedin=False)

    if (currentTab == '4'): #money
        t1class = "tabs-panel"
        t2class = "tabs-panel"
        t3class = "tabs-panel"
        t4class = "tabs-panel is-active"
        #exchangeUrl = urlopen("https://api.exchangerate-api.com/v4/latest/USD")
        #exchangeResponse = exchangeUrl.read()
        #base = json.loads(exchangeResponse)['base']
        return render_template("home.html", t1=t1class,t2=t2class,t3=t3class,t4=t4class, articles=data
                            )

@app.route("/logout")
def logout():
    print(session)
    session.pop('userID')
    session.pop('username')
    return redirect(url_for('root'))

@app.route("/sports")
def sports():
    u = urlopen("https://statsapi.web.nhl.com/api/v1/teams")
    response = u.read()
    data = json.loads(response)
    # username = session['username']
    if checkAuth():
        username = session['username']
        userteams= sportsfunctions.getTeamsAdded(c, username)
        allteams=data['teams']
        userteamsdata = sportsfunctions.getUserTeamData(c, username,userteams, allteams)
        userteamsdata = sportsfunctions.addMostRecentGame(userteamsdata)
        # print(userteamsdata)
        teamsnotadded= sportsfunctions.getTeamsNotAdded(c, username, allteams)
        # print(teamsnotadded)
        return render_template("sports.html", loggedin=True, teams=teamsnotadded, user_teams=userteams, user_team_data=userteamsdata)
    else:
        return render_template("sports.html", logeedin=False)

@app.route("/dropdown")
def dropdown():
	return render_template("dropdown.html")

@app.route("/addsport", methods=["POST"])
def addsport():
    if request.method=="POST":
        print(request.form)
        team = request.form['team']
        username = session['username']
        dbfunctions.addUserPref(c, username, "nhl_team", team)
        db.commit()
    return redirect(url_for("sports"))

if __name__ == "__main__":
    app.debug = True;
    app.run()

db.commit()
db.close()
