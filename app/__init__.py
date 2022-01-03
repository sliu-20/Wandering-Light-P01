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
import random

MAIN_DB = "vacation.db"

# Creation of db file
db = sqlite3.connect(MAIN_DB)
c = db.cursor()

# Vacation Ideas table creation
c.execute("""
CREATE TABLE IF NOT EXISTS SAVED (
    USERID     INTEGER,
    COUNTRY    TEXT    ,
    FORECAST   TEXT    ,
    HOLIDAYS   TEXT    ,
    ACTIVITY   TEXT    ,
    BOOKS      TEXT
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

langs = []
regions = []
countries = []
capital = []
countriesCapital = dict()
countriesCode = dict()
tempData = dict()
tempErrorMessage = []
subjs = ["young_adult", "fantasy", "thriller", "literary_fiction", "science_fiction", "romance", "historical", "memoir", "narrative", "history"]

def api_store(): # accesses the apis and stores the data into the VACATIONDATA table
    db = sqlite3.connect(MAIN_DB)
    c = db.cursor()
    try:
        # the fields are what we are interested in accessing
        # if we want a list of names, capitals, languages, or regions, we can just access it from the table
        url = "https://restcountries.com/v2/all?fields=name,capital,alpha2Code,languages,region"
        data = urllib.request.urlopen(url)
        read_data = data.read()
        d_data = read_data.decode('utf-8')
        p_data = json.loads(d_data)
        # for country in p_data:
        #     country["languages"] = country["languages"][0]["name"]
        # print(p_data)
        for country in p_data:
            for lang in country["languages"]:
                if lang["name"] not in langs:
                    langs.append(lang["name"])
            if country["region"] not in regions:
                regions.append(country["region"])
            if country["name"] not in countries:
                countries.append(country["name"])
            if country['capital'] not in capital:
                capital.append(country["capital"])
            countriesCapital.update({country["name"] : country["capital"]})
            countriesCode.update({country["name"] : country["alpha2Code"]})
    except:
        country = country
    # db.commit()
    # db.close()

api_store()

pickfrom = []
def sortCountries(langList, regionList):
    url = "https://restcountries.com/v2/all?fields=name,capital,languages,region"
    data = urllib.request.urlopen(url)
    read_data = data.read()
    d_data = read_data.decode('utf-8')
    p_data = json.loads(d_data)
    if len(regionList) != 0 and len(langList) == 0:
        for country in p_data:
            if country['region'] in regionList:
                pickfrom.append(country['name'])
    elif len(regionList) == 0 and len(langList) != 0:
        for country in p_data:
            for lang in country['languages']:
                if lang['name'] in langList:
                    pickfrom.append(country['name'])
    else:
        for country in p_data:
            if country['region'] in regionList and country['languages'][0]['name'] in langList:
                pickfrom.append(country['name'])
    return pickfrom

def pickCountry(langList, regionList):
    try:
        if len(langList) == 0 and len(regionList) == 0:
            random_country = random.choices(population=countries, k=1)
            # [0] is necessary because random_country is a list with one string
            return random_country[0]
        else:
            pickfrom = sortCountries(langList, regionList)
            if pickfrom:
                random_country = random.choices(pickfrom, k=1)
                return random_country[0]
            else:
                return "There is no country available with the language and region choices you picked."
    except:
        return "An unknown error with the API occurred. Vacation Time apologizes."

def getForecast(capital):
    try:
        f = open("keys/key_api0.txt", "r")
        api_key = f.read()
        url = "https://api.weatherapi.com/v1/current.json?key=" + api_key + "&q=" + capital
        data = urllib.request.urlopen(url)
        read_data = data.read()
        d_data = read_data.decode('utf-8')
        p_data = json.loads(d_data)
        return "Temperature: " + str(p_data['current']['temp_c']) + " ºC (" \
                + str(p_data['current']['temp_f']) + " ºF)\nFeels like: " + str(p_data['current']['feelslike_c']) \
                + " ºC (" + str(p_data['current']['feelslike_f']) + " ºF)\nHumidity: " + str(p_data['current']['humidity'])
    except:
        return "An unknown error with the API occurred. Vacation Time apologizes."

def getHolidays(countrycode):
    try:
        f = open("keys/key_api1.txt", "r")
        api_key = f.read()
        url = "https://holidays.abstractapi.com/v1/?api_key=" + api_key + "&country=" + countrycode + "&year=2020"
        data = urllib.request.urlopen(url)
        read_data = data.read()
        d_data = read_data.decode('utf-8')
        p_data = json.loads(d_data)
        randomNumber = randint(0,(len(p_data)-1))
        display = ""
        tempData.update({"HOLIDAYS" : p_data[randomNumber]['name']})
        for i in range(len(p_data)):
            display += p_data[i]['name']
            if i < len(p_data) - 1:
                display += ", "
        return display
    except:
        return "An unknown error with the API occurred. Vacation Time apologizes."

def pickActivity(integer):
    try:
        url = "https://www.boredapi.com/api/activity?participants=" + integer
        data = urllib.request.urlopen(url)
        read_data = data.read()
        d_data = read_data.decode('utf-8')
        p_data = json.loads(d_data)
        if p_data['link'] != '':
            return p_data['activity'] + ". Learn more at: " + p_data['link']
        else:
            return p_data['activity']
    except:
        return "An unknown error with the API occurred. Vacation Time apologizes."

def pickBook(string):
    try:
        url = "http://openlibrary.org/subjects/" + string + ".json"
        data = urllib.request.urlopen(url)
        read_data = data.read()
        d_data = read_data.decode('utf-8')
        p_data = json.loads(d_data)
        randBook = randint(0, len(p_data['works'])-1)
        return "Try reading: " + p_data['works'][randBook]['title'] + " by " + p_data['works'][randBook]['authors'][0]['name']
    except:
        return "An unknown error with the API occurred. Vacation Time apologizes."

def isAlphanumerical(string):
    for char in string:
        o = ord(char)
        if not ((0x41 <= o <= 0x5A) or (0x61 <= o <= 0x7A) or (0x30 <= o <= 0x39)):
            return False;
    return True;

@app.route("/") # assign fxn to route for home page
def home_page():
    if 'username' in session:
        return render_template("homepage.html", user=session.get('username'))
    else:
        return render_template("index.html", user=session.get('username'))

@app.route("/login", methods=['GET', 'POST']) # assign fxn to route for login page
def login_page():
    if request.method == "POST":
        if 'username' in session:
            return render_template("login.html", user=session.get('username'), error = "Already logged in!")
        if 'username' in request.form and 'password' in request.form:
            db = sqlite3.connect(MAIN_DB)
            c = db.cursor()
            c.execute("""SELECT PASSWORD FROM USERS WHERE USERNAME = ?;""", (request.form['username'],))
            hash = c.fetchone()
            db.close()
            #print(request.form['password'])
            if (hash == None):
                return render_template("login.html", user=session.get('username'), error = "User does not exist.")
            else:
                if hash[0] == request.form['password']:
                    session['username'] = request.form['username']
                    return render_template("homepage.html", user=session.get('username'), error = "Logged in!")
                else:
                     return render_template("login.html", user=session.get('username'), error="Password is incorrect")
        else:
            return render_template("login.html", user=session.get('username'), error="An error occurred. Please try logging in again.")
    else:
        if len(tempErrorMessage) != 0:
            return render_template("login.html", user=session.get('username'), error = tempErrorMessage.pop(0))
        else:
            return render_template("login.html", user=session.get('username'))

@app.route("/register", methods=['GET', 'POST']) # assign fxn to route for register page
def register_page():
    if request.method == "POST":
        db = sqlite3.connect(MAIN_DB)
        c = db.cursor()
        c.execute("""SELECT USERNAME FROM USERS WHERE USERNAME = ?;""", (request.form['username'],))
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
                checkPassword = request.form['confirm-password']
                if password == checkPassword:
                    print(checkPassword)
                    c.execute("""INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?,?)""", (request.form['username'], password))
                    db.commit()
                    c.execute("""SELECT USERNAME FROM USERS WHERE USERNAME = ?;""", (request.form['username'],))
                    exists = c.fetchone()
                    db.close()
                    if (exists != None):
                        return render_template("login.html", user=session.get('username'), action="/login", name="Login", error="Signed up successfully!")
                    else:
                        return render_template("register.html", user=session.get('username'), error="An error occurred. Try signing up again.")
                else:
                    return render_template("register.html", user=session.get('username'), error="Passwords do not match.")
            else:
                db.close()
                return render_template("register.html", user=session.get('username'), error="Password must be between 8 and 50 characters long.")
        else:
            return render_template("register.html", user=session.get('username'), error="Username is taken. Try using a different one.")
    else:
        return render_template("register.html", user=session.get('username'))

# page for the user to input their preferences
@app.route("/input")
def input():
    if 'username' not in session:
        return redirect("/")
    else:
        return render_template("input.html", user=session.get('username'), languages=langs, regionlist=regions)

# page for a suggested vacation to be displayed after the user enters their preferences
@app.route("/choose", methods=['GET', 'POST'])
def suggest():
    if 'username' not in session:
        return redirect("/")
    else:
        # print(request.form['people'])
        # print(request.form.getlist('subjects'))
        # print(request.form.getlist('languages'))
        # print(request.form.getlist('regions'))
        # print(request.form.getlist('people'))
        user_party_size = request.form.getlist('people')
        user_subjs = request.form.getlist('subjects')
        user_langs = request.form.getlist('languages')
        user_regions = request.form.getlist('regions')

        action = ""
        if len(user_party_size) != 0:
            action = pickActivity(user_party_size[0])
        else:
            action = pickActivity("1")
        tempData.update({'ACTIVITY' : action})

        readBook = ""
        if len(user_subjs) != 0:
            rand_subj = random.choices(user_subjs, k=1)
            readBook = pickBook(rand_subj[0])
        else:
            rand_subj = random.choices(subjs, k=1)
            readBook = pickBook(rand_subj[0])
        tempData.update({'BOOKS' : readBook})

        countrySelection = pickCountry(user_langs, user_regions)
        tempData.update({"COUNTRY" : countrySelection})

        # print(countrySelection)
        displayHolidays = getHolidays(countriesCode.get(countrySelection))
        try:
            cap = countriesCapital.get(countrySelection)
            displayForecast = getForecast(countriesCapital.get(countrySelection))
            tempData.update({"FORECAST" : displayForecast})
            return render_template("suggestedvacation.html", user=session.get('username'), activity = action, book = readBook, country = countrySelection, capital = cap, forecast = displayForecast, holidays = displayHolidays)
        except:
            displayForecast = "No location to obtain forecast from."
            tempData.update({"FORECAST" : displayForecast})
            return render_template("suggestedvacation.html", user=session.get('username'), activity = action, book = readBook, country = countrySelection, forecast = displayForecast, holidays = displayHolidays)


# page for a randomized vacation idea
@app.route("/randomize", methods=['GET', 'POST'])
def randomize():
    action = pickActivity("1")
    tempData.update({'ACTIVITY' : action})
    rand_subj = random.choices(subjs, k=1)
    readBook = pickBook(rand_subj[0])
    tempData.update({'BOOKS' : readBook})
    countrySelection = pickCountry([],[])
    tempData.update({"COUNTRY" : countrySelection})
    displayHolidays = getHolidays(countriesCode.get(countrySelection))
    # print(countriesCode)
    try:
        cap = countriesCapital.get(countrySelection)
        displayForecast = getForecast(countriesCapital.get(countrySelection))
        tempData.update({"FORECAST" : displayForecast})
        return render_template("suggestedvacation.html", user=session.get('username'), activity = action, book = readBook, country = countrySelection, capital = cap, forecast = displayForecast, holidays = displayHolidays)
    except:
        displayForecast = "No location to obtain forecast from."
        tempData.update({"FORECAST" : displayForecast})
        return render_template("suggestedvacation.html", user=session.get('username'), activity = action, book = readBook, country = countrySelection, forecast = displayForecast, holidays = displayHolidays)

# page for viewing all saved vacations
@app.route("/view", methods=['GET', 'POST'])
def view():
    if 'username' not in session:
        tempErrorMessage.append("You must be logged in to view and save these ideas.")
        return redirect("/login")
    else:
        if len(tempData) != 0:
            if request.method == "POST":
                db = sqlite3.connect(MAIN_DB)
                c = db.cursor()
                countrySelection = tempData.get("COUNTRY")
                readBook = tempData.get("BOOKS")
                action = tempData.get("ACTIVITY")
                forecast = tempData.get("FORECAST")
                holidays = tempData.get("HOLIDAYS")
                c.execute("""INSERT INTO SAVED (COUNTRY, BOOKS, ACTIVITY, FORECAST, HOLIDAYS) VALUES (?, ?, ?, ?, ?);""", ((countrySelection, readBook, action, forecast, holidays)))
                c.execute("""SELECT * FROM SAVED;""")
                saved = c.fetchall()
                # print(saved)
                db.commit()
                db.close()
                tempData.clear()
                return render_template("view.html", vacations = saved, user=session.get('username'))
        db = sqlite3.connect(MAIN_DB)
        c = db.cursor()
        c.execute("""SELECT * FROM SAVED;""")
        saved = c.fetchall()
        # print(saved)
        db.commit()
        db.close()
        return render_template("view.html", vacations = saved, user=session.get('username'))

@app.route("/logout")
def logout():
    session.pop('username', default=None)
    return redirect("/")

if __name__ == "__main__": # true if this file is NOT imported
    app.debug = True       # enable auto-reload upon code change
    app.run()
