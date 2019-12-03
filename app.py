from flask import Flask, render_template, request, redirect, url_for, session, flash
from urllib.request import urlopen
import json
import sqlite3, os
from utl import dbfunctions, sportsfunctions
from newsapi import NewsApiClient

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

@app.route("/logout")
def logOut():
    if checkAuth():
        session.pop('userID')
    return redirect("account")

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

@app.route("/oof", methods=["POST"])
def oof():
    #this is sad
    return render_template('oof.html')

@app.route("/acceptence", methods=["POST"])
def acceptence():
    #this is sad
    return redirect(url_for('login'))

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
        return redirect(url_for('account'))

@app.route("/news")
def news():
    loggedIn = True
    if (not(checkAuth())):
        loggedIn = False
    news = dbfunctions.gettopnews(c)
    if (dbfunctions.checkRecency(c)):
        newsapi = NewsApiClient(api_key='c10b74d97ec44a1f861474546fd3fc27')
        top_headlines = newsapi.get_top_headlines(language='en',country='us')
        data = top_headlines['articles']
        dbfunctions.settopnews(c,data)
        news = dbfunctions.gettopnews(c)
    return render_template("news.html",bool = loggedIn, articles=news)

@app.route("/yourNews")
def usernews():
    if (not(checkAuth())):
        return redirect(url_for('news'))
    user = session['username']
    types = ['business','health','general','science','technology','sports','entertainment']
    yourPrefs = dbfunctions.getUserPrefs(c,user,'news')
    news = []
    print(yourPrefs)
    for pref in yourPrefs:
        if (pref != []):
            pref = pref[0]
        if (not (dbfunctions.iscategoryRecent(c,pref))):
            newsapi = NewsApiClient(api_key='c10b74d97ec44a1f861474546fd3fc27')
            data = newsapi.get_top_headlines(language='en',country='us',category=pref,page = 1)['articles']
            dbfunctions.setnews(c,data,pref)
        news.extend(dbfunctions.getnewscategory(c,pref))
    return render_template("yourNews.html",categories = types,articles = news)

@app.route("/addcategory", methods = ['POST'])
def addcategory():
    if (not(checkAuth())):
        return redirect(url_for('news'))
    user = session['username']
    newPref = request.form['category']
    dbfunctions.addUserPref(c,user,'news',newPref)
    flash("Added " + newPref + " to your Preferences")
    return redirect(url_for('usernews'))

@app.route("/search", methods=['POST'])
def search():
    Search = request.form['search']
    newsapi = NewsApiClient(api_key='c10b74d97ec44a1f861474546fd3fc27')
    news = newsapi.get_everything(q=Search,language='en',page=1)['articles']
    return render_template("searchnews.html", search = Search, articles = news)

@app.route("/weather")
def weather():
    if (checkAuth()):
        tableBase = dbfunctions.getUserPrefs(c, session['username'], "location")
        first = tableBase[0]
        weatherUrl = urlopen("https://www.metaweather.com/api/location/" + first[0])
        log = True
    else:
        weatherUrl = urlopen("https://www.metaweather.com/api/location/2459115/")
        log = False
    allLocations = {'New York':'2459115','London':'44418','San Francisco':'2487956', 'Canada':'23424775',
    'Boston':'2367105', 'Chicago':'2379574', 'United Kingdom':'23424975'}


    weatherResponse = weatherUrl.read()
    weatherData = json.loads(weatherResponse)
    currentLocation = json.loads(weatherResponse)['title']
    return render_template("weather.html", allL=allLocations, location = currentLocation,
                            loggedIn = log,
                            pic=weatherData["consolidated_weather"][0]["weather_state_abbr"],DateToday=weatherData["consolidated_weather"][0]["applicable_date"],
                            TempToday='%.6s' % weatherData["consolidated_weather"][0]["the_temp"], HighestTemp='%.6s' % weatherData["consolidated_weather"][0]["max_temp"],
                            LowestTemp='%.6s' % weatherData["consolidated_weather"][0]["min_temp"], humidity='%.6s' % weatherData["consolidated_weather"][0]["humidity"],
                            windspeed='%.6s' % weatherData["consolidated_weather"][0]["wind_speed"],

                            pic1=weatherData["consolidated_weather"][1]["weather_state_abbr"],DateToday1=weatherData["consolidated_weather"][1]["applicable_date"],
                            TempToday1='%.6s' % weatherData["consolidated_weather"][1]["the_temp"], HighestTemp1='%.6s' % weatherData["consolidated_weather"][1]["max_temp"],
                            LowestTemp1='%.6s' % weatherData["consolidated_weather"][1]["min_temp"],

                            pic2=weatherData["consolidated_weather"][2]["weather_state_abbr"],DateToday2=weatherData["consolidated_weather"][2]["applicable_date"],
                            TempToday2='%.6s' % weatherData["consolidated_weather"][2]["the_temp"], HighestTemp2='%.6s' % weatherData["consolidated_weather"][2]["max_temp"],
                            LowestTemp2='%.6s' % weatherData["consolidated_weather"][2]["min_temp"],

                            pic3=weatherData["consolidated_weather"][3]["weather_state_abbr"],DateToday3=weatherData["consolidated_weather"][3]["applicable_date"],
                            TempToday3='%.6s' % weatherData["consolidated_weather"][3]["the_temp"], HighestTemp3='%.6s' % weatherData["consolidated_weather"][3]["max_temp"],
                            LowestTemp3='%.6s' % weatherData["consolidated_weather"][3]["min_temp"],

                            pic4=weatherData["consolidated_weather"][4]["weather_state_abbr"],DateToday4=weatherData["consolidated_weather"][4]["applicable_date"],
                            TempToday4='%.6s' % weatherData["consolidated_weather"][4]["the_temp"], HighestTemp4= '%.6s' % weatherData["consolidated_weather"][4]["max_temp"] ,
                            LowestTemp4='%.6s' % weatherData["consolidated_weather"][4]["min_temp"],

                            pic5=weatherData["consolidated_weather"][5]["weather_state_abbr"],DateToday5=weatherData["consolidated_weather"][5]["applicable_date"],
                            TempToday5='%.6s' % weatherData["consolidated_weather"][5]["the_temp"], HighestTemp5='%.6s' % weatherData["consolidated_weather"][5]["max_temp"],
                            LowestTemp5='%.6s' % weatherData["consolidated_weather"][5]["min_temp"]
                            )

