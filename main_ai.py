import cv2
from deepface import DeepFace

print("====================================")
print(" SMART DOOR AI - VERSION 3 ")
print("====================================")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera not found!")
    exit()

print("Press SPACE to capture your face.")
print("Press Q to quit.")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    cv2.imshow("Smart Door AI", frame)

    key = cv2.waitKey(1)

    if key == ord(' '):

        cv2.imwrite("captured_face.jpg", frame)

        break

    if key == ord('q'):
        exit()

camera.release()
cv2.destroyAllWindows()

print("\nAnalyzing face...\n")

result = DeepFace.find(
    img_path="captured_face.jpg",
    db_path="authorized_faces",
    model_name="ArcFace",
    detector_backend="retinaface",
    enforce_detection=True
)

print(result)