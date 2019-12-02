import sqlite3, json, datetime
from utl import dbfunctions
from urllib.request import urlopen

d = datetime.datetime.today()
date = d.strftime('%Y-%m-%d')

#get array of teams added to preferences
def getTeamsAdded(c, username):
    teams = dbfunctions.getUserPrefs(c, username, "nhl_team")
    if teams is None:
        teams=[]
    else:
        teams[:] = [team[0] for team in teams]
    return teams

#get array of teams not yet added to prefs
#teams: array of total teams
def getTeamsNotAdded(c, username, teams):
    userteams = getTeamsAdded(c, username)
    teams[:] = [team for team in teams if team not in userteams]
    return teams

#returns just dictionary entries for user teams added
def getUserTeamData(c, username, userteams, teamsdata):
    out = []
    for team in teamsdata:
        if team['name'] in userteams:
            out.append(team)
    return out

#retreives scores from today, adds them to databse if today's data is incomplete
# only adds 4 scores to database
def getNHLTodayScores(c):
    # c.execute("INSERT INTO nhl_scores VALUES(?, ?, ?, ?, ?)", ("s", 2, "d", "d", 1, 2))
    c.execute("SELECT * FROM nhl_scores;")
    scores = c.fetchall()
    #print(len(scores))
    #delete data from table if it's outdated:
    # if len(scores) > 0 && scores[0][0].split("T")[0] != date:
    if len(scores) > 0 and scores[0][0] != date:
        c.execute("DELETE FROM nhl_scores;")
    #api data:
    u = urlopen("https://statsapi.web.nhl.com/api/v1/schedule")
    response = u.read()
    data = json.loads(response)
    data = data['dates'][0]['games']
    #only add to database if database is missing info
    print(data)
    if len(scores) < 3:
        for game in data:
            gamePk = game['gamePk']
            print(gamePk)
            #check if this gamePk is already in the table
            if len(scores) == 0:
                c.execute("INSERT INTO nhl_scores VALUES (?, ?, ?, ?, ?, ?)", (date, gamePk, game['teams']['home']['team']['name'],  game['teams']['away']['team']['name'], game['teams']['home']['score'], game['teams']['away']['score']))
            else:
                for tuple in scores:
                    print(tuple)
                    if gamePk not in tuple:
                        c.execute("INSERT INTO nhl_scores VALUES (?, ?, ?, ?, ?, ?)", (date, gamePk, game['teams']['home']['team']['name'],  game['teams']['away']['team']['name'], game['teams']['home']['score'], game['teams']['away']['score']))
    #by nowthe table is updated, so return data from the table.
    c.execute("SELECT * FROM nhl_scores;")
    scores = c.fetchall()
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
        print(data)
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
        print(data)
        if "nextGameSchedule" in data['teams'][0]:
            teamdata[i]['nextgame'] = data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]
        else:
            teamdata[i]['nextgame'] = "No upcoming games."
    return teamdata

#--------------NFL-------------------------------------------------------------------------------
#gets all teams
def getNFLTeams():
    u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/Teams?key=e02ffffce823403aa4fc815b9aa7f667")
    response = u.read()
    data = json.loads(response)
    return data

#gets all players on a given team
#teamname = its abbreviation
def getNFLPlayers(teamname):
    u = urlopen("https://api.sportsdata.io/v3/nfl/scores/json/Players/"+teamname+"?key=e02ffffce823403aa4fc815b9aa7f667")
    response = u.read()
    data = json.loads(response)
    return data

#gets current standings (top 3 teams)
