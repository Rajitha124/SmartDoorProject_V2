import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from config import FIREBASE_JSON

# Prevent multiple initialization
if not firebase_admin._apps:

    cred = credentials.Certificate(FIREBASE_JSON)

    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://smartdoorlock-99215-default-rtdb.firebaseio.com/"
    })

# Database reference
database = db.reference("/")