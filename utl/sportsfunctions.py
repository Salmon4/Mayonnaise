import sqlite3, json, datetime, requests
from datetime import date
from utl import dbfunctions
from urllib.request import urlopen

d = datetime.datetime.today()
date = d.strftime('%Y-%m-%d')

#get array of teams added to preferences
def getNHLTeamsAdded(c, username):
    teams = dbfunctions.getUserPrefs(c, username, "nhl_team")
    if teams is None:
        teams=[]
    else:
        teams[:] = [team[0] for team in teams]
    return teams

#get array of teams not yet added to prefs
#teams: array of total teams
def getNHLTeamsNotAdded(c, username, teams):
    userteams = getNHLTeamsAdded(c, username)
    teams[:] = [team for team in teams if team['name'] not in userteams]
    return teams

#returns just dictionary entries for user teams added
def getNHLUserTeamData(c, username, userteams, teamsdata):
    out = []
    for team in teamsdata:
        if team['name'] in userteams:
            out.append(team)
    return out

#retreives scores from today, adds them to databse if today's data is incomplete
# only adds 4 scores to database
def getNHLTodayScores(c):
    c.execute("SELECT * FROM nhl_scores;")
    scores = c.fetchall()
    #delete data from table if it's outdated:
    if len(scores) > 0 and scores[0][0] != date:
        c.execute("DELETE FROM nhl_scores;")
    #api data:
    u = urlopen("https://statsapi.web.nhl.com/api/v1/schedule")
    response = u.read()
    data = json.loads(response)
    data = data['dates'][0]['games']
    #only add to database if database is missing info
    #re-get nhl_scores in case they were reset
    c.execute("SELECT * FROM nhl_scores;")
    scores = c.fetchall()

    alreadyAdded = False

    for game in data:
        gamePk = game['gamePk']
        # print(gamePk)
        #check if this gamePk is already in the table
        if len(scores) == 0:
            c.execute("INSERT INTO nhl_scores VALUES (?, ?, ?, ?, ?, ?, ?)", (date, gamePk, game['teams']['home']['team']['name'],  game['teams']['away']['team']['name'], game['teams']['home']['score'], game['teams']['away']['score'], game['status']['detailedState']))

        else:
            alreadyAdded = False
            for tuple in scores:
                # print(tuple)
                if gamePk in tuple:
                    alreadyAdded = True
                    if tuple[6].__contains__("In Progress") or tuple[6].__contains__("Scheduled"):
                        c.execute("UPDATE nhl_scores SET home_score = ?, away_score = ?, status = ? WHERE gameID = ? ", (game['teams']['home']['score'], game['teams']['away']['score'], game['status']['detailedState'], gamePk))
                    #^if game is already in table, but was in progress/not started before, update:
            #add to table if hasn't been added yet
            if not alreadyAdded:
                c.execute("INSERT INTO nhl_scores VALUES (?, ?, ?, ?, ?, ?, ?)", (date, gamePk, game['teams']['home']['team']['name'],  game['teams']['away']['team']['name'], game['teams']['home']['score'], game['teams']['away']['score'], game['status']['detailedState']))
    #by nowthe table is updated, so return data from the table.
    c.execute("SELECT * FROM nhl_scores;")
    scores = c.fetchall()
    if len(scores) == 0:
        return "No games played or scheduled for today."
    return scores

#adds most recent game info to teamdata
#parameter: data of user pref's teams (getUserTeamData)
def addMostRecentGame(teamdata):
    out = {}
    for i in range(len(teamdata)):
        team = teamdata[i]
        teamID = team['id']
        u = urlopen("https://statsapi.web.nhl.com/api/v1/teams/"+str(teamID)+"?expand=team.schedule.previous")
        response = u.read()
        data = json.loads(response)
        #print(data)
        #only add game if team has played games this szn
        if "previousGameSchedule" in data['teams'][0]:
            teamdata[i]['prevgame'] = data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]
        else:
            teamdata[i]['prevgame'] = "No games played this season."
    return teamdata

