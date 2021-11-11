import cv2
import numpy as np
from time import sleep

lower = {
    'red': (166, 84, 141),
    'green': (66, 122, 129),
    'blue': (97, 100, 117),
    'yellow': (23, 59, 119),
    'orange': (0, 50, 80),
    'white': (150, 150, 168)}
upper = {
    'red': (186, 255, 255),
    'green': (86, 255, 255),
    'blue': (117, 255, 255),
    'yellow': (54, 255, 255),
    'orange': (20, 255, 255),
    'white': (200, 200, 255)}
colors = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 217),
    'orange': (0, 140, 255),
    'white': (255, 255, 255)}


def detect_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for key, value in upper.items():
        # define kernel size
        kernel = np.ones((7, 7), np.uint8)
        # find the colors within the boundaries
        mask = cv2.inRange(hsv, lower[key], upper[key])
        # Remove unnecessary noise from mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # Find contours from the mask
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # img = cv2.drawContours(img, contours, -1, (200, 200, 255), 0)
        if len(contours) > 0:
            img = cv2.putText(img, key, (25,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    return img


def classify_squares(frame):
    # 1
    frame_to_detect = frame[55:145, 55:145]
    detect_color(frame_to_detect)
    # 2
    frame_to_detect = frame[55:145, 155:245]
    detect_color(frame_to_detect)
    # 3
    frame_to_detect = frame[55:145, 245:345]
    detect_color(frame_to_detect)
    # 4
    frame_to_detect = frame[155:245, 55:245]
    detect_color(frame_to_detect)
    # 5
    frame_to_detect = frame[155:245, 155:245]
    detect_color(frame_to_detect)
    # 6
    frame_to_detect = frame[155:245, 255:345]
    detect_color(frame_to_detect)
    # 7
    frame_to_detect = frame[255:345, 55:245]
    detect_color(frame_to_detect)
    # 8
    frame_to_detect = frame[255:345, 155:245]
    detect_color(frame_to_detect)
    # 9
    frame_to_detect = frame[255:345, 255:345]
    detect_color(frame_to_detect)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    # start webcam
    sleep(0.5)
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        cv2.rectangle(frame, (50, 50), (350, 350), (255, 0, 0), 3)
        cv2.line(frame, (150, 50), (150, 350), (0,255,0), 2)
        cv2.line(frame, (250, 50), (250, 350), (0,255,0), 2)
        cv2.line(frame, (50, 150), (350, 150), (0,255,0), 2)
        cv2.line(frame, (50, 250), (350, 250), (0,255,0), 2)
        # detect color in 9 squares
        classify_squares(frame)

        cv2.imshow('image', frame)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
        # take a snapshot when 'q' is pressed and save colors...
        if key == ord('q'):
            cv2.imshow('pressed q', frame)

    cv2.destroyAllWindows()