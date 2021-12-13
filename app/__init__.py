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
from flask import Flask, render_template, request, session, redirect

MAIN_DB = "vacation.db"

# Creation of db file
db = sqlite3.connect(MAIN_DB)
c = db.cursor()

# Vacation Ideas table creation
c.execute("""
CREATE TABLE IF NOT EXISTS VACATIONDATA (
    USERID     INTEGER,
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

app = Flask(__name__) #create instance of class Flask
app.secret_key = os.urandom(32)

def api_store(): # accesses the apis and stores the data into the VACATIONDATA table
    db = sqlite3.connect(MAIN_DB)
    c = db.cursor()
    url = "https://restcountries.com/v2/all?fields=name,capital"
    data = urllib.request.urlopen(url)
    read_data = data.read()
    d_data = read_data.decode('utf-8')
    p_data = json.loads(d_data)
    c.execute("""INSERT INTO VACATIONDATA (COUNTRY) VALUES (?);""", p_data)

@app.route("/") # assign fxn to route
def home_page():
    api_store()
    return render_template("index.html")

if __name__ == "__main__": # true if this file is NOT imported
    app.debug = True       # enable auto-reload upon code change
    app.run()
