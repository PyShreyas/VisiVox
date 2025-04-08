import cv2
import pytesseract
from pytesseract import Output
import sqlite3
import time
import numpy as np
import matplotlib.pyplot as plt

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\shrey\OCR-tesseract\tesseract.exe'

# Initialize SQLite database
def initialize_database():
    conn = sqlite3.connect('text_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detected_text (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        category TEXT,
        angle FLOAT,
        luminosity FLOAT,
        blur_score FLOAT,
        perspective_distortion TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    return conn, cursor

# Store detected text in database
def store_in_database(cursor, conn, text, category, angle, luminosity, blur_score, perspective_distortion):
    cursor.execute('''
    INSERT INTO detected_text (text, category, angle, luminosity, blur_score, perspective_distortion)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (text, category, angle, luminosity, blur_score, perspective_distortion))
    conn.commit()

# Calculate image luminosity
def calculate_luminosity(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)

# Calculate image blur score
def calculate_blur_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

# Detect text angle using Tesseract OSD
def detect_text_angle(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        osd = pytesseract.image_to_osd(gray, config='--psm 0', output_type=Output.DICT)
        return osd.get('rotate', 0.0)
    except Exception as e:
        print(f"OSD Error: {e}")
        return 0.0

# Detect perspective distortion
def detect_perspective_distortion(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    small_gray = cv2.resize(gray, (320, 240))
    edges = cv2.Canny(small_gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        angles = [np.degrees(np.arctan2(y2 - y1, x2 - x1)) for line in lines for x1, y1, x2, y2 in line]
        return f"{np.mean(angles):.2f} degrees"
    return "0.00 degrees"

# Process each frame
def process_frame(frame, cursor, conn):
    frame = cv2.resize(frame, (640, 480))
    luminosity = calculate_luminosity(frame)
    blur_score = calculate_blur_score(frame)

    if blur_score < 100:
        print("Skipping blurry frame...")
        return

    perspective_distortion = detect_perspective_distortion(frame)
    angle = detect_text_angle(frame)

    try:
        text_data = pytesseract.image_to_data(frame, output_type=Output.DICT)
    except Exception as e:
        print(f"OCR Error: {e}")
        return

    for i, word in enumerate(text_data['text']):
        if word.strip():
            category = (
                "2-letter word" if len(word) == 2 else
                "3-letter word" if len(word) == 3 else
                "4-letter word" if len(word) == 4 else
                "More than 4 letters"
            )
            store_in_database(cursor, conn, word, category, angle, luminosity, blur_score, perspective_distortion)
            print(f"Detected: {word} | Category: {category} | Angle: {angle}° | Luminosity: {luminosity:.2f} | Blur Score: {blur_score:.2f} | Distortion: {perspective_distortion}")

# Fetch data from the database
def fetch_data():
    conn = sqlite3.connect('text_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, category, angle, luminosity, blur_score, perspective_distortion, timestamp FROM detected_text")
    data = cursor.fetchall()
    conn.close()
    return data

# Plot category distribution
def plot_category_distribution(data):
    categories = [row[1] for row in data]
    unique_categories, counts = np.unique(categories, return_counts=True)

    plt.figure(figsize=(8, 5))
    plt.bar(unique_categories, counts, color=['blue', 'green', 'red', 'purple'])
    plt.xlabel("Word Categories")
    plt.ylabel("Count")
    plt.title("Text Category Distribution")
    plt.xticks(rotation=30)
    plt.show()

# Plot angle distribution
def plot_angle_distribution(data):
    angles = [row[2] for row in data]

    plt.figure(figsize=(8, 5))
    plt.hist(angles, bins=10, color='orange', edgecolor='black', alpha=0.7)
    plt.xlabel("Angle (Degrees)")
    plt.ylabel("Frequency")
    plt.title("Detected Text Angle Distribution")
    plt.show()

# Plot luminosity vs. blur score
def plot_luminosity_vs_blur(data):
    luminosity = [row[3] for row in data]
    blur_score = [row[4] for row in data]

    plt.figure(figsize=(8, 5))
    plt.scatter(luminosity, blur_score, color='red', alpha=0.6)
    plt.xlabel("Luminosity")
    plt.ylabel("Blur Score")
    plt.title("Luminosity vs. Blur Score")
    plt.grid(True)
    plt.show()

# Plot perspective distortion analysis
def plot_perspective_analysis(data):
    # Filter out None values and empty strings
    distortions = [row[5] for row in data if row[5] is not None and row[5].strip() != '']
    if not distortions:
        print("No valid perspective distortion data to plot.")
        return

    # Extract unique distortion values and their counts
    unique_distortions, counts = np.unique(distortions, return_counts=True)

    # Limit the number of categories to the top 10 most frequent ones
    top_indices = counts.argsort()[-10:][::-1]
    top_unique_distortions = np.array(unique_distortions)[top_indices]
    top_counts = counts[top_indices]

    # Create a pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(top_counts, labels=top_unique_distortions, autopct='%1.1f%%', startangle=90, colors=plt.cm.rainbow(np.linspace(0, 1, len(top_counts))))
    plt.title("Top 10 Perspective Distortion Analysis")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# Main function
def main():
    conn, cursor = initialize_database()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    start_time = time.time()
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % 2 == 0:
                process_frame(frame, cursor, conn)
            frame_count += 1

            cv2.imshow("Environment View", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        conn.close()

    print(f"Total time taken: {time.time() - start_time:.6f} seconds")

    data = fetch_data()
    if not data:
        print("No data found in the database.")
        return

    plot_category_distribution(data)
    plot_angle_distribution(data)
    plot_luminosity_vs_blur(data)
    plot_perspective_analysis(data)

if __name__ == "__main__":
    main()