# ✋ Hand Gesture-Controlled LED Matrix Display

This project uses **Python**, **OpenCV**, and **MediaPipe** to detect hand gestures from a webcam and sends signals to an **Arduino** which displays numbers or a smiley face on an **8x8 LED matrix (MAX7219)**.

---

## 🎯 Features
- Detects number of fingers raised (0–5)
- Detects only-middle-finger gesture
- Displays:
  - Digits `0` to `5` on LED matrix
  - 😊 Smiley when only middle finger is shown
- Works from both palm and back view
- Shows live **finger labels** on screen for debugging

---

## 🛠 Technologies Used
- **Python 3**
- **OpenCV** for video processing
- **MediaPipe** for hand tracking
- **PySerial** for Arduino communication
- **Arduino UNO** + **8x8 LED Matrix (MAX7219)**

---

## 🧩 Folder Structure

```
gesture-led-matrix/
├── gesture_display.py        # Python gesture detection code
├── gesture_display.ino       # Arduino display logic
├── images/                   # Screenshots, circuit diagram
├── README.md                 # You're reading this 😄
```

---

## 🧠 How It Works

| Gesture                  | Python Sends | LED Matrix Displays |
|--------------------------|--------------|----------------------|
| All fingers closed       | `0`          | 0                   |
| 1–5 fingers raised       | `1`–`5`       | 1–5                 |
| Only middle finger raised| `MIDDLE`     | 😊 Smiley            |

---

## 🔌 Circuit Connection (MAX7219)
- **DIN → Pin 11**
- **CLK → Pin 13**
- **CS → Pin 10**
- **VCC → 5V**
- **GND → GND**

---

## ✅ How to Run

### 1. Install Required Python Packages
```bash
pip install opencv-python mediapipe pyserial
```

### 2. Upload the Arduino Code
Use Arduino IDE to upload `gesture_display.ino` to your board.

### 3. Run the Python Script
```bash
python gesture_display.py
```

---

## 📸 Screenshots

---

## 👤 Author
**MOHAMMED SHESHIN THAMARACHALIL ABDULRESAK**  
This project is part of my personal robotics and embedded systems portfolio.
