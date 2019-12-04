import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
from datetime import date #for checking recency of topnews table
lastHitApi = ""
#create 2 general tables
def setup(c):
	#this keeps track of all the accounts created
	c.execute("""CREATE TABLE IF NOT EXISTS users(
				userID integer PRIMARY KEY,
				username text,
				password text
				);""")
	#table with all of the news articles
	c.execute("""CREATE TABLE IF NOT EXISTS topnews(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")
	#table with hockey stuff
	c.execute("""CREATE TABLE IF NOT EXISTS nhl_scores(
				datetime text,
				gameID integer,
				home text,
				away text,
				home_score integer,
				away_score integer,
				status text
				);""")
	#table with basketball stuff
	c.execute("""CREATE TABLE IF NOT EXISTS nba_scores(
				datetime text,
				gameID integer,
				home text,
				away text,
				home_score integer,
				away_score integer,
				status text
				);""")
	resetbusiness(c)
	resetnews(c)
	resethealth(c)
	resetentertainment(c)
	resetscience(c)
	resetgeneral(c)
	resetsports(c)
	resettechnology(c)

def gettopnews(c):#gets all articles
	c.execute("SELECT * FROM topnews")
	news = c.fetchall()
	return news

#new day: reset topnews table

def resetnews(c):#resets news table to a blank state
	c.execute("DROP TABLE IF EXISTS topnews")
	c.execute("""CREATE TABLE topnews(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetbusiness(c): #resets business news articles table
	c.execute("DROP TABLE IF EXISTS business")
	c.execute("""CREATE TABLE business(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resethealth(c): #resets health news articles table
	c.execute("DROP TABLE IF EXISTS health")
	c.execute("""CREATE TABLE health(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetentertainment(c): #resets entertainment news articles table
	c.execute("DROP TABLE IF EXISTS entertainment")
	c.execute("""CREATE TABLE entertainment(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetscience(c):  #resets science news article table
	c.execute("DROP TABLE IF EXISTS science")
	c.execute("""CREATE TABLE science(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetgeneral(c): #resets general news article table
	c.execute("DROP TABLE IF EXISTS general")
	c.execute("""CREATE TABLE general(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resetsports(c): #resets sport news article table
	c.execute("DROP TABLE IF EXISTS sports")
	c.execute("""CREATE TABLE sports(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def resettechnology(c): #resets technology news article table
	c.execute("DROP TABLE IF EXISTS technology")
	c.execute("""CREATE TABLE technology(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				description text
				);""")

def checkRecency(c): #checks if the news article in the database are up to date
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


def settopnews(c,news): #updates news article table to the latest one
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
			image = "https://cdn.britannica.com/25/93825-050-D1300547/collection-newspapers.jpg"
		if (author == None):
			author = "N/A"
		c.execute(
		"INSERT INTO topnews VALUES(?,?,?,?,?,?)",(datetime,title,author,url,image,description,)
		)

def getnewscategory(c,category): #gets all news article categories into a dict
	c.execute("SELECT * FROM " + category)
	news = c.fetchall()
	return news

def iscategoryRecent(c,category): #checks if the category of news is up to date
	dateToday = date.today()
	if (getnewscategory(c,category) != []):
		news = getnewscategory(c,category)
		todayDate = news[0][0][0:10]
		if (todayDate == dateToday):
			return True
	return False

def setnews(c,news,category): #if category of news isn't up to date, it will update the inputted category
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
def newUserTable(c, username): #creates a table for the new user when the user creates an account
	c.execute("CREATE TABLE IF NOT EXISTS "+username+" (area text, preference text)")
	addUserPref(c, username, "base_currency", "USD")
	addUserPref(c, username, "location", "2459115")

def addUserPref(c, username, pref_area, pref): #addes a row with the user's preference in the preference area into the user's table
	c.execute("INSERT INTO "+username+" VALUES('"+pref_area+"', '"+pref+"')")

def getUserPrefs(c, username, pref_area): #gets all rows of the specified user with the matching preference area
	c.execute("SELECT preference FROM "+username+" WHERE area = ?", (pref_area, ))
	return c.fetchall()

def updatePref(c , username, pref_area, pref): #updates prefence row of specified area with the new preference of the user
	c.execute("UPDATE "+username+" SET preference = '"+pref+"' WHERE area = ?", (pref_area,))

def removePref(c,username,pref):
	c.execute("DELETE FROM " +username+ " WHERE preference = ?",(pref,))
