import cv2
import face_recognition
import os
import warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
warnings.filterwarnings("ignore")

from deepface import DeepFace

import time
from cloud.upload_image import upload_image
from cloud.update_database import update_visitor
from firebase_admin import db


print("====================================")
print(" SMART DOOR LOCK SYSTEM - VERSION 2 ")
print("====================================")
print()

print("Door Status : 🔒 LOCKED")

db.reference("door").set({
    "command": "LOCK",
    "status": "Locked"
})

print()

print("Starting Camera...")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera not found!")
    exit()

print("✅ Camera Started")
print("Looking for a face...")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)

    cv2.imshow("Smart Door", frame)

    # If exactly one face is detected, capture automatically
    if len(face_locations) == 1:

        cv2.imwrite("captured_face.jpg", frame)

        print("📷 Face Captured!")

        break

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

print("Camera Closed")

print("\n🤖 AI Recognizing Face...")

result = DeepFace.find(
    img_path="captured_face.jpg",
    db_path="authorized_faces",
    model_name="ArcFace",
    detector_backend="retinaface",
    enforce_detection=True,
    silent=True
)

if len(result) > 0 and len(result[0]) > 0:

    identity = result[0].iloc[0]["identity"]

    name = os.path.basename(os.path.dirname(identity))

else:

    name = "Unknown"

if name != "Unknown":

    print(f"\n✅ Welcome {name}")

    print("\n🔓 Door Status : UNLOCKED")

    print("\nDoor will lock in:")

    for i in range(10,0,-1):

        print(i)

        time.sleep(1)

    print("\n🔒 Door Status : LOCKED")

    print("\n✅ Program Finished")

    exit()

else:

    print("\n❌ Unknown Visitor")

    print("\n📷 Capturing Visitor...")

    image_path = "captured_face.jpg"

    print("☁ Uploading Image to Cloudinary...")

    image_url = upload_image(image_path)

    if image_url:

        print("✅ Upload Successful")

        print("📡 Updating Firebase...")

        update_visitor(image_url)

        print("\nWaiting 15 seconds for Owner...")

        approved = False





        approved = False
        rejected = False

        for i in range(15,0,-1):

            print(i)

            door = db.reference("door").get()

            if door:

                command = door.get("command")

                if command == "UNLOCK":

                    approved = True
                    break

                elif command == "REJECT":

                    rejected = True
                    break

            time.sleep(1)





        if approved:

            print("\n✅ Owner Approved")

            print("🔓 Door Status : UNLOCKED")

            print("\nDoor will lock in:")

            for i in range(10,0,-1):

                print(i)

                time.sleep(1)

            print("\n🔒 Door Status : LOCKED")

            db.reference("door").set({
                "command": "LOCK",
                "status": "Locked"
            })

        elif rejected:

            print("\n❌ Owner Rejected")

            print("🔒 Door Remains LOCKED")

        else:

            print("\n⌛ No Response From Owner")

            print("🔒 Door Remains LOCKED")

    print("\n✅ Program Finished")