from rubik_solver import utils

if __name__ == "__main__":
    # cube_colors = 'rryoyygoygybogboroyyrgoobgbgbogbyrbgbbygrrorrwwwwwwwww'
    cube_colors = 'rryoyygoybboygrgooyyrgoobgbgbogbyrbgbbygrrorrwwwwwwwww'
    print(utils.solve(cube_colors, 'Kociemba'))