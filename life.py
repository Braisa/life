# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 00:00:14 2022

@author: brais
"""

import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as img
from functools import lru_cache
import sys

DEAD = 0
ALIVE = 1

# Start
current_generation = 0
# Opens and converts to black (False) and white (True)
names = np.genfromtxt("names.txt", dtype = "str")

ask_file = True
while ask_file:
    filename = input("File? ")
    if filename in names[:, 0]:
        filename = names[np.where(names == filename)[0], 1][0]
    try:
        board = np.asarray(img.open(filename + ".png").convert("1"))
        ask_file = False
    except IOError:
        input("File not found.")

game_grid = np.zeros(board.shape)
game_grid[np.where(board == False)] = DEAD
game_grid[np.where(board == True)] = ALIVE
grid_side = int(np.sqrt(game_grid.size))
grid_shape = (grid_side, grid_side)

def draw_grid(grid, generation):
    plt.figure(dpi = grid_side)
    image = np.zeros((grid_side, grid_side, 3))
    image[np.where(grid == DEAD)] = [0, 0, 0]
    image[np.where(grid == ALIVE)] = [1, 1, 1]
    plt.imshow(image)
    plt.title("Generation " + str(generation))
    plt.show()
    return image

# Draws generation 0
draw_grid(game_grid, current_generation)

def get_surrounding_alive(row, column, grid):
    """
    Returns the number of alive cells that surround [row, column].
    """
    if row == 0:
        left = grid_side - 1
    else:
        left = row - 1
    if column == 0:
        up = grid_side - 1
    else:
        up = column - 1
    right = (row + 1) % grid_side
    down = (column + 1) % grid_side
    surroundings = np.array([grid[left, up], grid[row, up], grid[right, up],
                             grid[left, column], grid[right, column],
                             grid[left, down], grid[row, down], grid[right, down]])
    return np.where(surroundings == ALIVE)[0].size

@lru_cache
def get_evolution(cell_state, surrounding_alive):
    if cell_state == DEAD:
        # BIRTH
        if surrounding_alive == 3:
            return ALIVE
    else:
        # SOLITUDE or SUPERPOPULATION
        if surrounding_alive < 2 or surrounding_alive > 3:
            return DEAD
    # No change
    return cell_state

def get_grid_evolution(grid):
    """
    Returns an array of ints which indicate the state to which each cell will evolve.
    This is needed because you cannot evolve cells as you iterate through the grid since that will
    affect what the next cells will detect.
    """
    grid_evolution = np.zeros(grid_shape)
    for row in range(grid_side):
        for column in range(grid_side):
            grid_evolution[row, column] = get_evolution(grid[row, column], get_surrounding_alive(row, column, grid))
    return grid_evolution

def evolve_grid(grid, generations = 1):
    for generation in range(generations):
        grid = get_grid_evolution(grid).copy()
    return grid

# Game loop
while True:
    try:
        game_grid = evolve_grid(game_grid, 1).copy()
        current_generation += 1
        draw_grid(game_grid, current_generation)
    except KeyboardInterrupt:
        plt.imsave("life_board.png", draw_grid(game_grid, current_generation))
        sys.exit()
