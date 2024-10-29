import cv2
from deepface import DeepFace
import atexit
import serial
import time
import Controller as cnt






arduino = serial.Serial('/dev/cu.usbmodem1401', 9600)
def main():
    # OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    def cleanup():
        cnt.led_off()  # Ensure LED is turned off on exit
        arduino.close()  # Close serial communication

    # Register cleanup function to ensure LED is turned off on program exit
    atexit.register(cleanup)

    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        try:
            # Perform face analysis
            faces = DeepFace.analyze(frame, actions=['age'], enforce_detection=False)

            num_faces = len(faces)
            ClassIndex = []  # Initialize ClassIndex
            led_on = False  # Initialize LED state

            for idx, face in enumerate(faces):
                # Get face coordinates
                left = face['region']['x']
                top = face['region']['y']
                right = left + face['region']['w']
                bottom = top + face['region']['h']

                # Draw rectangle around face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Display the person number
                cv2.putText(frame, str(idx + 1), (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                # Get age estimation for each face
                age = face["age"]

                # Determine age category
                if age >= 23:
                    age_category = "Adult"
                    ClassIndex.append(0)
                else:
                    age_category = "Child"
                    ClassIndex.append(1)

                # Check if the detected age is correct
                if age <= 24:
                    led_on = True

                # Display age and category
                text = f"Age: {age}, Category: {age_category}"
                cv2.putText(frame, text, (10, 30 * (idx + 1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Turn LED on or off based on the detected age
            if led_on:
                cnt.led(ClassIndex)
                arduino.write(b'1')  # Send signal to Arduino
            else:
                cnt.led_off()
                arduino.write(b'0')  # Send signal to Arduino

            # Display message if only one person of age is detected
            if num_faces == 1 and faces[0]["age"] <= 25:
                cv2.putText(frame, "Only one person detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)

        except ValueError as ve:
            print("Error:", ve)
            age_category = "No face detected"
            cv2.putText(frame, age_category, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cnt.led_off()  # Ensure LED is turned off if an error occurs
            arduino.write(b'0')  # Send signal to Arduino

        # Display frame
        cv2.imshow('Face Age and Category Analysis', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
