import cv2
import numpy as np
from time import sleep
import cube_solver


colors = {}
lower = {}
upper = {}
# lower = {
#     'red': (166, 84, 141),
#     'green': (66, 122, 129),
#     'blue': (97, 100, 117),
#     'yellow': (23, 59, 119),
#     'orange': (0, 50, 80),
#     'white': (150, 150, 168)}
# upper = {
#     'red': (186, 255, 255),
#     'green': (86, 255, 255),
#     'blue': (117, 255, 255),
#     'yellow': (54, 255, 255),
#     'orange': (20, 255, 255),
#     'white': (200, 255, 255)}
# colors = {
#     'red': (0, 0, 255),
#     'green': (0, 255, 0),
#     'blue': (255, 0, 0),
#     'yellow': (0, 255, 217),
#     'orange': (0, 140, 255),
#     'white': (255, 255, 255)}
# colors = {
#     0: (0, 0, 255),  # red
#     1: (0, 255, 0),  # green
#     2: (255, 0, 0),  # blue
#     3: (0, 255, 217),  # yellow
#     4: (0, 140, 255),  # orange
#     5: (255, 255, 255)}  # white
# color_enum = {
#     'red': 'r',
#     'green': 'g',
#     'blue': 'b',
#     'yellow': 'y',
#     'orange': 'o',
#     'white': 'w',
# }
color_enum = {
    0: 'r',
    1: 'g',
    2: 'b',
    3: 'y',
    4: 'o',
    5: 'w',
}
faces = {
    'top': '',
    'left': '',
    'front': '',
    'right': '',
    'back': '',
    'bottom': ''
}


# def detect_color(img):
#     return_value = '_'
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     for key, value in upper.items():
#         # print("in detect color", lower[key], upper[key])
#         # define kernel size
#         kernel = np.ones((7, 7), np.uint8)
#         # find the colors within the boundaries
#         mask = cv2.inRange(hsv, lower[key], upper[key])
#         # Remove unnecessary noise from mask
#         mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#         mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#         # Find contours from the mask
#         contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         # img = cv2.drawContours(img, contours, -1, (200, 200, 255), 0)
#         if len(contours) > 0:
#             print(len(contours), "->", color_enum[key])
#             return_value = color_enum[key]
#             # break
#     return return_value
def detect_color(img):
    return_value = '_'
    # bgr = img[45,45]
    bgr = np.average(img, axis=0)
    bgr = np.average(bgr, axis=0)
    bgr = np.uint8(bgr)
    print("one pixel", img[45, 46])
    print("mean", bgr)
    all_min = 1000
    for key, value in colors.items():
        my_min_1 = abs(int(bgr[0]) - int(colors[key][0]))
        my_min_2 = abs(int(bgr[1]) - int(colors[key][1]))
        my_min_3 = abs(int(bgr[2]) - int(colors[key][2]))
        my_min = my_min_1 + my_min_2 + my_min_3
        print(color_enum[key], colors[key], "my_min", my_min)
        if my_min < all_min:
            all_min = my_min
            return_value = color_enum[key]
    print("all_min", all_min, "return_value", return_value)
    return return_value


def classify_squares(frame, cube_color_string):
    # 1
    frame_to_detect = frame[55:145, 55:145]
    cube_color_string += detect_color(frame_to_detect)
    # 2
    frame_to_detect = frame[55:145, 155:245]
    cube_color_string += detect_color(frame_to_detect)
    # 3
    frame_to_detect = frame[55:145, 245:345]
    cube_color_string += detect_color(frame_to_detect)
    # 4
    frame_to_detect = frame[155:245, 55:245]
    cube_color_string += detect_color(frame_to_detect)
    # 5
    frame_to_detect = frame[155:245, 155:245]
    cube_color_string += detect_color(frame_to_detect)
    # 6
    frame_to_detect = frame[155:245, 255:345]
    cube_color_string += detect_color(frame_to_detect)
    # 7
    frame_to_detect = frame[255:345, 55:245]
    cube_color_string += detect_color(frame_to_detect)
    # 8
    frame_to_detect = frame[255:345, 155:245]
    cube_color_string += detect_color(frame_to_detect)
    # 9
    frame_to_detect = frame[255:345, 255:345]
    cube_color_string += detect_color(frame_to_detect)
    return cube_color_string


