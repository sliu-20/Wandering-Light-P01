# Wandering Lights | Sophie Liu (Quacky), Ryan Wang (Jack), Jonathan Wu (Loki), Roshani Shrestha (Pete)
# SoftDev
# P01: ArRESTed Development
# 2021-12-10
# time spent: ??

import os
import sqlite3
from flask import Flask, render_template, request, session, redirect

MAIN_DB = "vacation.db"

# Creation of db file
db = sqlite3.connect(MAIN_DB)
c = db.cursor()

# Vacation Ideas table creation
c.execute("""
CREATE TABLE IF NOT EXISTS BLOGS (
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

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
