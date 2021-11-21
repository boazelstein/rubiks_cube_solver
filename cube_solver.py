from rubik_solver import utils
import cv2


def show_solution(solution):
    sol_image = cv2.imread("solution_explenation.png")
    cv2.putText(sol_image,
                f'Solution is: {solution}',
                (160, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (6, 5, 250), 2)
    cv2.imshow("solution", sol_image)
    key = cv2.waitKey()
    if key == 27:  # exit on ESC
        exit()


def solve_cube(cube_color_string):
    solution = utils.solve(cube_color_string, 'Kociemba')
    return solution


if __name__ == "__main__":
    # cube_colors = 'yyggybyybgrbgborogroybrrogooyobgybrryrrgoogbbwwwwwwwww'
    cube_colors = 'ryrryrryrbbbbbbbbbwrwwrwwrwgggggggggyoyyoyyoyowoowoowo'
    print(solve_cube(cube_colors))
    show_solution(solve_cube(cube_colors))