#adds next game info to teamdata
#parameter: data of user pref's teams (getUserTeamData)
def addNextGame(teamdata):
    out = {}
    for i in range(len(teamdata)):
        team = teamdata[i]
        teamID = team['id']
        u = urlopen("https://statsapi.web.nhl.com/api/v1/teams/"+str(teamID)+"?expand=team.schedule.next")
        response = u.read()
        data = json.loads(response)
        #print(data)
        if "nextGameSchedule" in data['teams'][0]:
            teamdata[i]['nextgame'] = data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]
        else:
            teamdata[i]['nextgame'] = "No upcoming games."
    return teamdata
#----NBA---------------------------------------------------------------------------------------------------------------------------
#NOT ACTUALLY USING NBA DATA // API IS OUTDATED AND THERE IS NO FREE UPDATED ONE. :( :(
def getNBAToday(c):
    c.execute("SELECT * FROM nba_scores;")
    scores = c.fetchall()
    #print(len(scores))
    #delete data from table if it's outdated:
    # if len(scores) > 0 && scores[0][0].split("T")[0] != date:
    if len(scores) > 0 and scores[0][0] != date:
        c.execute("DELETE FROM nba_scores;")
    url = "https://free-nba.p.rapidapi.com/games"
    querystring = {"date":"2019-12-02"}
    headers = {
        'x-rapidapi-host': "free-nba.p.rapidapi.com",
        'x-rapidapi-key': "eedd51b020mshc462a1043ca26dep113106jsn43a6a1a8e712"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    data = data['data']
    if len(scores) < 3:
        for game in data:
            gameID = game['id']
            # print(gamePk)
            #check if this gamePk is already in the table
            if len(scores) == 0:
                #print("len=0inserting")
                c.execute("INSERT INTO nba_scores VALUES (?, ?, ?, ?, ?, ?, ?)", (date, gameID, game['home_team']['full_name'],  game['visitor_team']['full_name'], game['home_team_score'], game['visitor_team_score'], game['status']))
            else:
                for tuple in scores:
                    # print(tuple)
                    if gameID not in tuple:
                        #print("inserting")
                        c.execute("INSERT INTO nba_scores VALUES (?, ?, ?, ?, ?, ?, ?)", (date, gameID, game['home_team']['full_name'],  game['visitor_team']['full_name'], game['home_team_score'], game['visitor_team_score'], game['status']))
                    #if game is already in table, but was in progress/not started before, update:
                    elif game[6] != "Final":
                        c.execute("UPDATE nba_scores SET home_score = ?, away_score = ?, status = ? WHERE gameID = ? ", (game['home_team_score'], game['visitor_team_score'], game['status'], gameID))
    #by nowthe table is updated, so return data from the table.
    c.execute("SELECT * FROM nba_scores;")
    scores = c.fetchall()
    return scores
#--------------NFL-------------------------------------------------------------------------------
#gets all teams as well data for each one
def getNFLTeams():
    u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/Teams?key=a5f39026df8640e18f44f1b0c8e0685f")
    response = u.read()
    data = json.loads(response)
    return data

#returns a list of teams user has added to preferences (converts from list of tuples to list)
def getNFLTeamsList(c, username):
    teams = dbfunctions.getUserPrefs(c, username, "nfl_team")
    if teams is None:
        teams=[]
    else:
        teams[:] = [team[0] for team in teams]
    return teams

#get array of teams not yet added to prefs
#teams: array of total teams
def getNFLTeamsNotAdded(c, username, teams):
    userteams = getNFLTeamsList(c, username)
    teams[:] = [team for team in teams if team['FullName'] not in userteams]

    return teams

#gets all players on a given team
#teamname = its abbreviation
def getNFLPlayers(teamname):
    u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/Players/"+teamname+"?key=a5f39026df8640e18f44f1b0c8e0685f")
    response = u.read()
    data = json.loads(response)
    return data

#gets current standings (top 3 teams)
def getNFLStandings():
    return 0

#gets current season week, updates databse if necessary
def getNFLWeek(c):
    c.execute("SELECT * FROM nfl_week;")
    week = c.fetchall()
    d = datetime.datetime.today()
    date = d.strftime('%Y-%m-%d')
    if len(week) == 0:
        print("updating season week")
        u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/CurrentWeek?key=a5f39026df8640e18f44f1b0c8e0685f")
        response = u.read()
        data = json.loads(response)
        week = int(data)
        c.execute("INSERT INTO nfl_week VALUES(?, ?, ?)", (date,datetime.datetime.today().weekday(),week))
        c.execute("SELECT * FROM nfl_week;")
        week = c.fetchall()[0][2]
        return week
    #only get new week if it is monday and you haven't updated this week
    today = date(int(date[0:4]), int(date[5:7]), int(date[8:]))
    last_updated = date(int(week[0][0][0:4]), int(week[0][0][5:7]), int(week[0][0][8:]))
    diff = today - last_updated
    if diff > 7 or (datetime.datetime.today().weekday() == 0 and week[0][0] != date):
        print("updating season week")
        u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/CurrentWeek?key=a5f39026df8640e18f44f1b0c8e0685f")
        response = u.read()
        data = json.loads(response)
        week = int(data)
        c.execute("DELETE FROM nfl_week;")
        c.execute("INSERT INTO nfl_week VALUES(?, ?, ?)", (date,datetime.datetime.today().weekday(),week))
    c.execute("SELECT * FROM nfl_week;")
    week = c.fetchall()[0][2]
    return week

#updates nfl_scores database, returns data from table
def getNFLToday(c):
    c.execute("SELECT * FROM nfl_scores;")
    scores = c.fetchall()

    #delete data from table if it's outdated:
    if len(scores) > 0 and scores[0][0] != date:
        c.execute("DELETE FROM nfl_scores;")
        c.execute("SELECT * FROM nfl_scores;")
        scores = c.fetchall()

    #api data:
    #first get season week #:
    u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/CurrentWeek?key=a5f39026df8640e18f44f1b0c8e0685f")
    response = u.read()
    data = json.loads(response)
    week = int(data)
    #get team stats
    u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/TeamGameStats/2019/"+str(week)+"?key=a5f39026df8640e18f44f1b0c8e0685f")
    response = u.read()
    data = json.loads(response)
    #only add to database if database is missing info
    #print(data)

    alreadyAdded = False

    for game in data:
        #print(game['Date'].split("T")[0])
        if game['Date'].split("T")[0] == date:
            print("game found")
            gameID = game['GameKey']
            # print(gamePk)
            #check if this gamePk is already in the table
            if len(scores) == 0:
                c.execute("INSERT INTO nfl_scores VALUES (?, ?, ?, ?, ?, ?, ?)", (date, gameID, game['Team'],  game['Opponent'], game['Score'], game['OpponentScore'], game['IsGameOver']))

            else:
                alreadyAdded = False
                for tuple in scores:
                    # print(tuple)
                    if gameID in tuple:
                        alreadyAdded = True
                        #if game is already in table, but was in progress/not started before, update:
                        if tuple[6] == 0:
                            c.execute("UPDATE nhl_scores SET home_score = ?, away_score = ?, status = ? WHERE gameID = ?", (game['Score'], game['OpponentScore'], game['IsGameOver'], gameID))
                #insert game if it hasn't already been added
                if not alreadyAdded:
                    c.execute("INSERT INTO nfl_scores VALUES (?, ?, ?, ?, ?, ?, ?)", (date, gameID, game['Team'],  game['Opponent'], game['Score'], game['OpponentScore'], game['IsGameOver']))
    c.execute("SELECT * FROM nfl_scores;")
    scores = c.fetchall()
    if len(scores) == 0:
        return "No games played or scheduled for today."
    return scores

#returns data for teams user has added
def getNFLTeamsAdded(c,username):
    c.execute("SELECT * FROM "+username+" WHERE area = 'nfl_team'")
    teams = c.fetchall()

    u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/Standings/2019?key=a5f39026df8640e18f44f1b0c8e0685f")
    response = u.read()
    data = json.loads(response)

    out = []

    for team in teams:
        team = team[1] #team[1] is where the preference is stored
        for teamdata in data:
            if teamdata['Name'] == team:
                out.append(teamdata)
    return out
