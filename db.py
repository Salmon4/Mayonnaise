import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="mayonnaise.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#==========================================================
def setup():
	c.execute("CREATE TABLE IF NOT EXISTS users")
	c.execute("CREATE TABLE IF NOT EXISTS topnews")
	
#new day: reset topnews table
def resetnews():
	c.execute("DROP TABLE IF EXISTS topnews")
	c.execute("CREATE TABLE topnews")

#deletes all existing tables
def reset():
    #LATER: create loop to delete every single user table
    c.execute("SELECT COUNT(1)")
    for i in range(users.
    
    #delete users and topnews table
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS topnews")
    
#==========================================================
def 
    


