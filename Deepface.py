import cv2
import os
import time
from deepface import DeepFace

# OpenCV video capture
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

timer_started = False
start_time = 0
countdown_time = 5  # countdown time in seconds
screenshot_taken = False
child_detected_message = False  # Flag to show the child detected message

# Specify the directory for storing screenshots
screenshot_dir = "/Users/saran/Desktop/Detected"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Reduce the frame size only for analysis
resize_factor = 0.5  # Analyze smaller frames for speed

frame_skip = 10  # Only analyze every 10th frame
frame_count = 0

# Text to show permanently on the top left corner
permanent_text = "Face Age and Category Analysis"

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Always display the permanent text
    cv2.putText(frame, permanent_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Only process every n-th frame for DeepFace analysis
    if frame_count % frame_skip == 0:
        # Resize the frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

        try:
            # Perform face analysis on the smaller frame
            faces = DeepFace.analyze(small_frame, actions=['age'], enforce_detection=False)
        except Exception as e:
            print(f"DeepFace analysis error: {e}")
            faces = []

        num_faces = len(faces)
        child_detected = False

        for idx, face in enumerate(faces):
            # Get face coordinates (adjust for resized frame)
            left = int(face['region']['x'] / resize_factor)
            top = int(face['region']['y'] / resize_factor)
            right = left + int(face['region']['w'] / resize_factor)
            bottom = top + int(face['region']['h'] / resize_factor)

            # Draw rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Display the person number
            cv2.putText(frame, str(idx + 1), (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Get age estimation for each face
            age = face["age"]

            # Determine age category
            if age >= 23:
                age_category = "Adult"
            else:
                age_category = "Child"

            # Check if a child (age < 30) is detected
            if age < 30:
                child_detected = True

            # Display age and category below permanent text
            text = f"Age: {age}, Category: {age_category}"
            cv2.putText(frame, text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if child_detected and num_faces == 1:
            if not timer_started:
                timer_started = True
                start_time = time.time()
                screenshot_taken = False  # Reset the screenshot flag when timer starts
            elapsed_time = time.time() - start_time
            remaining_time = max(0, countdown_time - elapsed_time)
            countdown_text = f"Timer: {int(remaining_time)}"
            cv2.putText(frame, countdown_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)

            if remaining_time == 0 and not screenshot_taken:
                screenshot_filename = os.path.join(screenshot_dir, f"child_screenshot_{int(time.time())}.png")
                cv2.imwrite(screenshot_filename, frame)
                screenshot_taken = True
                child_detected_message = True  # Set the flag to show the message
        else:
            timer_started = False
            child_detected_message = False  # Reset the flag if conditions change

        if child_detected_message:
            cv2.putText(frame, "Child detected and screenshot taken", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

    # Display the current frame
    cv2.imshow('Face Age and Category Analysis', frame)

    # Increment the frame counter
    frame_count += 1

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
