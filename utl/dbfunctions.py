import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
from datetime import date #for checking recency of topnews table
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
				imageURL text
				);""")

#new day: reset topnews table
def resetnews(c):
	c.execute("DROP TABLE IF EXISTS topnews")
	c.execute("""CREATE TABLE topnews(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text
				);""")

def settopnews(c,news):
	date = news[0]['publishedAt'][0:10];
	dateToday = date.today();
	if (date == dateToday):
		return
	for article in news:
		image = article['urlToImage']
		author = article['author']
		url = article['url']
		datetime = article['publishedAt']
		title = article['title']
		if (image == None):
			image = "newspaper.jpg"
		if (author == None)
			author = "None"
		c.execute(
		"INSERT INTO topnews VALUES("+datetime+","+title+","+author+","url+","image+")"
		)
	return



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

def addUserPref(c, username, pref_area, pref):
	c.execute("INSERT INTO "+username+" VALUES('"+pref_area+"', '"+pref+"')")

def getUserPrefs(c, username, pref_area):
	c.execute("SELECT preference FROM "+username+" WHERE area = ?", (pref_area, ))
	return c.fetchall()
