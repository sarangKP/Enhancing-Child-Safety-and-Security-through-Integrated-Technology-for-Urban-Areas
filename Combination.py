import cv2
from deepface import DeepFace

# Load the person detection model
config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'frozen_inference_graph.pb'

model = cv2.dnn_DetectionModel(frozen_model, config_file)

classLabels = []
file_name = "Labels.txt"
with open(file_name, 'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

model.setInputSize(320, 320)  # Because inside Configuration file that is the size
model.setInputScale(1.0/127.5)     # 255/2=127.5
model.setInputMean(127.5)  # mobilenet=> [-1,-1]
model.setInputSwapRB(True)

def main():
    # OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + '/Users/saran/PycharmProjects/cvZone/haarcascade_frontalface_default.xml')

    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        # Perform face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            try:
                # Perform face analysis
                results = DeepFace.analyze(frame[y:y+h, x:x+w], actions=['age'], enforce_detection=False)

                for result in results:
                    # Get age estimation for each face
                    age = result["age"]

                    # Determine age category
                    if age >= 18:
                        age_category = "Adult"
                    else:
                        age_category = "Child"

                    # Display age and category
                    text = f"Age: {age}, Category: {age_category}"
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

            except ValueError as ve:
                print("Error:", ve)

        # Perform person detection
        ClassIndex, confidence, bbox = model.detect(frame, confThreshold=0.5)

        if len(ClassIndex) != 0:
            for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
                if ClassInd <= 4:
                    cv2.rectangle(frame, boxes, (255, 0, 0), 2)
                    cv2.putText(frame, classLabels[ClassInd - 1], (boxes[0] + 10, boxes[1] + 40), cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=3, color=(0, 0, 0), thickness=3)

        # Display frame
        cv2.imshow('Face Age and Person Detection Analysis', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
