from datetime import datetime
from cloud.firebase import database


def update_visitor(image_url):

    visitor = {

        "image_url": image_url,

        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

        "status": "Waiting"

    }

    database.child("visitor").set(visitor)

    print("✅ Firebase Updated")