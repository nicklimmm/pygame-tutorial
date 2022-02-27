import pygame
from pygame.locals import *
import sys
from collections import deque

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

BLOCK_LENGTH = 25

# Direction constants (x, y)
UP_DIR = (0, -BLOCK_LENGTH)
DOWN_DIR = (0, BLOCK_LENGTH)
RIGHT_DIR = (BLOCK_LENGTH, 0)
LEFT_DIR = (-BLOCK_LENGTH, 0)

INITIAL_SNAKE_BODY_LENGTH = 25

apple = pygame.image.load("./apple.png").convert_alpha()
apple = pygame.transform.scale(apple, (BLOCK_LENGTH, BLOCK_LENGTH))
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dir = RIGHT_DIR

        # left-most item -> tail, right-most item -> head
        self.body = deque([
            pygame.rect.Rect((i * BLOCK_LENGTH, 0, BLOCK_LENGTH, BLOCK_LENGTH)) for i in range(INITIAL_SNAKE_BODY_LENGTH)
        ])


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

        # Remove tail
        self.body.popleft()

        # Get the new position of head
        new_head = self.body[-1].copy()
        new_head.move_ip(self.dir)

        # Reset conditions
        # Too far up
        if new_head.y < 0:
            new_head.y = WINDOW_HEIGHT
        
        # Too far down
        if new_head.y > WINDOW_HEIGHT:
            new_head.y = 0

        # Too far right
        if new_head.x > WINDOW_WIDTH:
            new_head.x = 0
        
        # Too far left
        if new_head.x < 0:
            new_head.x = WINDOW_WIDTH
        
        # Add head
        self.body.append(new_head)

    def draw(self):
        # Reset the window
        WINDOW.fill('Black')
        WINDOW.blit(apple, (0, 0))

        # Draw body
        for block in self.body:
            pygame.draw.rect(WINDOW, 'White', block)

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
    clock.tick(20)

    # Update display
    pygame.display.update()
