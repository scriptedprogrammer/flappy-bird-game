from threading import local
import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
GROUND_HEIGHT = 50
FPS = 35
BIRD_X = SCREEN_WIDTH // 4
BIRD_SIZE = SCREEN_HEIGHT // 20
PIPE_WIDTH = SCREEN_WIDTH // 15
GAP_SIZE = SCREEN_HEIGHT // 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images
bg_image = pygame.image.load('background.png')
ground_image = pygame.image.load('ground.png')
bird_image = pygame.image.load('bird.png')
pipe_image = pygame.image.load('pipe.png')  
start_image = pygame.image.load('start.png')

# Resize images
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH + 20, SCREEN_HEIGHT + 20))
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, GROUND_HEIGHT))
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, SCREEN_HEIGHT))
start_image = pygame.transform.scale(start_image, (100, 100))

# Flip the pipe image for the top-facing pipe
flipped_pipe_image = pygame.transform.flip(pipe_image, False, True)

# Create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Load sounds
jump_sound = pygame.mixer.Sound('jump.wav')
collision_sound = pygame.mixer.Sound('collision.wav')

# Functions
def draw_background():
    screen.blit(bg_image, (0, 0))

def draw_ground():
    screen.blit(ground_image, (0, SCREEN_HEIGHT - GROUND_HEIGHT + 20))

def draw_bird(bird_y):
    screen.blit(bird_image, (BIRD_X, bird_y))

def draw_pipes(pipe_x, top_pipe_height, bottom_pipe_height):
    screen.blit(pipe_image, (pipe_x, 0), (0, 0, PIPE_WIDTH, top_pipe_height))
    screen.blit(flipped_pipe_image, (pipe_x, SCREEN_HEIGHT - bottom_pipe_height))

def draw_score(score):
    score_text = font.render(f'Score: {score}', True, RED)
    screen.blit(score_text, (10, 10))

# Game loop
def game():
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    gravity = 1.5
    jump_strength = SCREEN_HEIGHT // 30
    restart_delay = 0

    pipe_x = SCREEN_WIDTH
    pipe_height = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - GAP_SIZE - 100)
    gap_top = pipe_height
    gap_bottom = SCREEN_HEIGHT - GROUND_HEIGHT - gap_top - GAP_SIZE

    score = 0

    game_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_active:
                bird_velocity = -jump_strength
                jump_sound.play()  # Play jump sound
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if SCREEN_WIDTH // 2 - 50 < x < SCREEN_WIDTH // 2 + 50 and \
                        SCREEN_HEIGHT // 2 - 50 < y < SCREEN_HEIGHT // 2 + 50 and not game_active:
                    game_active = True
                    bird_y = SCREEN_HEIGHT // 2  # Reset bird position
                    bird_velocity = 0  # Reset bird velocity
                    pipe_x = SCREEN_WIDTH  # Reset pipe position
                    score = 0
                    restart_delay = FPS * 1  # 1-second delay

        if game_active:
            # Update bird
            bird_velocity += gravity
            bird_y += bird_velocity

            # Update pipes
            pipe_x -= SCREEN_WIDTH // 100
            if pipe_x < -PIPE_WIDTH:
                pipe_x = SCREEN_WIDTH
                pipe_height = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - GAP_SIZE - 100)
                gap_top = pipe_height
                gap_bottom = SCREEN_HEIGHT - GROUND_HEIGHT - gap_top - GAP_SIZE
                score += 1
                 # Play jump sound

            # Check collisions with a slight overlap allowance
            if (pipe_x < BIRD_X + BIRD_SIZE - 5 < pipe_x + PIPE_WIDTH and
                    (bird_y < gap_top or bird_y + BIRD_SIZE > gap_top + GAP_SIZE+45)):
                game_active = False
                collision_sound.play()  # Play collision sound

            if bird_y > SCREEN_HEIGHT - GROUND_HEIGHT or bird_y < 0:
                game_active = False
                collision_sound.play()  # Play collision sound

            # Draw everything
            draw_background()
            draw_pipes(pipe_x, gap_top, gap_bottom)
            draw_ground()
            draw_bird(bird_y)
            draw_score(score)

        else:
            screen.blit(start_image, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()
        clock.tick(FPS)

        # Decrease restart delay
        restart_delay = max(0, restart_delay - 1)

# Run the game
game()
