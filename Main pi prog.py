import cv2
import pytesseract
import pyttsx3
import serial
import time
import re

# Initialize text-to-speech engine
engine = pyttsx3.init()
# Initialize serial communication (Change port if needed)
ser = serial.Serial('COM4', 9600, timeout=1) 
# Initialize camera
cam = cv2.VideoCapture(0)  # 0 is the default camera

# Function to read distance from serial

def get_distance():

    if ser.in_waiting > 0:

        try:
            # Read the raw data from the serial port
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Raw data from sensor: {data}")  # Debugging line

            

            # Split the data by '*' and filter out empty strings
            parts = data.split('*')
            distances = []

            # Process each part
            for part in parts:
                # Remove non-numeric characters (e.g., '#') and check if it's a valid number
                clean_part = re.sub(r'\D', '', part)  # Remove non-digit characters
                if clean_part.isdigit():
                    distances.append(int(clean_part))  # Add valid distance to the list

            # If we found any valid distances, return the first one

            if distances:
                return distances[0]
            else:
                print("No valid distance found after cleaning.")
        except ValueError:
            print("Error: Could not convert data to integer.")
    else:
        print("No data in serial buffer.")

    return None  # Return None if no valid distance is found





# Function to extract text from a live camera frame

def extract_text_from_frame():
    ret, frame = cam.read()
    if not ret:
        print("Error: Unable to capture frame.")
        return ""

    text = pytesseract.image_to_string(frame)
    return text.replace("\x00", "").strip()  # Remove null bytes

# Function to convert text to speech
def speak(text):
    if text:
        engine.say(text)
        engine.runAndWait()

# Main loop
while True:
    distance = get_distance()
    if distance is not None:
        print(f"Distance: {distance} cm")

        if distance < 30:

            print("Obstacle ahead!")
            speak("Obstacle ahead")
        else:
            text = extract_text_from_frame()
            if text:
                print("Extracted Text:", text)
                speak(text)
            else:
                print("No text detected.")

    

    else:
        print("Waiting for distance data...")
    time.sleep(2)  # Small delay before next cycle

# Release camera when done (optional)
cam.release()