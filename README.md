# Hand Gesture Controller

**Hand Gesture Controller** is a Python-based application that lets you control your mouse and launch applications like Chrome, Notepad, and Calculator using just your hand gestures. It uses your webcam along with OpenCV, MediaPipe, and PyAutoGUI to recognize finger positions and trigger actions accordingly.

---

## 🚀 Features

- **Mouse Movement**  
  Move your cursor using your index finger.

- **Left & Right Click**  
  Perform mouse clicks using specific finger combinations.

- **Double Click**  
  Extend all fingers (except thumb) to simulate a double click.

- **Pinch Screenshot**  
  Bring thumb and index finger close to take a screenshot.

- **Application Launcher**  
  Trigger different hand gestures to open:
  - Chrome
  - Notepad
  - Calculator

- **Gesture Cooldown Timer**  
  Prevents accidental repeated triggers by adding a cooldown duration.

---

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/hand-gesture-control.git
   cd hand-gesture-control

2. **Install Dependencies**

   Ensure you have Python 3 installed, then run:
   ```bash
   pip install opencv-python mediapipe pyautogui pynput

3. **Run the Application**
   ```bash
   python hand_gesture.py

---

## 📌 Usage

- **Mouse Move**  
  Extend only your index finger.

- **Left Click**  
  Extend index and middle fingers.

- **Right Click**  
  Extend index, middle, and ring fingers.

- **Double Click**  
  Extend all fingers except thumb.

- **Screenshot**  
  Pinch your thumb and index finger together.

- **Freeze Cursor**  
  Extend both thumb and pinky fingers.

- **Open Chrome**  
  Extend both index fingers from each hand to form a "V".

- **Open Notepad**  
  Extend left index and right thumb.

- **Open Calculator**  
  Extend left thumb and right index.

  
**Press q to exit the application.**

---

## 📁 File Structure

hand-gesture-control/

├── hand_gesture.py           # Main application script

---

## 💡 Notes

•  Ensure good lighting and position your hands within the webcam frame.

•  Only works on systems with the listed applications installed at the expected paths.

---

**Built with Python, OpenCV, and MediaPipe.**

**Hands-free interaction made possible.**

