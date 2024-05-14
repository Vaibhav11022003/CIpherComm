import sqlite3
import hashlib

FORMAT='utf-8'

conn=sqlite3.connect('userdata.db')
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata(
            id INTEGER PRIMARY KEY,
            username VARCHAR(265) NOT NULL,
            password VARCHAR(265) NOT NULL,
            status BOOLEAN NOT NULL
)
            """)

username1,password1='vaibhav',hashlib.sha256("Vaibhav@@3737".encode(FORMAT)).hexdigest()
username2,password2='mayank',hashlib.sha256("Mayank@@3737".encode(FORMAT)).hexdigest()
username3,password3='khushi',hashlib.sha256("Khushi@@3737".encode(FORMAT)).hexdigest()
username4,password4='vasu',hashlib.sha256("vasu".encode(FORMAT)).hexdigest()
username5,password5='uday',hashlib.sha256("uday".encode(FORMAT)).hexdigest()


cur.execute("INSERT INTO userdata (username,password,status) VALUES (?, ?,?)",(username1,password1,True))
cur.execute("INSERT INTO userdata (username,password,status) VALUES (?, ?,?)",(username2,password2,True))
cur.execute("INSERT INTO userdata (username,password,status) VALUES (?, ?,?)",(username3,password3,True))
cur.execute("INSERT INTO userdata (username,password,status) VALUES (?, ?,?)",(username4,password4,True))
cur.execute("INSERT INTO userdata (username,password,status) VALUES (?, ?,?)",(username5,password5,True))

cur.execute("""
CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY,
            filename VARCHAR(265) NOT NULL unique
)
            """)
filename1='applogo.png'
filename2='ayush.pdf'
filename3='nnd lab file.pdf'
filename4='dynamic routing rip.docx'
filename5='download.py'
cur.execute('INSERT INTO files (filename) VALUES (?)',(filename1,))
cur.execute('INSERT INTO files (filename) VALUES (?)',(filename2,))
cur.execute('INSERT INTO files (filename) VALUES (?)',(filename3,))
cur.execute('INSERT INTO files (filename) VALUES (?)',(filename4,))
cur.execute('INSERT INTO files (filename) VALUES (?)',(filename5,))
conn.commit()

print(2)