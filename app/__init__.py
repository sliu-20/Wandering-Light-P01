# Wandering Lights | Sophie Liu (Quacky), Ryan Wang (Jack), Jonathan Wu (Loki), Roshani Shrestha (Pete)
# SoftDev
# P01: ArRESTed Development
# 2021-12-10
# time spent: ??

import os
import sqlite3
import json
import ssl
import urllib.request
from random import randint
from flask import Flask, render_template, request, session, redirect

MAIN_DB = "vacation.db"

# Creation of db file
db = sqlite3.connect(MAIN_DB)
c = db.cursor()

# Vacation Ideas table creation
c.execute("""
CREATE TABLE IF NOT EXISTS SAVED (
    USERID     INTEGER,
    COUNTRY    TEXT    NOT NULL,
    FORECAST   TEXT    NOT NULL,
    HOLIDAYS   TEXT    NOT NULL,
    ACTIVITY   TEXT    NOT NULL,
    BOOKS      TEXT    NOT NULL,
    MEDIA      TEXT    NOT NULL
);""")

# Storing data table creation
c.execute("""
CREATE TABLE IF NOT EXISTS VACATIONDATA (
    COUNTRY    TEXT    NOT NULL,
    FORECAST   TEXT    NOT NULL,
    HOLIDAYS   TEXT    NOT NULL,
    ACTIVITY   TEXT    NOT NULL,
    BOOKS      TEXT    NOT NULL,
    MEDIA      TEXT    NOT NULL
);""")

# User/password table creation
c.execute("""
CREATE TABLE IF NOT EXISTS USERS (
    USERID       INTEGER PRIMARY KEY,
    USERNAME     TEXT    NOT NULL,
    PASSWORD     TEXT    NOT NULL
);""")

# Closes and commits edits of database files
db.commit()
db.close()

app = Flask(__name__) # create instance of class Flask
app.secret_key = os.urandom(32) # generates a string containing random characters

ssl._create_default_https_context = ssl._create_unverified_context # bypasses the 'certificate verify failed: certificate has expired' error on machines.

def api_store(): # accesses the apis and stores the data into the VACATIONDATA table
    db = sqlite3.connect(MAIN_DB)
    c = db.cursor()
    url = "https://restcountries.com/v2/all?fields=name,capital"
    data = urllib.request.urlopen(url)
    read_data = data.read()
    d_data = read_data.decode('utf-8')
    p_data = json.loads(d_data)

    # c.execute("""INSERT INTO VACATIONDATA (COUNTRY) VALUES();""", p_data[0])
    # db.commit()
    # db.close()

def isAlphanumerical(string):
    for char in string:
        l = ord(char)
        if not ((0x41 <= o <= 0x5A) or (0x61 <= o <= 0x7A) or (0x30 <= o <= 0x39)):
            return False;
    return True;

@app.route("/") # assign fxn to route for home page
def home_page():
    api_store()
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST']) # assign fxn to route for login page
def login_page():
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST']) # assign fxn to route for register page
def register_page():
    if request.method == "POST":
        db = sqlite3.connect(MAIN_DB)
        c = db.cursor()
        c.execute("""SELECT UESERNAME FROM USERS WHERE USERNAME = ?;""", (request.form['username'],))
        exists = c.fetchone()
        if (exists == None):
            username = (request.form['username']).encode('utf-8')
            if isAlphanumerical(username.decode('utf-8')) ==  None:
                db.close()
                return render_template("register.html", user=session.get('username'), error="Username can only contain alphanumeric characters and underscores.")
            if len(username) < 5 or len(username) > 15:
                db.close()
                return render_template("register.html", user=session.get('username'), error="Username must be between 5 and 15 characters long.")
            password = request.form['password']
            if ' ' in list(password) or '\\' in list(password):
                db.close()
                return render_template("register.html", user=session.get('username'), error="Passwords cannot contain spaces or backslashes.")
            password = str(password)
            if len(password) > 7 and len(password) <= 50:
                c.execute("""INSERT INTO USERS (USERNAME, HASH) VALUES (?,?)""", request.form['username'], password,)
                db.commit()
                c.execute("""SELECT USERNAME FROM USERS WHERE USERNAME = ?;"""), (request.form['username'],)
                exists = c.fetchone()
                db.close()
                if (exists != None):
                    return render_template("login.html", user=session.get('username'), error="Signed up successfully!")
                else:
                    return render_template("login.html", user=session.get('username'), error="An error occurred. Try signing up again.")
            else:
                db.close()
                return render_template("login.html", user=session.get('username'), error="Password must be between 8 and 50 characters long.")
        else:
            return render_template("login.html", user=session.get('username'), error="Some error occurred. Please try signing up again.")
    else:
        return render_template("login.html", user=session.get('username'))

if __name__ == "__main__": # true if this file is NOT imported
    app.debug = True       # enable auto-reload upon code change
    app.run()
