from processing.read_file import process_file
from solver import print_sol, recurse

if __name__ == '__main__':
    grid = process_file("../queens_25.png")
    print_sol(recurse(grid, 0))