import cv2
import imutils
from imutils.video import FPS
import numpy as np


colors = {
    'red': ([76, 0, 41], [179, 255, 70]),        # Red
    'blue': ([69, 120, 100], [179, 255, 255]),    # Blue
    'yellow': ([21, 110, 117], [45, 255, 255]),   # Yellow
    'orange': ([0, 110, 125], [17, 255, 255]),     # Orange
    'white': ([0, 0, 0], [25, 25, 25]),  # White
    'green': ([], []),  # Green
}


def detect_squares(frame):
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decrease_noise = cv2.fastNlMeansDenoising(grey, 10, 15, 7, 21)
    blurred = cv2.GaussianBlur(decrease_noise, (3, 3), 0)
    canny = cv2.Canny(blurred, 20, 40)
    thresh = cv2.threshold(canny, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    for c in contours:
        # obtain the bounding rectangle coordinates for each square
        x, y, w, h = cv2.boundingRect(c)
        factor = h / w if w > h else w / h
        if factor > 0.9 and 60 < h < 150:
            print(x, y, w, h)
            # With the bounding rectangle coordinates we draw the green bounding boxes
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('image', frame)
    cv2.waitKey(0)


def detect_color(image):
    hsvFrame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Set range for red color and
    # define mask
    red_lower = np.array([76, 0, 41], np.uint8)
    red_upper = np.array([179, 255, 70], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    # Set range for green color and
    # define mask
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    # Set range for blue color and
    # define mask
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    yellow_lower = np.array([21, 110, 117], np.uint8)
    yellow_upper = np.array([45, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")
    # For red color
    color_frame = image.copy()
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(color_frame, color_frame,
                              mask=red_mask)
    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(color_frame, color_frame,
                                mask=green_mask)
    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(color_frame, color_frame,
                               mask=blue_mask)
    # For yellow
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(color_frame, color_frame,
                               mask=yellow_mask)
    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        factor = h / w if w > h else w / h
        if factor > 0.9 and 60 < h < 150:
            color_frame = cv2.rectangle(color_frame, (x, y),
                                        (x + w, y + h),
                                        (0, 0, 255), 2)
            cv2.putText(color_frame, "Red Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))
    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        factor = h / w if w > h else w / h
        if factor > 0.9 and 60 < h < 150:
            color_frame = cv2.rectangle(color_frame, (x, y),
                                        (x + w, y + h),
                                        (0, 255, 0), 2)

            cv2.putText(color_frame, "Green Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 0))

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        factor = h / w if w > h else w / h
        if factor > 0.9 and 60 < h < 150:
            color_frame = cv2.rectangle(color_frame, (x, y),
                                        (x + w, y + h),
                                        (255, 0, 0), 2)

            cv2.putText(color_frame, "Blue Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 0))

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(yellow_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        factor = h / w if w > h else w / h
        if factor > 0.9 and 60 < h < 150:
            color_frame = cv2.rectangle(color_frame, (x, y),
                                        (x + w, y + h),
                                        (255, 255, 0), 2)

            cv2.putText(color_frame, "Yellow Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 255, 0))

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", color_frame)
    cv2.waitKey(0)


if __name__ == "__main__":
    # cap = cv2.VideoCapture(0)
    # if not cap.isOpened():
    #     raise IOError("Cannot open webcam")
    # start webcam
    while True:
        # ret, frame = cap.read()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        image = cv2.imread('cube4.jpeg')
        frame = image.copy()
        detect_squares(frame)
        # frame = image.copy()
        # detect_color(frame)

        
        cv2.destroyAllWindows()

        exit()

    # cap.release()
