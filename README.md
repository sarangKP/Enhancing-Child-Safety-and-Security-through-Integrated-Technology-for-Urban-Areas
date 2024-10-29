# Enhancing-Child-Safety-and-Security-through-Integrated-Technology-for-Urban-Areas

A real-time child safety alert system designed to enhance surveillance capabilities and proactively identify potential child abduction scenarios. This system leverages machine learning and embedded systems to recognize unattended children, alert caregivers, and assist authorities in rapid response. Integrated with CCTV infrastructure, it utilizes advanced image processing and real-time data processing to enhance child safety and mitigate abduction risks.

## 🚀 Features

1. Real-time Monitoring: Processes live video feeds from CCTV systems to monitor children in public spaces.
2. Image Recognition with CNNs: Uses Convolutional Neural Networks (CNNs) to accurately identify and differentiate children from surrounding elements.
3. Haar-Cascade Classifiers: Implements Haar-Cascade classifiers for efficient object detection and tracking of children.
4. Automated Alerts: Notifies caregivers and authorities when a potential abduction risk is detected.
5. Data Management: Matches missing and found children through dataset management, sending alerts to guardians if a match is confirmed.
6. Embedded Systems Integration: Optimized for embedded environments for seamless deployment and real-time response.

## 📋 Requirements

1. Python 3.x
2. OpenCV
3. TensorFlow/Keras (for CNN models)
4. NumPy
5. Embedded system compatibility (Arduino UNO)


## 💡 Key Technologies

- Machine Learning: Convolutional Neural Networks (CNNs) for accurate image recognition.
-  OpenCV: Real-time image and video processing.
-   Haar-Cascade Classifiers: Object detection for identifying children in crowded areas.
-    bedded Systems: Integrated into CCTV setups with microcontrollers like Arduino UNO for real-time response.
6. Alert Management: Automated alerts through integrated channels for caregivers and authorities.

## 🛠 Embedded System Integration

The project incorporates an Arduino Uno connected to an LED display to mimic an alert system. When a child is detected, the message "Child Detected" is displayed on the LED, providing a visual alert. The integration between the Arduino and the Python code running on the laptop is facilitated by the Firmata library, allowing for seamless communication and control of the Arduino's GPIO pins.

### Setup Instructions for Arduino
1. Connect the LED Display: Wire the LED display to the Arduino Uno according to the provided schematic.
2. Upload Firmata Firmware:
- Open the Arduino IDE.
- Navigate to File > Examples > Firmata > StandardFirmata.
- Upload the StandardFirmata sketch to the Arduino Uno.
3. Run the Python Code: Ensure the Firmata library is installed in your Python environment, and execute the main script to start monitoring for child detection.


## 📚 References

- [DeepFace: A Unified Face Recognition Library](https://github.com/serengil/deepface) - A powerful library for face analysis and recognition, used for building the face detection component of this project.