def instructions(frame, face_count):
    if face_count == 0:
        cv2.putText(frame,
                    "Place TOP side of cube in the marked square then press 'T'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if face_count == 1:
        cv2.putText(frame,
                    "Place LEFT side of cube in the marked square then press 'L'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if face_count == 2:
        cv2.putText(frame,
                    "Place FRONT side of cube in the marked square then press 'F'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if face_count == 3:
        cv2.putText(frame,
                    "Place RIGHT side of cube in the marked square then press 'R'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if face_count == 4:
        cv2.putText(frame,
                    "Place BACK side of cube in the marked square then press 'B'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if face_count == 5:
        cv2.putText(frame,
                    "Place Bottom side of cube in the marked square then press 'Z'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)


def calib_instructions(frame, color_count):
    cv2.rectangle(frame, (130, 130), (190, 190), (255, 0, 0), 3)
    cv2.putText(frame,
                f'Colors calibrated={color_count}',
                (360, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 150, 250), 1)

    if color_count == 0:
        cv2.putText(frame,
                    "Place RED color in the box and press 'E'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if color_count == 1:
        cv2.putText(frame,
                    "Place GREEN color in the box and press 'E'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if color_count == 2:
        cv2.putText(frame,
                    "Place BLUE color in the box and press 'E'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if color_count == 3:
        cv2.putText(frame,
                    "Place YELLOW color in the box and press 'E'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if color_count == 4:
        cv2.putText(frame,
                    "Place ORANGE color in the box and press 'E'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    if color_count == 5:
        cv2.putText(frame,
                    "Place WHITE color in the box and press 'E'",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)


def snapshots(frame, key, face_count, cube_color_string):
    if key == ord('t'):
        face_count += 1
        # cv2.imshow('TOP', frame)
        # save details of TOP face
        # detect color of 9 squares
        faces['top'] = classify_squares(frame, cube_color_string)
        print("top face", faces['top'])
    if key == ord('l'):
        face_count += 1
        # cv2.imshow('LEFT', frame)
        # save details of LEFT face
        faces['left'] = classify_squares(frame, cube_color_string)
        print("left face", faces['left'])
    if key == ord('f'):
        face_count += 1
        # cv2.imshow('FRONT', frame)
        # save details of FRONT face
        faces['front'] = classify_squares(frame, cube_color_string)
        print("front face", faces['front'])
    if key == ord('r'):
        face_count += 1
        # cv2.imshow('RIGHT', frame)
        # save details of RIGHT face
        faces['right'] = classify_squares(frame, cube_color_string)
        print("right face", faces['right'])
    if key == ord('b'):
        face_count += 1
        # cv2.imshow('BACK', frame)
        # save details of BACK face
        faces['back'] = classify_squares(frame, cube_color_string)
        print("back face", faces['back'])
    if key == ord('z'):
        face_count += 1
        # cv2.imshow('BOTTOM', frame)
        # save details of BOTTOM face
        faces['bottom'] = classify_squares(frame, cube_color_string)
        print("bottom face", faces['bottom'])
    return face_count


if __name__ == "__main__":
    cube_color_string = ''
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    # start webcam
    sleep(0.5)
    face_count = 0
    color_count = 0
    calibrated = False
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        if not calibrated:
            calib_instructions(frame, color_count)
            cv2.imshow('image', frame)
            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break
            # take a snapshot and save colors...
            if key == ord('e'):
                # get BGR lower and upper values
                bgr_1 = frame[155,156]
                bgr = np.average(frame[145:165, 145:165], axis=0)
                bgr = np.average(bgr, axis=0)
                bgr = np.uint8(bgr)
                print("one pixel", bgr_1)
                print("mean", bgr)
                # lower[color_count] = (bgr[0]-15, bgr[1]-15, bgr[2]-15)
                colors[color_count] = (bgr[0], bgr[1], bgr[2])
                # print(color_count, colors[color_count])

                color_count += 1
            if color_count == 6:
                calibrated = True
        else:
            cv2.rectangle(frame, (50, 50), (350, 350), (255, 0, 0), 3)
            cv2.line(frame, (150, 50), (150, 350), (0, 255, 0), 2)
            cv2.line(frame, (250, 50), (250, 350), (0, 255, 0), 2)
            cv2.line(frame, (50, 150), (350, 150), (0, 255, 0), 2)
            cv2.line(frame, (50, 250), (350, 250), (0, 255, 0), 2)
            cv2.putText(frame,
                        f'Cube sides recorded={face_count}',
                        (360, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 150, 250), 1)

            key = cv2.waitKey(20)

            # instruct user which face to show
            instructions(frame, face_count)
            # take the face snapshot and save colors...
            face_count = snapshots(frame, key, face_count, cube_color_string)

            if face_count == 6:
                final_color_string = faces['top'] + faces['left'] \
                                     + faces['front'] + faces['right'] \
                                     + faces['back'] + faces['bottom']
                print("going to solve this cube string: ",
                      len(final_color_string), final_color_string)
                # only now send to solver
                solution = cube_solver.solve_cube(final_color_string)
                print("solution is ", solution)
                # instruct user how to solve the cube

            if key == 27:  # exit on ESC
                break
            cv2.imshow('image', frame)
    cv2.destroyAllWindows()
