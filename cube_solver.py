from rubik_solver import utils


def solve_cube(cube_color_string):
    utils.solve(cube_color_string, 'Kociemba')

if __name__ == "__main__":
    # cube_colors = 'rryoyygoygybogboroyyrgoobgbgbogbyrbgbbygrrorrwwwwwwwww'
    cube_colors = 'rryoyygoybboygrgooyyrgoobgbgbogbyrbgbbygrrorrwwwwwwwww'
    print(utils.solve(cube_colors, 'Kociemba'))