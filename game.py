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

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 50, 40
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

# Button dimensions
buttonNextGeneration_width, buttonNextGeneration_height = 200, 50
buttonNextGeneration_x, buttonNextGeneration_y = (width - buttonNextGeneration_width) // 20, height - buttonNextGeneration_height - 10

buttonStart_width, buttonStart_height = 200, 50
buttonStart_x, buttonStart_y = (width - buttonStart_width) // 20, height - buttonStart_height - 70

buttonPause_width, buttonPause_height = 200, 50
buttonPause_x, buttonPause_y = (width - buttonPause_width) // 20, height - buttonPause_height - 130

buttonSave_width, buttonSave_height = 200, 50
buttonSave_x, buttonSave_y = (width - buttonSave_width) // 20, height - buttonSave_height - 190

buttonLoad_width, buttonLoad_height = 200, 50
buttonLoad_x, buttonLoad_y = (width - buttonLoad_width) // 20, height - buttonLoad_height - 250


def draw_buttonNextGeneratrion():
    pygame.draw.rect(screen, green, (buttonNextGeneration_x, buttonNextGeneration_y, buttonNextGeneration_width, buttonNextGeneration_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Next Generation", True, black)
    text_rect = text.get_rect(center=(buttonNextGeneration_x + buttonNextGeneration_width // 2, buttonNextGeneration_y + buttonNextGeneration_height // 2))
    screen.blit(text, text_rect)
def draw_buttonStart():
    pygame.draw.rect(screen, green, (buttonStart_x, buttonStart_y, buttonStart_width, buttonStart_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, black)
    text_rect = text.get_rect(center=(buttonStart_x + buttonStart_width // 2, buttonStart_y + buttonStart_height // 2))
    screen.blit(text, text_rect)

def draw_buttonPause():
    pygame.draw.rect(screen, green, (buttonPause_x, buttonPause_y, buttonPause_width, buttonPause_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Pause", True, black)
    text_rect = text.get_rect(center=(buttonPause_x + buttonPause_width // 2, buttonPause_y + buttonPause_height // 2))
    screen.blit(text, text_rect)

def draw_buttonSave():
    pygame.draw.rect(screen, green, (buttonSave_x, buttonSave_y, buttonSave_width, buttonSave_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Save", True, black)
    text_rect = text.get_rect(center=(buttonSave_x + buttonSave_width // 2, buttonSave_y + buttonSave_height // 2))
    screen.blit(text, text_rect)

def draw_buttonLoad():
    pygame.draw.rect(screen, green, (buttonLoad_x, buttonLoad_y, buttonLoad_width, buttonLoad_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Load", True, black)
    text_rect = text.get_rect(center=(buttonLoad_x + buttonLoad_width // 2, buttonLoad_y + buttonLoad_height // 2))
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
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
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

running = True
while running:
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_buttonNextGeneratrion()
    draw_buttonStart()
    draw_buttonPause()
    draw_buttonSave()
    draw_buttonLoad()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttonNextGeneration_x <= event.pos[0] <= buttonNextGeneration_x + buttonNextGeneration_width and buttonNextGeneration_y <= event.pos[1] <= buttonNextGeneration_y + buttonNextGeneration_height:
                next_generation()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]

pygame.quit()



