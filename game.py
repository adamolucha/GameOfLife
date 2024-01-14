# To create & start using python venv:
#       python -m venv venv
#       source venv/bin/activate

# Install specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic

# High-level logic
# 1. Create and init the simulation grid
# 2. Start the simulation with a tick interval of <n> seconds
# 3. At each tick:
#   3.1. Update the grid - loop over each element of the board
#   3.2. Render new generation

# General approach
# 1. Plan & write down the general workflow
#  1.1. Define Input&Output
#  1.2. Consider adding validation
# 2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
# 3. Define communication between the objects
# 4. List the patterns you could apply
# 5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
#    and combine them into a complete application
# 6. Refine if needed

# Deadline - 15th of December 2023
# Mail with:
# 1. short screen recording demonstrating the new features
# 2. Linked code
# 3. Short description of the changes. Which design patterns you used and how you applied them.

import pygame
import numpy as np
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 50, 40
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])
saved_game_state = game_state
# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
red = (255, 0, 0)


class Button:
    def __init__(self, width, height, x, y, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.name = name

    def is_clicked(self, mouse_pos_x, mouse_pos_y):
        return self.x <= mouse_pos_x <= self.x + self.width and self.y <= mouse_pos_y <= self.y + self.height


class ButtonFactory:
    @staticmethod
    def create_green_button(y_offset, name):
        return Button(200, 50, (width - 200) // 20, (height - 50) - y_offset, green, name)

    @staticmethod
    def create_red_button(y_offset, name):
        return Button(200, 50, (width - 200) // 20, (height - 50) - y_offset, red, name)


# Button dimensions
button_next_generation = ButtonFactory.create_green_button(70, "Next generation")
button_start = ButtonFactory.create_green_button(130, "Start")
button_pause = ButtonFactory.create_green_button(190, "Pause")
button_save = ButtonFactory.create_green_button(250, "Save")
button_load = ButtonFactory.create_green_button(310, "Load")
button_close = ButtonFactory.create_red_button(10, "close")


def draw_button(button):
    pygame.draw.rect(screen, button.color, (
        button.x, button.y, button.width, button.height))
    font = pygame.font.Font(None, 36)
    text = font.render(button.name, True, black)
    text_rect = text.get_rect(center=(button.x + button.width // 2,
                                      button.y + button.height // 2))
    screen.blit(text, text_rect)


def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)


def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state


def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)


clock = pygame.time.Clock()
running = True
game_running = False
next_gen_requested = False
next_gen_time = 0
pause = game_running


def draw():
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button(button_next_generation)
    draw_button(button_start)
    draw_button(button_pause)
    draw_button(button_save)
    draw_button(button_load)
    draw_button(button_close)
    pygame.display.flip()


def handle_events():
    global pause, next_gen_requested, game_running, next_gen_time, game_state, saved_game_state, running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if button_next_generation.is_clicked(mouse_x, mouse_y):
                next_gen_requested = True
                next_generation()
            if button_start.is_clicked(mouse_x, mouse_y):
                game_running = True
                pause = False
                next_gen_time = pygame.time.get_ticks()
            if button_pause.is_clicked(mouse_x, mouse_y):
                pause = True
            if button_save.is_clicked(mouse_x, mouse_y):
                saved_game_state = game_state
            if button_load.is_clicked(mouse_x, mouse_y):
                game_state = game_state
                game_state = saved_game_state
            if button_close.is_clicked(mouse_x, mouse_y):
                running = not running
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]


while running:
    draw()
    handle_events()

    if game_running and not pause:
        current_time = pygame.time.get_ticks()
        if next_gen_requested or current_time - next_gen_time >= 100:
            next_generation()
            next_gen_requested = False
            next_gen_time = current_time

    clock.tick(60)

pygame.quit()
