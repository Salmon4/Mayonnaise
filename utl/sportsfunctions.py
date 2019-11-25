import sqlite3, json
from utl import dbfunctions
from urllib.request import urlopen

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
