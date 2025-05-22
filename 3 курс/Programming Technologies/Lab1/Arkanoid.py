import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
FPS = 90

PADDLE_WIDTH = 330
PADDLE_HEIGHT = 35
PADDLE_SPEED = 15

BALL_RADIUS = 20
BALL_SPEED = 6
BALL_RECT = int(BALL_RADIUS * 2 ** 0.5)

BLOCK_WIDTH = 100
BLOCK_HEIGHT = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed
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

def draw_objects(paddle, ball, blocks):
    screen.fill((0, 0, 0))
    for block in blocks:
        pygame.draw.rect(screen, block.color, block.rect)
    pygame.draw.rect(screen, pygame.Color('darkorange'), paddle.rect)
    pygame.draw.circle(screen, pygame.Color('white'), ball.rect.center, BALL_RADIUS)

def main():
    paddle = Paddle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
    ball = Ball(rnd(BALL_RECT, WIDTH - BALL_RECT), HEIGHT // 2, BALL_RADIUS, BALL_SPEED)
    blocks = [Block(10 + 120 * i, 10 + 70 * j, BLOCK_WIDTH, BLOCK_HEIGHT, (rnd(30, 256), rnd(30, 256), rnd(30, 256))) for i in range(10) for j in range(4)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_objects(paddle, ball, blocks)
        ball.move()

        if ball.rect.centerx < BALL_RADIUS or ball.rect.centerx > WIDTH - BALL_RADIUS:
            ball.dx = -ball.dx

        if ball.rect.centery < BALL_RADIUS:
            ball.dy = -ball.dy

        if ball.rect.colliderect(paddle.rect) and ball.dy > 0:
            detect_collision(ball, paddle.rect)

        for block in blocks:
            if ball.rect.colliderect(block.rect):
                detect_collision(ball, block.rect)
                blocks.remove(block)
                break

        if ball.rect.bottom > HEIGHT or not blocks:
            if not blocks:
                print('ПОБЕДА!!!')
            else:
                print('КОНЕЦ ИГРЫ!')
            pygame.quit()
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
