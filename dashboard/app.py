from flask import Flask, render_template, redirect
import os
import json
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

if not firebase_admin._apps:

    firebase_credentials = json.loads(
        os.environ["FIREBASE_CREDENTIALS"]
    )

    cred = credentials.Certificate(firebase_credentials)

    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartdoorlock-99215-default-rtdb.firebaseio.com/"
    })

app = Flask(__name__)

if not firebase_admin._apps:
    cred = credentials.Certificate(
        "smartdoorlock-99215-firebase-adminsdk-fbsvc-fbb385588c.json"
    )

    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartdoorlock-99215-default-rtdb.firebaseio.com/"
    })


@app.route("/")
def home():
    visitor = db.reference("visitor").get()
    return render_template("index.html", visitor=visitor)


@app.route("/unlock")
def unlock():

    db.reference("door").set({
        "command": "UNLOCK",
        "status": "Unlocked by Owner"
    })

    return redirect("/")


@app.route("/reject")
def reject():

    db.reference("door").set({
        "command": "REJECT",
        "status": "Access Denied"
    })

    return redirect("/")



@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response



if __name__ == "__main__":
    app.run(debug=True)