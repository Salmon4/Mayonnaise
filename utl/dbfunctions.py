import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
from datetime import date #for checking recency of topnews table
lastHitApi = ""
#create 2 general tables
def setup(c):
	c.execute("""CREATE TABLE IF NOT EXISTS users(
				userID integer PRIMARY KEY,
				username text,
				password text
				);""")
	c.execute("""CREATE TABLE IF NOT EXISTS topnews(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")
	c.execute("""CREATE TABLE IF NOT EXISTS nhl_scores(
				datetime text,
				gameID integer,
				home text,
				away text,
				home_score integer,
				away_score integer
				);""")

def gettopnews(c):
	c.execute("SELECT * FROM topnews")
	news = c.fetchall()
	return news

#new day: reset topnews table

def resetnews(c):
	c.execute("DROP TABLE IF EXISTS topnews")
	c.execute("""CREATE TABLE topnews(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")
def checkRecency(c):
	global lastHitApi
	dateToday = date.today()
	if (gettopnews(c) != []):
		print(dateToday)
		if (dateToday == lastHitApi):
			return False
	else:
		lastHitApi= dateToday
		return True
	return True


def settopnews(c,news):
	resetnews(c)
	for article in news:
		image = article['urlToImage']
		author = article['author']
		url = article['url']
		datetime = article['publishedAt']
		title = article['title']
		description = article['description']
		if (description == None):
			description = "None"
		if (image == None):
			image = "newspaper.jpg"
		if (author == None):
			author = "N/A"
		c.execute(
		"INSERT INTO topnews VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
		)
	return False


#deletes all existing tables
def reset(c):
    #LATER: create loop to delete every single user table
    c.execute("SELECT COUNT(1)")

    #delete users and topnews table
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS topnews")

#==========================================================
def newUserTable(c, username):
	c.execute("CREATE TABLE IF NOT EXISTS "+username+" (area text, preference text)")
	addUserPref(c, username, "base_currency", "USD")
	addUserPref(c, username, "location", "2459115")

def addUserPref(c, username, pref_area, pref):
	c.execute("INSERT INTO "+username+" VALUES('"+pref_area+"', '"+pref+"')")

def getUserPrefs(c, username, pref_area):
	c.execute("SELECT preference FROM "+username+" WHERE area = ?", (pref_area, ))
	return c.fetchall()

def updatePref(c , username, pref_area, pref):
	c.execute("UPDATE "+username+" SET preference = '"+pref+"' WHERE area = ?", (pref_area,))
