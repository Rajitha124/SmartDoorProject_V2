import cv2
from insightface.app import FaceAnalysis

print("====================================")
print(" SMART DOOR AI VERSION ")
print("====================================")

print("\nLoading AI Model...")

app = FaceAnalysis(name="buffalo_s")
app.prepare(
    ctx_id=-1,
    det_size=(320, 320)
)

print("✅ AI Model Loaded")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera not found")
    exit()

print("✅ Camera Started")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    faces = app.get(frame)

    for face in faces:

        x1, y1, x2, y2 = face.bbox.astype(int)

        cv2.rectangle(frame,
                      (x1, y1),
                      (x2, y2),
                      (0,255,0),
                      2)

    cv2.imshow("Smart Door AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()