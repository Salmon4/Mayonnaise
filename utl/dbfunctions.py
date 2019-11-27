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
				imageURL text
				);""")

def settopnews(c,news):
	if (gettopnews(c) != []):
		articleDate = news[0];
		print(articleDate)
		dateToday = date.today();
		print(dateToday)
		if (articleDate == dateToday):
			return True
	resetnews(c)
	for article in news:
		image = article['urlToImage']
		author = article['author']
		url = article['url']
		datetime = article['publishedAt']
		title = article['title']
		if (image == None):
			image = "/newspaper.jpg"
		if (author == None):
			author = "N/A"
		c.execute(
		"INSERT INTO topnews VALUES(?,?,?,?,?)",(datetime,title,author,url,image,)
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

def addUserPref(c, username, pref_area, pref):
	c.execute("INSERT INTO "+username+" VALUES('"+pref_area+"', '"+pref+"')")

def getUserPrefs(c, username, pref_area):
	c.execute("SELECT preference FROM "+username+" WHERE area = ?", (pref_area, ))
	return c.fetchall()
