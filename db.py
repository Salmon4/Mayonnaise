import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE="mayonnaise.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#==========================================================
def reset():
    #remove tables to avoid dupliacte error
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("SELECT COUNT(1)")
    for i in range(users.
    c.execute("DROP TABLE IF EXISTS students")
    c.execute("DROP TABLE IF EXISTS stu_avg")
