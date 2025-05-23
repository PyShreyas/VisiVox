# 🤖 VisiVox - Assistive Vision and Voice Robot

VisiVox is an AI-powered assistive robot designed to aid **visually impaired individuals** by providing **real-time text recognition, obstacle detection**, and **text-to-speech (TTS)** feedback. The system combines computer vision, ultrasonic sensing, and speech generation to interpret surroundings and vocalize critical visual information.

---

## 📌 Features

- 🔍 **Optical Character Recognition (OCR)** using a camera module
- 📏 **Obstacle detection** using ultrasonic sensors
- 🗣️ **Text-to-Speech conversion** for spoken feedback
- 🔊 Alerts when specific keywords (like "ARTICLE") are detected
- 📦 Embedded system using Raspberry Pi and Arduino Nano
- 👣 Supports navigation assistance in real-world environments

---

## 🛠️ Hardware Components

| Component               | Description                              |
| ----------------------- | ---------------------------------------- |
| Raspberry Pi 4 (8GB)    | Central controller and vision processing |
| Arduino Nano            | Controls ultrasonic sensors              |
| Ultrasonic Sensor      | Measures distance to obstacles           |
| Camera Module           | Captures frames for text extraction      |
| Speaker                 | Outputs the TTS voice                    |
| Power Bank (20,000 mAh) | Powers the full system                   |
|                         |                                          |

---

## 🧠 Software & Libraries

- **Python 3**
- **OpenCV** - for image capture and processing
- **Tesseract OCR** - for text extraction
- **pyttsx3** - for TTS output
- **Serial communication** (via `pyserial`) - to interface with Arduino
- **Raspberry Pi OS / Linux environment**

---

## 📚 Dependencies

VisiVox relies on several Python libraries for image processing, text recognition, speech synthesis, sensor interfacing, and optional data visualization. Before running the application, ensure that the necessary dependencies are installed.

### 🔧 Required Libraries

All libraries used in the VisiVox project are listed in the [`libraries.txt`](./libraries.txt) file. 

### 🛠️ Installation
Code:
```bash
pip install opencv-python pytesseract pyttsx3 pyserial numpy pillow imutils matplotlib seaborn pandas plotly
```

`Tesseract-OCR` is installed on both the Raspberry Pi and PC for text and OCR evaluation analysis.
Installation code:
```bash
sudo apt-get install tesseract-ocr
```

---

## 🗂️ Folder Structure

```plaintext
VisiVox/
├── 1ultrasens.ino                # Arduino Nano code for ultrasonic obstacle detection
├── Basic text detection.py       # Text detection with ROI-based bounding in captured frames
├── Combination graphs 2.py       # Graph plotting of text parameters (angle, blur, luminance, etc.)
├── combination-graphs.py         # Alternate script for the same graphical analysis
├── IMAGES.docx                   # Screenshots of device, terminal logs, and text detection regions
├── libraries.txt                 # List of all required Python libraries
├── main pi prog.py               # Final tested Raspberry Pi program for TTS + obstacle detection
├── pi prog.py                    # Alternate Pi script for text + obstacle-based auditory alerts
└── README.md                     # Project overview and documentation
```



