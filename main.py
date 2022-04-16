import pygame
from pygame.locals import *
import sys
from collections import deque
from itertools import islice
from random import randrange

# Initialize pygame
pygame.init()

BLOCK_LENGTH = 25

# In block units
WIDTH_IN_BLOCKS = 32
HEIGHT_IN_BLOCKS = 24

SCORE_SURFACE_OFFSET = 4

# Set up window
WINDOW_WIDTH = WIDTH_IN_BLOCKS * BLOCK_LENGTH
WINDOW_HEIGHT = (HEIGHT_IN_BLOCKS + SCORE_SURFACE_OFFSET) * BLOCK_LENGTH
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

score_surface = pygame.Surface((WINDOW_WIDTH, SCORE_SURFACE_OFFSET * BLOCK_LENGTH))
score_surface.fill('blue')
score_rect = score_surface.get_rect()
score_rect.x = 0
score_rect.y = 0

game_surface = pygame.Surface((WINDOW_WIDTH, HEIGHT_IN_BLOCKS * BLOCK_LENGTH))
game_rect = game_surface.get_rect()
game_rect.x = 0
game_rect.y = SCORE_SURFACE_OFFSET * BLOCK_LENGTH

# Change window title
pygame.display.set_caption("Snake")

# Clock to set framerate
clock = pygame.time.Clock()

# Direction constants (x, y)
UP_DIR = (0, -BLOCK_LENGTH)
DOWN_DIR = (0, BLOCK_LENGTH)
RIGHT_DIR = (BLOCK_LENGTH, 0)
LEFT_DIR = (-BLOCK_LENGTH, 0)

INITIAL_SNAKE_BODY_LENGTH = 5

apple = pygame.image.load("./apple.png").convert_alpha()
apple = pygame.transform.scale(apple, (BLOCK_LENGTH, BLOCK_LENGTH))

# Create a Rect for apple to detect collisions
apple_rect = apple.get_rect()
apple_rect.x = BLOCK_LENGTH
apple_rect.y = BLOCK_LENGTH

has_apple = True
game_over = False

def display_game_over():
    myfont = pygame.font.SysFont("monospace", 32)
    label = myfont.render("Game Over", 1, (255,0,0))
    game_surface.blit(label, (300, 300))

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dir = RIGHT_DIR

        # left-most item -> tail, right-most item -> head
        self.body = deque([
            pygame.rect.Rect((i * BLOCK_LENGTH, 0, BLOCK_LENGTH, BLOCK_LENGTH)) for i in range(INITIAL_SNAKE_BODY_LENGTH)
        ])

    def process_input(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP] and self.dir != DOWN_DIR:
            self.dir = UP_DIR
        if pressed_keys[K_DOWN] and self.dir != UP_DIR:
            self.dir = DOWN_DIR
         
        if pressed_keys[K_LEFT] and self.dir != RIGHT_DIR:
            self.dir = LEFT_DIR       
        if pressed_keys[K_RIGHT] and self.dir != LEFT_DIR:
            self.dir = RIGHT_DIR

    def update(self):
        # Remove tail
        popped_tail = self.body.popleft()

        # Get the new position of head
        new_head = self.body[-1].copy()
        new_head.move_ip(self.dir)

        # TODO: Do not let the snake travel on the score_surface
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
        
        # Check if head collides with body -> game over
        for sq in deque(islice(self.body, len(self.body) - 1)):
            if new_head.colliderect(sq):
                global game_over
                game_over = True

        # Check if head collides with apple
        global apple, has_apple
        if new_head.colliderect(apple_rect):
            # Append back the popped tail (basically increasing the length)
            self.body.appendleft(popped_tail)

            # Randomize new position of apple
            while True:
                repeat = False
                apple_rect.x = randrange(0, WIDTH_IN_BLOCKS) * BLOCK_LENGTH
                apple_rect.y = randrange(0, HEIGHT_IN_BLOCKS) * BLOCK_LENGTH

                # Check if apple collides with body
                for sq in deque(islice(self.body, len(self.body) - 1)):
                    if apple_rect.colliderect(sq):
                        repeat = True
                        break
                
                if not repeat:
                    break

        # Add head
        self.body.append(new_head)

    def draw(self):
        # Reset the window
        game_surface.fill('Black')

        if has_apple:
            game_surface.blit(apple, apple_rect)

        # Draw body
        for block in self.body:
            pygame.draw.rect(game_surface, 'White', block)
        
        window.blit(score_surface, score_rect)
        window.blit(game_surface, game_rect)

snake = Snake()

update_counter = 0
# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        display_game_over()
    else:
        # Process input takes 60 fps
        snake.process_input()
        update_counter += 1

        # Update and redraw take 10 fps (60 / 6)
        if update_counter == 6:
            snake.update()
            snake.draw()
            update_counter = 0

        # Set framerate
        clock.tick(60)

    # Update display
    pygame.display.update()
