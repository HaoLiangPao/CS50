import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    #POST
    if request.method == "POST":
        # A new delete feature
        delete = request.form.get("delete")
        if delete:
            # Get the user input infomation
            deleteName = request.form.get("deleteName")
            deleteMonth = request.form.get("deleteMonth")
            deleteDay = request.form.get("deleteDay")
            # remove the specified record from the database
            db.execute("DELETE FROM birthdays WHERE name=? AND month=? AND day=?", deleteName, deleteMonth, deleteDay)
        else:
            # Get the user input infomation
            name = request.form.get("name")
            month = request.form.get("month")
            day = request.form.get("day")
            if name != '' and month and day:
                # Add the user's entry into the database
                db.execute("INSERT INTO birthdays (name, month, day) VALUES (?,?,?)", name, month, day)
        # Redirect to homepage to see newly made changes
        return redirect("/")
    #GET
    else:

        # Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays");

        return render_template("index.html", birthdays = birthdays);


