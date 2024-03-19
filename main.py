import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import Scale

# Initialize Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set the frame width and height
frame_width, frame_height = 640, 480

# Open the camera
cap = cv2.VideoCapture(0)
cap.set(3, frame_width)
cap.set(4, frame_height)

# Default sensitivity value
sensitivity_value = 1.0

def update_sensitivity(value):
    global sensitivity_value
    sensitivity_value = float(value)

# Create GUI window
root = tk.Tk()
root.title("Hand Gesture Mouse Control by Dev-Uncommanash")
root.geometry("550x500")

# Create a frame for the selfie preview
selfie_frame = tk.Frame(root)
selfie_frame.grid(row=0, column=0)

# Create a label for the selfie preview
selfie_label = tk.Label(selfie_frame)
selfie_label.pack()

# Create a frame for sensitivity controls
sensitivity_frame = tk.Frame(root)

left_click_note_label = tk.Label(root, text="Connect Thumb and Index Finger for Left Click")
left_click_note_label.grid(row=1, columnspan=2, pady=10)


# Create sensitivity slider
sensitivity_label = tk.Label(sensitivity_frame, text="Sensitivity")
sensitivity_label.pack()

sensitivity_slider = Scale(sensitivity_frame, from_=0.1, to=2.0, resolution=0.1, orient="horizontal", command=update_sensitivity)
sensitivity_slider.set(sensitivity_value)
sensitivity_slider.pack()

# Function to update mouse position based on hand gesture
def update_mouse_position():
    ret, frame = cap.read()
    if not ret:
        return

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract hand landmarks
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Get the coordinates of index finger and thumb
            x_index, y_index = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)
            x_thumb, y_thumb = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)

            # Move the mouse using pyautogui with sensitivity
            pyautogui.moveTo(x_index * sensitivity_value*2.5, y_index * sensitivity_value*2.5)

            # Check for left-click gesture (thumb and index finger tips close)
            if abs(x_thumb - x_index) < 20 and abs(y_thumb - y_index) < 20:
                pyautogui.click()

    # Display the frame in the selfie preview window
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (400, 300))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    selfie_label.imgtk = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
    selfie_label.configure(image=selfie_label.imgtk)

    # Schedule the function to run again
    root.after(10, update_mouse_position)

# Start the GUI loop
root.after(10, update_mouse_position)
root.mainloop()

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
