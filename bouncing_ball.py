import sys
import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_SPEED = [5, 5]
PADDLE_SPEED = 7
MAX_LIVES = 3
FONT_SIZE = 30

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Game")
clock = pygame.time.Clock()

# Load and scale ball image
try:
    ball = pygame.image.load("ball_red.png")
    ball = pygame.transform.scale(ball, (int(ball.get_width() * 0.7), int(ball.get_height() * 0.7)))
except FileNotFoundError:
    ball = pygame.Surface((14, 14))
    ball.fill((255, 0, 0))
    pygame.draw.circle(ball, (255, 0, 0), (7, 7), 7)

ballrect = ball.get_rect(center=(WIDTH // 2, HEIGHT // 2))
speed = BALL_SPEED.copy()

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# Game variables
score = 0
lives = MAX_LIVES
game_over = False
font = pygame.font.Font(None, FONT_SIZE)

def reset_ball():
    ballrect.center = (WIDTH // 2, HEIGHT // 2)
    speed[0] = BALL_SPEED[0]
    speed[1] = BALL_SPEED[1]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                score = 0
                lives = MAX_LIVES
                game_over = False
                reset_ball()
            if event.key == pygame.K_q:
                sys.exit()

    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(PADDLE_SPEED, 0)

        # Ball movement
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > WIDTH:
            speed[0] = -speed[0]
        if ballrect.top < 0:
            speed[1] = -speed[1]
        if ballrect.bottom > HEIGHT:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                reset_ball()

        # Ball-paddle collision
        if ballrect.colliderect(paddle) and speed[1] > 0:
            speed[1] = -speed[1]
            score += 10
            speed[0] *= 1.05
            speed[1] *= 1.05

    # Draw
    screen.fill(BLACK)
    screen.blit(ball, ballrect)
    pygame.draw.rect(screen, WHITE, paddle)

    # HUD
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()