from flask import Flask, render_template, redirect, url_for, session, flash, request
from urllib.request import urlopen
import json
import sqlite3, os, requests
from utl import dbfunctions, sportsfunctions
from newsapi import NewsApiClient

app = Flask(__name__)

app.secret_key = os.urandom(32)


DB_FILE = "mayonnaise.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor() #facilitate db operations

c.execute("drop table nfl_scores;")
dbfunctions.setup(c)

def checkAuth(): #checks if the user is logged in
    if "userID" in session:
        return True
    else:
        return False

@app.route("/")
def root():
    if checkAuth(): #checks if the user is logged in
        username = session['username']
        flash("Welcome " + username + ". You have been logged in successfully.")
        return redirect(url_for('account')) #if logged in, redirects to account page
    return render_template('homepage.html')


@app.route("/createAccount")
def createAccount():
    return render_template("createAcc.html")

@app.route("/logout")
def logOut(): #logs out the user and redirects to login page
    if checkAuth():
        session.pop('userID')
    return redirect("account")

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        c.execute("SELECT username FROM users WHERE username = ?", (username, ))
        a = c.fetchone()
        if a != None: #checks for duplicate usernames
            flash("Account with that username already exists")
            return redirect(url_for('createAccount'))
        elif " " in username: #checks for spaces cause spaces suck
            flash("Username cannot contain spaces")
            return redirect(url_for('createAccount'))
        elif password != password2: #checks if both passwords are the same
            flash("Passwords do not match")
            return redirect(url_for('createAccount'))
        elif len(password) < 8: #passwords must have a minimum length of 8
            flash("Password must be at least 8 characters in length")
            return redirect(url_for('createAccount'))

        else: #successfully created an account
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
        return redirect(url_for('account'))
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
    if a == None: #checks login username and password
        flash("No user found with given username") #no given username in database
        return redirect(url_for('login'))
    elif password != a[1]:
        flash("Incorrect password") #password is incorrect for given username
        return redirect(url_for('login'))
    else: #successfully pass the tests
        session['userID'] = a[0]
        session['username'] = username
        flash("Welcome " + username + ". You have been logged in successfully.")
        return redirect(url_for('account'))

@app.route("/news") #where the news article will be displayed
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
    types = ['business','health','general','science','technology','sports','entertainment'] #all the categories of news
    yourPrefs = dbfunctions.getUserPrefs(c,user,'news')
    news = []
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
    if (checkAuth()): #checks if logged in
        #if logged in, location is changeable
        tableBase = dbfunctions.getUserPrefs(c, session['username'], "location")
        first = tableBase[0]
        weatherUrl = urlopen("https://www.metaweather.com/api/location/" + first[0])
        log = True
    else:
        #otherwise it isn't
        weatherUrl = urlopen("https://www.metaweather.com/api/location/2459115/")
        log = False
    allLocations = {'New York':'2459115','London':'44418','San Francisco':'2487956',
    'Boston':'2367105', 'Chicago':'2379574', 'El Paso, Texas':'2397816', 'Seattle, Washington':'2490383',
        'Honolulu, Hawaii':'2423945','Baltimore, Maryland':'2358820'} #this is all of our locations that the user can look at with the Where On Earth ID (WOE)


    weatherResponse = weatherUrl.read()
    weatherData = json.loads(weatherResponse)
    currentLocation = json.loads(weatherResponse)['title'] #the name of the chosen place
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
    newLocation = request.form['location'] #new location selected from dropdown menu from weather.html
    username = session['username']
    dbfunctions.updatePref(c, username, "location", newLocation) #updates the current logged in user preference in weather location
    db.commit()
    return redirect(url_for('weather'))


@app.route("/money/<amount>") #amount is the amount of money that the user wants to be converted
def money(amount):
        if (checkAuth()): #checks if the user is logged in or not
            #you can only change the base currency when you are logged in
            tableBase = dbfunctions.getUserPrefs(c, session['username'], "base_currency")
            first = tableBase[0]
            exchangeUrl = urlopen("https://api.exchangerate-api.com/v4/latest/" + first[0])
        else:
            exchangeUrl = urlopen("https://api.exchangerate-api.com/v4/latest/USD")
        exchangeResponse = exchangeUrl.read()
        base = json.loads(exchangeResponse)['base']
        allData = json.loads(exchangeResponse)['rates']
        am = float(amount)
        if (checkAuth()): #different variables get pass to money.html so it will know what to display based on whether user is logged in
            tableBase2 = dbfunctions.getUserPrefs(c, session['username'], "base_currency") #chosen base currency is stored in table for later use
            first2 = tableBase[0]
            return render_template("money.html", b = first2, d = allData, count = 1
                                    , a = am, loggedIn = True)
        else:
            return render_template("money.html", b = base, d = allData, count = 1
                                    , a = am, loggedIn = False)
