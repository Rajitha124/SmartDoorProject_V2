import cv2
import face_recognition
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

print("\nRecognizing Face...")

image = face_recognition.load_image_file("captured_face.jpg")

encodings = face_recognition.face_encodings(image)

if len(encodings) == 0:
    print("❌ No face found.")
    exit()

captured_encoding = encodings[0]

print("✅ Face Encoding Generated")


import os

known_encodings = []
known_names = []

for person in os.listdir("authorized_faces"):

    person_folder = os.path.join("authorized_faces", person)

    if os.path.isdir(person_folder):

        for image_name in os.listdir(person_folder):

            image_path = os.path.join(person_folder, image_name)

            known_image = face_recognition.load_image_file(image_path)

            face_encoding = face_recognition.face_encodings(known_image)

            if len(face_encoding) > 0:

                known_encodings.append(face_encoding[0])

                known_names.append(person)

print(f"Loaded {len(known_names)} authorized faces.")


distances = face_recognition.face_distance(
    known_encodings,
    captured_encoding
)

best_match = distances.argmin()
best_distance = distances[best_match]



if best_distance < 0.40:

    print(f"\n✅ Welcome {known_names[best_match]}")

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