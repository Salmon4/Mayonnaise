import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

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
				content text
				);""")

#new day: reset topnews table
def resetnews(c):
	c.execute("DROP TABLE IF EXISTS topnews")
	c.execute("""CREATE TABLE topnews(
				datetime text,
				title text,
				author text,
				url text,
				imageURL text,
				content text
				);""")

def settopnews(news):
	for article in news:
		c.execute("INSERT INTO topnews VALUES ")

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