@app.route("/changeLocation", methods=['POST'])
def changeLocation():
    newLocation = request.form['location']
    username = session['username']
    dbfunctions.updatePref(c, username, "location", newLocation)
    db.commit()
    return redirect(url_for('weather'))


@app.route("/money/<amount>")
def money(amount):
        if (checkAuth()):
            tableBase = dbfunctions.getUserPrefs(c, session['username'], "base_currency")
            first = tableBase[0]
            exchangeUrl = urlopen("https://api.exchangerate-api.com/v4/latest/" + first[0])
        else:
            exchangeUrl = urlopen("https://api.exchangerate-api.com/v4/latest/USD")
        exchangeResponse = exchangeUrl.read()
        base = json.loads(exchangeResponse)['base']
        allData = json.loads(exchangeResponse)['rates']
        print(amount)
        am = float(amount)
        if (checkAuth()):
            tableBase2 = dbfunctions.getUserPrefs(c, session['username'], "base_currency")
            first2 = tableBase[0]
            return render_template("money.html", b = first2, d = allData, count = 1
                                    , a = am, loggedIn = True)
        else:
            return render_template("money.html", b = base, d = allData, count = 1
                                    , a = am, loggedIn = False)
@app.route("/moneyprocess", methods=['POST','GET'])
def moneyprocess():
    i = request.form['amount']
    info = float(i)
    return redirect(url_for('money', amount = info))


@app.route("/changeBase/<am>", methods=['POST'])
def changeBase(am):
    newBase = request.form['base']
    username = session['username']
    dbfunctions.updatePref(c, username, "base_currency", newBase)
    db.commit()
    return redirect(url_for('money', amount = am))


@app.route("/account")
def account():
    if (checkAuth()):
        username = session['username']
        loggedIn = True
        return render_template("account.html", login = True, user = username)
    else:
        loggedIn = False
        return render_template("account.html", login = False)

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
    NHLtodayscores = sportsfunctions.getNHLTodayScores(c)
    NBAtodayscores = sportsfunctions.getNBAToday(c)
    print(NBAtodayscores)
    db.commit()
    #print(NHLtodayscores)
    # username = session['username']
    if checkAuth():
        username = session['username']
        userteams= sportsfunctions.getTeamsAdded(c, username)
        allteams=data['teams']
        userteamsdata = sportsfunctions.getUserTeamData(c, username,userteams, allteams)
        userteamsdata = sportsfunctions.addMostRecentGame(userteamsdata)
        userteamsdata = sportsfunctions.addNextGame(userteamsdata)
        # print(userteamsdata)
        teamsnotadded= sportsfunctions.getTeamsNotAdded(c, username, allteams)
        # print(teamsnotadded)
        return render_template("sports.html", loggedin=True, teams=teamsnotadded, user_teams=userteams, user_team_data=userteamsdata, NHLtoday=NHLtodayscores, NBAtoday=NBAtodayscores)
    else:
        return render_template("sports.html", logeedin=False, NHLtoday=NHLtodayscores, NBAtoday=NBAtodayscores)

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
