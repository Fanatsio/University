import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60

# Paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15

# Ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)

# Block settings
block_width = 100
block_height = 50

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

        # Keep the paddle within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

class Ball:
    def __init__(self, x, y, radius, speed):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.speed = speed
        self.dx, self.dy = 1, -1

    def move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

class Block:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
img = pygame.image.load('1.jpg').convert()

paddle = Paddle(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h, paddle_speed)
ball = Ball(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_radius, ball_speed)
blocks = [Block(10 + 120 * i, 10 + 70 * j, block_width, block_height, (rnd(30, 256), rnd(30, 256), rnd(30, 256))) for i in range(10) for j in range(4)]

def detect_collision(ball, rect):
    if ball.dx > 0:
        delta_x = ball.rect.right - rect.left
    else:
        delta_x = rect.right - ball.rect.left
    if ball.dy > 0:
        delta_y = ball.rect.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.rect.top

    if abs(delta_x - delta_y) < 10:
        ball.dx, ball.dy = -ball.dx, -ball.dy
    elif delta_x > delta_y:
        ball.dy = -ball.dy
    elif delta_y > delta_x:
        ball.dx = -ball.dx

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(img, (0, 0))

    # Drawing world
    for block in blocks:
        pygame.draw.rect(screen, block.color, block.rect)

    pygame.draw.rect(screen, pygame.Color('darkorange'), paddle.rect)
    pygame.draw.circle(screen, pygame.Color('white'), ball.rect.center, ball_radius)

    # Ball movement
    ball.move()

    # Collision detection
    if ball.rect.centerx < ball_radius or ball.rect.centerx > WIDTH - ball_radius:
        ball.dx = -ball.dx

    if ball.rect.centery < ball_radius:
        ball.dy = -ball.dy

    if ball.rect.colliderect(paddle.rect) and ball.dy > 0:
        detect_collision(ball, paddle.rect)

    for block in blocks:
        if ball.rect.colliderect(block.rect):
            detect_collision(ball, block.rect)
            blocks.remove(block)
            break

    # Game over conditions
    if ball.rect.bottom > HEIGHT or not blocks:
        if not blocks:
            print('WIN!!!')
        else:
            print('GAME OVER!')
        running = False

    # Control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    # Update screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()