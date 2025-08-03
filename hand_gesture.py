import cv2
import mediapipe as mp
import pyautogui
import time
import subprocess
from pynput.mouse import Button, Controller

# Initialize Mouse Controller
mouse = Controller()

# Get Screen Size
screen_width, screen_height = pyautogui.size()

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2  
)

# Cursor Positioning
cursor_x, cursor_y = screen_width // 2, screen_height // 2
alpha = 0.2

# Cooldown Timer for Gestures
last_action_time = 0
cooldown_duration = 7

# Move Mouse Smoothly
def move_mouse(index_finger_tip):
    global cursor_x, cursor_y
    if index_finger_tip:
        # Expanded input clamp range
        x = max(-0.2, min(1.2, index_finger_tip.x))
        y = max(-0.2, min(1.2, index_finger_tip.y))

        # Convert to screen coordinates
        new_x = x * screen_width
        new_y = y * screen_height * 1.2

        # Apply smoothing
        cursor_x = alpha * new_x + (1 - alpha) * cursor_x
        cursor_y = alpha * new_y + (1 - alpha) * cursor_y

        # Loosen screen bound clamp slightly with buffer (simulate over-scroll)
        edge_buffer = 20  # pixels
        cursor_x = max(-edge_buffer, min(screen_width + edge_buffer, int(cursor_x)))
        cursor_y = max(-edge_buffer, min(screen_height + edge_buffer, int(cursor_y)))

        # Move cursor
        pyautogui.moveTo(cursor_x, cursor_y, duration=0.01)

# Check if a finger is extended
def is_finger_extended(landmarks, finger_tip, finger_pip):
    return landmarks[finger_tip].y < landmarks[finger_pip].y

# Calculate distance between two landmarks
def get_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2) ** 0.5

# Open Application with Cooldown
def open_application(app_name):
    global last_action_time
    current_time = time.time()
    if current_time - last_action_time > cooldown_duration:
        print(f"Opening {app_name}")
        if app_name == "chrome":
            subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])  
        elif app_name == "notepad":
            subprocess.Popen(["notepad.exe"])  
        elif app_name == "calculator":
            subprocess.Popen("calc.exe")  
        last_action_time = current_time

# Detect App Opening Gestures 
def detect_app_opening(frame, landmarks_left, landmarks_right):
    global last_action_time
    current_time = time.time()

    if current_time - last_action_time < cooldown_duration:
        return False

    if landmarks_left and landmarks_right:
        # Gesture 1: Both index fingers extended (forming a "V") to open Chrome
        if is_finger_extended(landmarks_left, 8, 6) and is_finger_extended(landmarks_right, 8, 6):
            cv2.putText(frame, "Opening Chrome...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            open_application("chrome")
            return True

        # Gesture 2: Left index finger extended + Right thumb extended to open Notepad
        elif is_finger_extended(landmarks_left, 8, 6) and is_finger_extended(landmarks_right, 4, 2):
            cv2.putText(frame, "Opening Notepad...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            open_application("notepad")
            return True

        # Gesture 3: Left thumb extended + Right index finger extended to open Calculator
        elif is_finger_extended(landmarks_left, 4, 2) and is_finger_extended(landmarks_right, 8, 6):
            cv2.putText(frame, "Opening Calculator...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            open_application("calculator")
            return True

    return False  

# Gesture Detection
def detect_gesture(frame, landmarks_list, num_hands):
    global last_action_time
    current_time = time.time()

    if num_hands == 0:
       cv2.putText(frame, "Hand Not Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
       return  
  

    if current_time - last_action_time < cooldown_duration:
        return  

    landmarks = landmarks_list[0]  

    index_finger_tip = landmarks[mpHands.HandLandmark.INDEX_FINGER_TIP]
    index_extended = is_finger_extended(landmarks, 8, 6)
    middle_extended = is_finger_extended(landmarks, 12, 10)
    ring_extended = is_finger_extended(landmarks, 16, 14)
    pinky_extended = is_finger_extended(landmarks, 20, 18)
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    # Cursor Movement
    if index_extended and not (middle_extended or ring_extended or pinky_extended):
        move_mouse(index_finger_tip)
        cv2.putText(frame, "Cursor Movement", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Left Click (Index + Middle Finger Extended)
    elif index_extended and middle_extended and not (ring_extended or pinky_extended):
        mouse.press(Button.left)
        mouse.release(Button.left)
        cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Right Click (Index + Middle + Ring Finger Extended)
    elif index_extended and middle_extended and ring_extended and not pinky_extended:
        mouse.press(Button.right)
        mouse.release(Button.right)
        cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Screenshot (Pinch Gesture)
    elif get_distance(thumb_tip, index_tip) < 0.05:
        if current_time - last_action_time > cooldown_duration:
            print("Pinch gesture detected! Taking Screenshot...")
            screenshot = pyautogui.screenshot()
            screenshot.save(f'screenshot_{int(time.time())}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            last_action_time = current_time
    
    # Double Click (All Fingers Extended except Thumb)
    elif index_extended and middle_extended and ring_extended and pinky_extended:
        pyautogui.doubleClick()
        cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Freeze Cursor (Thumb + Pinky Extended)
    elif is_finger_extended(landmarks, 4, 2) and is_finger_extended(landmarks, 20, 18):
        cv2.putText(frame, "Cursor Frozen", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        return  


# Main Function
def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frame", 640, 480)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmarks_left, landmarks_right = None, None
            landmarks_list = []

            if processed.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(processed.multi_hand_landmarks, processed.multi_handedness):
                    if handedness.classification[0].label == "Left":
                        landmarks_left = [lm for lm in hand_landmarks.landmark]
                    elif handedness.classification[0].label == "Right":
                        landmarks_right = [lm for lm in hand_landmarks.landmark]
                    landmarks_list.append(hand_landmarks.landmark)

           
            if detect_app_opening(frame, landmarks_left, landmarks_right):
                pass
            else:
                detect_gesture(frame, landmarks_list, len(landmarks_list))

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
