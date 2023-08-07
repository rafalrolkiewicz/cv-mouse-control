"""
Moving Mouse by Tracking Hand
This program uses computer vision and hand tracking to control the mouse
cursor's movement based on hand gestures.

Dependencies:
- cv2 (OpenCV): Computer vision library for image processing.
- cvzone: A Python module for hand tracking.
- pyautogui: A cross-platform GUI automation library used to control mouse.

Usage:
1. Make sure you have a webcam connected to your computer.
2. Adjust the cropping parameters for the hand's working area
on the camera feed.
3. Run the program. It will use your hand's gestures to control
the mouse cursor's movement.
4. Close fist to use left mouse button.
5. Press 'q' on camera feed window to stop program

"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui


# Webcam setup
cap = cv2.VideoCapture(0)
cam_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Camera resolution: {int(cam_width)}x{int(cam_height)}")
cap.set(3, cam_width)
cap.set(4, cam_height)

# Set up working area for hand (how to crop camera view)
x_crop_min = 0.4
x_crop_max = 0.7
y_crop_min = 0.4
y_crop_max = 0.8
crop_cam_x_min = cam_width * x_crop_min
crop_cam_x_max = cam_width * x_crop_max
crop_cam_y_min = cam_height * y_crop_min
crop_cam_y_max = cam_height * y_crop_max

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.9)
leftclick = False

# Monitor set up
monitor_width, monitor_height = pyautogui.size()
print(f"Monitor resolution: {monitor_width}x{monitor_height}")

# Don't rise error when cursor moving to corners of screen
pyautogui.FAILSAFE = False

# Variables for cursor moving average
WINDOW_SIZE = 6
cursor_positions = []


# Map value from croped region of camera to full monitor resolution:
def map_value(value_to_map, minimum, maximum, new_min, new_max):
    return ((value_to_map - minimum)
            * (new_max - new_min)
            / (maximum - minimum) + new_min)


while True:
    succes, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand['lmList']

        # if index, middle, ring and pinky fingers closed
        # push left mouse button
        if (
            lmList[8][1] > lmList[5][1]
            and lmList[12][1] > lmList[9][1]
            and lmList[16][1] > lmList[13][1]
            and lmList[20][1] > lmList[17][1]
            and leftclick is False
        ):
            pyautogui.mouseDown()
            leftclick = True

        # if fingers straight release left mouse button
        if (
            lmList[8][1] < lmList[5][1]
            and lmList[12][1] < lmList[9][1]
            and lmList[16][1] < lmList[13][1]
            and lmList[20][1] < lmList[17][1]
            and leftclick is True
        ):
            pyautogui.mouseUp()
            leftclick = False

        # Track base of hand as mouse reference (point 0)
        x = lmList[0][0]
        y = lmList[0][1]
        x = (cam_width - x)

        x = map_value(x, crop_cam_x_min, crop_cam_x_max, 0, monitor_width)
        y = map_value(y, crop_cam_y_min, crop_cam_y_max, 0, monitor_height)
        cursor_positions.append((x, y))

        # Maintain the moving average window size
        if len(cursor_positions) > WINDOW_SIZE:
            cursor_positions.pop(0)  # Remove the oldest position

        # Calculate the average of recent cursor positions
        avg_x = sum(pos[0] for pos in cursor_positions) / len(cursor_positions)
        avg_y = sum(pos[1] for pos in cursor_positions) / len(cursor_positions)

        # Move mouse to coordinates
        pyautogui.moveTo(avg_x, avg_y)

    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)

    # Stop the loop and close the program if 'q' is pressed
    if key == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
