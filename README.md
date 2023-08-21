# Moving Mouse using computer vision and tracking hand

This program uses computer vision and hand tracking to control the mouse cursor's movement based on hand gestures.

## Dependencies:
- cv2 (OpenCV): Computer vision library for image processing.
- cvzone: A Python module for hand tracking.
- pyautogui: A cross-platform GUI automation library used to control the mouse.

## Usage:
1. Make sure you have a webcam connected to your computer.
2. Adjust the cropping parameters for the hand's working area on the camera feed.
3. Run the program. It will use your hand's gestures to control the mouse cursor's movement.
4. Close fist to use left mouse button.
5. Press 'q' on the camera feed window to stop the program.

![Mouse control via computer vision](cv_mouse.gif)

## Webcam setup
- The program uses the OpenCV library to capture video from the webcam.
- The resolution of the webcam is automatically detected and set as the resolution for the program.

## Hand tracking and cropping
- The program uses the cvzone module for hand tracking.
- The cropping parameters are used to define the working area for the hand on the camera feed.
- Adjust the values of `x_crop_min`, `x_crop_max`, `y_crop_min`, and `y_crop_max` to change the cropping area.

## Mouse control
- The program uses the pyautogui library to control the mouse.
- When the index, middle, ring, and pinky fingers are closed, the left mouse button is pressed.
- When the fingers are straight, the left mouse button is released.
- The program tracks the base of the hand as a reference point for mouse movement (point 0 in hand_points.png)
- The program maps the coordinates of the hand in the cropped region to the full monitor resolution.
- The program calculates the average of recent cursor positions to smooth out the mouse movement. Adjust window size to your needs.

## Stopping the program
- Press 'q' on the camera feed window to stop the program.
- The webcam is released and all OpenCV windows are closed.

## Additional files
- The project includes a `requirements.txt` file for installing the necessary dependencies.
- The project also includes a `hands_points.png` file for reference.
