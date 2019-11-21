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
	c.execute("CREATE TABLE topnews")

#deletes all existing tables
def reset(c):
    #LATER: create loop to delete every single user table
    c.execute("SELECT COUNT(1)")

    #delete users and topnews table
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS topnews")

#==========================================================
