import cv2
import numpy as np
from time import sleep
# import cube_solver
from rubik_solver import utils


colors = {}
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


def detect_color(img):
    return_value = '_'
    bgr = np.average(img[15:75, 15:75], axis=0)
    bgr = np.average(bgr, axis=0)
    bgr = np.uint8(bgr)
    # print("one pixel", img[45, 46])
    # print("mean", bgr)
    all_min = 1000
    for key, value in colors.items():
        my_min_1 = abs(int(bgr[0]) - int(colors[key][0]))
        my_min_2 = abs(int(bgr[1]) - int(colors[key][1]))
        my_min_3 = abs(int(bgr[2]) - int(colors[key][2]))
        my_min = my_min_1 + my_min_2 + my_min_3
        # print(color_enum[key], my_min)
        if my_min < all_min:
            all_min = my_min
            return_value = color_enum[key]
    # print("all_min", all_min, "return_value", return_value)
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
    if key == ord('a'):
        face_count -= 1
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


def show_solution(solution):
    sol_image = cv2.imread("images/solution_explanation.png")
    cv2.putText(sol_image,
                f'Solution is: {solution}',
                (160, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (6, 5, 250), 2)
    cv2.imshow("solution", sol_image)
    key = cv2.waitKey()
    if key == 27:  # exit on ESC
        exit()


if __name__ == "__main__":
    # init parameters
    face_count, color_count, record_counter = 0, 0, 0
    calibrated, record = False, False
    cube_color_string = ''
    # start webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    sleep(0.5)
    while True:
        # get frame and start analysis
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        # first need to calibrate colors
        if not calibrated:
            # instruct user which color to calibrate
            calib_instructions(frame, color_count)
            cv2.imshow('image', frame)
            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break
            # take a snapshot and save colors...
            if key == ord('e'):
                # bgr_1 = frame[155, 156]
                temp = np.average(frame[145:175, 145:175], axis=0)
                temp = np.average(temp, axis=0)
                bgr = np.uint8(temp)
                # print("one pixel", bgr_1)
                colors[color_count] = (bgr[0], bgr[1], bgr[2])
                # colors[color_count] = (bgr[0], bgr[1], bgr[2])
                print(color_count, colors[color_count])
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
            cv2.putText(frame,
                        "To go back and correct the color press 'A'",
                        (60, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (6, 50, 250), 1)

            key = cv2.waitKey(20)

            # instruct user which face to show
            instructions(frame, face_count)
            # take the face snapshot and save colors...
            face_count = snapshots(frame, key, face_count, cube_color_string)

            if face_count == 6:
                # got all 6 faces, now fetch solution
                final_color_string = faces['top'] + faces['left'] \
                                     + faces['front'] + faces['right'] \
                                     + faces['back'] + faces['bottom']
                print("going to solve this cube string: ",
                      len(final_color_string), final_color_string)
                # send cube string to solver and receive the solution
                solution = utils.solve(final_color_string)
                print("solution is ", solution)
                # show user the solution on the instructions image
                show_solution(solution)
                cv2.destroyAllWindows()
                exit()

            if key == 27:  # exit on ESC
                break
            cv2.imshow('image', frame)
    cv2.destroyAllWindows()
