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

if __name__ == "__main__":
    # cap = cv2.VideoCapture(0)
    # if not cap.isOpened():
    #     raise IOError("Cannot open webcam")
    # start webcam
    while True:
        # ret, frame = cap.read()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        frame = cv2.imread('1.png')

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

                open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
                close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                for color, (lower, upper) in colors.items():
                    lower = np.array(lower, dtype=np.uint8)
                    upper = np.array(upper, dtype=np.uint8)
                    # color_mask = cv2.inRange(frame[y:y+h, x:x+w], lower, upper)

        cv2.imshow('image', frame)
        cv2.waitKey(0)
        exit()
        # detect all 9 squares
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.medianBlur(frame, 5)
        kernel = np.ones((5, 5), np.float32) / 25
        frame = cv2.filter2D(frame, -1, kernel)

        frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)
        # detect the colors
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

    # cap.release()
    cv2.destroyAllWindows()