from collections import deque

neighbors_2d_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
neighbors_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def validate_row(grid, row):
    """
    Each row must have 1 queen.
    :param grid: Current state of the board
    :param row: Row index we're checking
    :return: True if valid (only one queen). False otherwise
    """
    c = 0
    for col_val in grid[row]:
        if col_val[1]:
            c += 1
    return c == 1


def validate_col(grid, col):
    """
    Each column must have 1 queen.
    :param grid: Current state of the board
    :param col: Column index we're checking
    :return: True if valid (only one queen). False otherwise
    """
    c = 0
    for row in grid:
        if row[col][1]:
            c += 1
    return c == 1


def valid_point(grid, point):
    """
    Checks if the point is out of bounds or not.
    :param grid: Current state of the board
    :param point: i,j coordinates of the point
    :return: True if the point is in bounds. False otherwise.
    """
    i, j = point
    return 0 <= i < len(grid) and 0 <= j < len(grid[i])


def flood_fill(grid, i, j):
    """
    Each grid spot is a tuple of number / queenPresent.
    This checks that the color in the target spot only has one queen.
    :param grid: Current state of the board
    :param i: Row index
    :param j: Col index
    :return: True if the color has only one queen.
    """
    color = grid[i][j][0]
    seen = set()
    toVisit = deque([(i, j)])
    count = 0
    while toVisit:
        curr = toVisit.popleft()
        c_i, c_j = curr
        if valid_point(grid, curr) and grid[c_i][c_j][0] == color and curr not in seen:
            if grid[c_i][c_j][1]:
                count += 1
            seen.add(curr)
            for di, dj in neighbors_2d_4:
                toVisit.append((c_i + di, c_j + dj))
    return count == 1


def validate_diag_neighbors(grid, i, j):
    """
    A queen placement can't have any adjacent (including diagonals) queens. The row and column validators check the
    direct neighbors, so we need to check the diagonals here.
    :param grid: Current state of the board
    :param i: Row index
    :param j: Column index
    :return: True if there are no neighboring queens.
    """
    c = 0
    for di, dj in neighbors_diag:
        ni, nj = i + di, j + dj
        if valid_point(grid, (ni, nj)) and grid[ni][nj][1]:
            c += 1
    return c == 0


def validate_placement(grid, i, j):
    """
    Checks if placing a queen here is valid
    :param grid: Current state of the board
    :param i: row index
    :param j: col index
    :return: True if placing a queen here is valid
    """
    return (validate_diag_neighbors(grid, i, j)
            and validate_col(grid, j)
            and validate_row(grid, i)
            and flood_fill(grid, i, j))


def recurse(grid, row):
    """
    Uses recursive backtracking to solve the Linkedin Queens game.
    :param grid: Current state of the board
    :param row: Row index to place a queen in.
    :return: Solution
    """
    if row == len(grid):
        # we're done, return.
        return grid
    for col in range(len(grid[row])):
        grid[row][col][1] = True
        if validate_placement(grid, row, col):
            v = recurse(grid, row + 1)
            if v:
                return v
        grid[row][col][1] = False
    return None


def print_sol(sol):
    for line in sol:
        s = ""
        for entry in line:
            if entry[1]:
                s += f"{str(entry[0])}x\t"
            else:
                s += f"{str(entry[0])}.\t"
        print(s)


if __name__ == '__main__':
    var = [[[0, False], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False],
            [0, False]],
           [[0, False], [1, False], [1, False], [1, False], [6, False], [6, False], [6, False], [6, False], [6, False],
            [7, False]],
           [[0, False], [1, False], [2, False], [2, False], [2, False], [2, False], [4, False], [5, False], [6, False],
            [7, False]],
           [[0, False], [1, False], [2, False], [9, False], [9, False], [9, False], [4, False], [5, False], [6, False],
            [7, False]],
           [[0, False], [1, False], [2, False], [8, False], [8, False], [9, False], [4, False], [5, False], [6, False],
            [7, False]],
           [[0, False], [1, False], [2, False], [8, False], [3, False], [9, False], [4, False], [5, False], [6, False],
            [7, False]],
           [[0, False], [1, False], [3, False], [3, False], [3, False], [9, False], [4, False], [5, False], [6, False],
            [7, False]],
           [[0, False], [4, False], [4, False], [4, False], [4, False], [4, False], [4, False], [5, False], [6, False],
            [7, False]],
           [[0, False], [5, False], [5, False], [5, False], [5, False], [5, False], [5, False], [5, False], [6, False],
            [7, False]],
           [[7, False], [7, False], [7, False], [7, False], [7, False], [7, False], [7, False], [7, False], [7, False],
            [7, False]]]
    ans = recurse(var, 0)
    print_sol(ans)
