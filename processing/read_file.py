import cv2
import numpy as np
from PIL import Image
from solver.solver import recurse, print_sol


def color_distance(c1, c2):
    return np.sqrt(np.sum((np.array(c1) - np.array(c2)) ** 2))


# Function to merge similar colors
def merge_similar_colors(grid, tolerance=10):
    unique_colors = []
    color_map = {}

    for row in grid:
        for color in row:
            merged = False
            for unique_color in unique_colors:
                if color_distance(color, unique_color) < tolerance:
                    color_map[color] = unique_color
                    merged = True
                    break
            if not merged:
                unique_colors.append(color)
                color_map[color] = color

    merged_color_grid = [[color_map[color] for color in row] for row in grid]
    return merged_color_grid


def build_grid_for_solver(color_grid, colors):
    grid = []
    for row in color_grid:
        r = []
        for entry in row:
            r.append([colors.index(entry), False])
        grid.append(r)
    return grid


def process_file(image_path):
    img = Image.open(image_path)
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # # Sort and find the largest rectangle contour which should be the outer border of the grid
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    grid_contour = contours[0]
    #
    # # Approximate the contour to get the number of divisions
    epsilon = 0.1 * cv2.arcLength(grid_contour, True)
    approx = cv2.approxPolyDP(grid_contour, epsilon, True)

    x, y, w, h = cv2.boundingRect(grid_contour)

    cell_width = w // 10
    cell_height = h // 10

    color_grid = []
    for row in range(11):
        color_row = []
        for col in range(11):
            # Get the color of the center pixel of the square
            center_x = x + int((col + 0.5) * cell_width)
            center_y = y + int((row + 0.5) * cell_height)
            color = tuple(img_np[center_y, center_x][:3])
            color_row.append(color)
        color_grid.append(color_row)
    color_grid = merge_similar_colors(color_grid, tolerance=10)

    color_indexes = set()
    for row in color_grid:
        for entry in row:
            color_indexes.add(entry)
    colors = list(color_indexes)
    return build_grid_for_solver(color_grid, colors)
