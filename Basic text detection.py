import cv2
import pytesseract
from pytesseract import Output
import numpy as np

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\shrey\OCR-tesseract\tesseract.exe'

# Process each frame
def process_frame(frame):
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    text_data = pytesseract.image_to_data(gray, output_type=Output.DICT)
    
    for i in range(len(text_data['text'])):
        word = text_data['text'][i].strip()
        if word:
            x, y, w, h = (text_data['left'][i], text_data['top'][i], 
                           text_data['width'][i], text_data['height'][i])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

# Main function
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = process_frame(frame)
            cv2.imshow("Environment View", processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
