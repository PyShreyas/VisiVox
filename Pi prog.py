import cv2
import pytesseract
import pyttsx3
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\shrey\OCR-tesseract\tesseract.exe'

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize camera
cam = cv2.VideoCapture(0)  # 0 is the default camera

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
    text = extract_text_from_frame()
    if text:
        print("Extracted Text:", text)
        speak(text)
    else:
        print("No text detected.")
    
    time.sleep(2)  # Small delay before next cycle

# Release camera when done (optional)
cam.release()
