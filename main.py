from lib2to3 import pygram
from tkinter import RIGHT
import pygame
from pygame.locals import *
import sys

# Initialize pygame
pygame.init()

# Set up window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Change window title
pygame.display.set_caption("Snake")

# Create colors
# my_color = pygame.Color(255, 255, 0)

# Drawing functions
# NOTE: coordinates starts from top-left corner, x -> horizontal (right), y -> vertical (down)
# pygame.draw.circle(WINDOW, my_color, (500, 200), 50)

# _RectValue -> (x, y, width, height)
# pygame.draw.rect(WINDOW, 'Blue', (200, 50, 100, 50))

# Start coordinate, end coordinate
# pygame.draw.line(WINDOW, 'White', (800, 0), (0, 600))

# Clock to set framerate
clock = pygame.time.Clock()


# Direction constants (x, y)
UP_DIR = (0, -5)
DOWN_DIR = (0, 5)
RIGHT_DIR = (5, 0)
LEFT_DIR = (-5, 0)

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect((0, 0, 25, 25))
        self.dir = RIGHT_DIR
        # self.length = 

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP] and self.dir != DOWN_DIR:
            self.dir = UP_DIR
        if pressed_keys[K_DOWN] and self.dir != UP_DIR:
            self.dir = DOWN_DIR
         
        if pressed_keys[K_LEFT] and self.dir != RIGHT_DIR:
            self.dir = LEFT_DIR       
        if pressed_keys[K_RIGHT] and self.dir != LEFT_DIR:
            self.dir = RIGHT_DIR

        self.rect.move_ip(self.dir)

        # Reset conditions
        # Too far up
        if self.rect.y < 0:
            self.rect.y = WINDOW_HEIGHT
        
        # Too far down
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = 0

        # Too far right
        if self.rect.x > WINDOW_WIDTH:
            self.rect.x = 0
        
        # Too far left
        if self.rect.x < 0:
            self.rect.x = WINDOW_WIDTH

    def draw(self):
        # Reset the window
        WINDOW.fill('Black')

        # Draw rectangle
        pygame.draw.rect(WINDOW, 'White', self.rect)

snake = Snake()

# Game Loop
while True:
    # Looking all events that is happening
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    snake.update()
    snake.draw()

    # Set framerate
    clock.tick(60)

    # Update display
    pygame.display.update()