@app.route("/moneyprocess", methods=['POST','GET']) #changes the amount of money the user wants to be converted
def moneyprocess():
    i = request.form['amount'] #gets the new amount of money the user wants to convert
    info = float(i) #converts from string to float so it is able to be multiplied
    return redirect(url_for('money', amount = info))


@app.route("/changeBase/<am>", methods=['POST']) #changes the base type of currency the user wants
def changeBase(am):
    newBase = request.form['base'] #gets submitted new currency from dropdown menu
    username = session['username']
    dbfunctions.updatePref(c, username, "base_currency", newBase) #update the user's prefered currency for next usage
    db.commit()
    return redirect(url_for('money', amount = am))


@app.route("/account") #account management tab
def account():
    if (checkAuth()): #checks if logged in
        username = session['username']
        loggedIn = True
        newsPrefs = dbfunctions.getUserPrefs(c,username,"news")
        NHL_teams = dbfunctions.getUserPrefs(c,username,"nhl_team")
        NFL_teams = dbfunctions.getUserPrefs(c,username,"nfl_team")
        print(newsPrefs)
        print(NHL_teams)
        return render_template("account.html", login = True, user = username, news = newsPrefs, NHLteams = NHL_teams, NFLteams = NFL_teams)
    else:
        #user will be prompted to log in if desired
        loggedIn = False
        return render_template("account.html", login = False)

@app.route("/removepreference/<pref>")
def remove(pref):
    if (checkAuth()):
        username = session['username']
        dbfunctions.removePref(c,username,pref)
        flash("Removed " + pref + " from Preferences")
    return redirect(url_for('account'))

@app.route("/logout") #to log the user out of his account
def logout():
    session.pop('userID')
    session.pop('username')
    return redirect(url_for('root'))

@app.route("/sports")
def sports():
    #get all nhl teams, read into data
    u = urlopen("https://statsapi.web.nhl.com/api/v1/teams")
    response = u.read()
    data = json.loads(response)
    #update nhl_today and nfl_today tables and returns its data
    #used to display scores for today (displayed even if not logged in)
    NHLtodayscores = sportsfunctions.getNHLTodayScores(c)
    #NBAtodayscores = sportsfunctions.getNBAToday(c)
    NFLtodayscores = sportsfunctions.getNFLToday(c)
    print(len(NFLtodayscores))
    print("today done")
    db.commit()
    if checkAuth():
        username = session['username']
        #gets a list of user's NHL team prefs
        nhl_userteams= sportsfunctions.getNHLTeamsAdded(c, username)
        #allteams stores data on all nhl/nfl teams
        nhl_allteams=data['teams']
        nfl_allteams = sportsfunctions.getNFLTeams()
        #userteamsdata stores data only on NHL teams user has added to prefs
        #get general team data from api
        nhl_userteamsdata = sportsfunctions.getNHLUserTeamData(c, username,nhl_userteams, nhl_allteams)
        #add most recent game data
        nhl_userteamsdata = sportsfunctions.addMostRecentGame(nhl_userteamsdata)
        #add next game data
        nhl_userteamsdata = sportsfunctions.addNextGame(nhl_userteamsdata)
        nfl_userteamsdata = sportsfunctions.getNFLTeamsAdded(c, username)
        print("nfl user teams done")
        #list of teams in dropdown = teams user has not added yet
        nhlteamsnotadded= sportsfunctions.getNHLTeamsNotAdded(c, username, nhl_allteams)
        nfl_teamsnotadded = sportsfunctions.getNFLTeamsNotAdded(c, username, nfl_allteams)
        return render_template("sports.html", loggedin=True, nhl_teams=nhlteamsnotadded, nhl_user_teams=nhl_userteams, nhl_user_team_data=nhl_userteamsdata, NHLtoday=NHLtodayscores, nfl_teams=nfl_allteams, NFLtoday=NFLtodayscores, nfl_user_team_data=nfl_userteamsdata, nfl_teams_not_added=nfl_teamsnotadded)
    else:
        return render_template("sports.html", logeedin=False, NHLtoday=NHLtodayscores, NBAtoday=NBAtodayscores, NFLtoday=NFLtodayscores)

@app.route("/dropdown")
def dropdown():
	return render_template("dropdown.html")

@app.route("/addsport", methods=["POST"])
def addsport():
    if request.method=="POST":
        print(request.form)
        username = session['username']
        if "nhl_team" in request.form:
            team = request.form['nhl_team']
            dbfunctions.addUserPref(c, username, "nhl_team", team)
        if "nfl_team" in request.form:
            team = request.form['nfl_team']
            dbfunctions.addUserPref(c, username, "nfl_team", team)
        db.commit()
    return redirect(url_for("sports"))

if __name__ == "__main__":
    app.debug = True;
    app.run()

db.commit()
db.close()
