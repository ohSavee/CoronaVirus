import tkinter as tk
import requests
import datetime
import mysql.connector


#Get data from api
def getCovidData():
    api = "https://disease.sh/v3/covid-19/all"
    json_data = requests.get(api).json()
    total_cases = str(json_data['cases'])
    total_deaths = str(json_data['deaths'])
    today_cases = str(json_data['todayCases'])
    today_deaths = str(json_data['todayDeaths'])
    today_recovered = str(json_data['todayRecovered'])
    updated_at = json_data['updated']
    date = datetime.datetime.fromtimestamp(updated_at/1e3)

    label.config(text="Today Cases: "+today_cases
                 + "\nToday Deaths: "+today_deaths
                 + "\nToday Recovered: "+today_recovered
                 + "\n\nTotal Cases: " + total_cases
                 + "\nTotal Deaths: " + total_deaths)

    label2.config(text=date)

    return date, today_cases, today_deaths, today_recovered, total_cases, total_deaths

#store in database on button click
def storeInDatabase(date, today_cases, today_deaths, today_recovered, total_cases, total_deaths):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="CoronaVirusSaved"
        )

        cursor = db.cursor()
        cursor.execute(f"INSERT INTO saves (date, today_cases, today_deaths, today_recovered, total_cases, total_deaths) VALUES ('" + date + "', '" + today_cases + "', '" + today_deaths + "', '" + today_recovered + "', '" + total_cases + "', '" + total_deaths + "')")
    except Exception as ex:
        return None

#create box app
canvas = tk.Tk()
canvas.geometry('400x400')
canvas.title("Corona Tracker")

f = ("poppins", 15, "bold")

#buttons
button = tk.Button(canvas, font=f, text="Load", command=getCovidData)
button.pack(pady=20)

button = tk.Button(canvas, font=f, text="Save", command=storeInDatabase)
button.pack(pady=20)

#labels
label = tk.Label(canvas, font=f)
label.pack(pady=20)

label2 = tk.Label(canvas, font=8)
label2.pack()
getCovidData()

canvas.mainloop()
