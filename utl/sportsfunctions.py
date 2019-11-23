import sqlite3
from utl import dbfunctions

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
