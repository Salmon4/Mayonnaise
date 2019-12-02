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

def resetbusiness(c):
	c.execute("DROP TABLE IF EXISTS business")
	c.execute("""CREATE TABLE business(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resethealth(c):
	c.execute("DROP TABLE IF EXISTS health")
	c.execute("""CREATE TABLE health(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetentertainment(c):
	c.execute("DROP TABLE IF EXISTS entertainment")
	c.execute("""CREATE TABLE entertainment(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetscience(c):
	c.execute("DROP TABLE IF EXISTS science")
	c.execute("""CREATE TABLE science(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetgeneral(c):
	c.execute("DROP TABLE IF EXISTS general")
	c.execute("""CREATE TABLE general(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetsports(c):
	c.execute("DROP TABLE IF EXISTS sports")
	c.execute("""CREATE TABLE sports(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resettechonology(c):
	c.execute("DROP TABLE IF EXISTS technology")
	c.execute("""CREATE TABLE technology(
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
		if (dateToday == lastHitApi):
			return False
	else:
		lastHitApi= dateToday
		return True
	lastHitApi= dateToday
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

def getnewscategory(c,category):
	c.execute("SELECT * FROM " + category)
	news = c.fetchall()
	return news

def iscategoryRecent(c,category):
	dateToday = date.today()
	if (getnewscategory(c,category) != []):
		news = getnewscategory(c,category)
		todayDate = news[0][0][0:10]
		if (todayDate == dateToday):
			return True
	return False

def setnews(c,news,category):
	if (category == "business"):
		resetbusiness(c)
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
				"INSERT INTO business VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
				)
	if (category == "science"):
		resetscience(c)
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
				"INSERT INTO science VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
				)
	if (category == "sports"):
		resetsports(c)
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
				"INSERT INTO sports VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
				)
	if (category == "general"):
		resetgeneral(c)
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
				"INSERT INTO general VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
				)
	if (category == "health"):
		resethealth(c)
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
				"INSERT INTO health VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
				)
	if (category == "technology"):
		resettechnology(c)
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
				"INSERT INTO technology VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
				)
	if (category == "entertainment"):
		resetentertainment(c)
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
				"INSERT INTO entertainment VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
				)

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
