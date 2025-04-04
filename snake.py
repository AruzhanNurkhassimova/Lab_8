import pygame
import random
import time

# Настройки окна
width, height = 600, 600
cell_size = 20

# Цвета
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)

# Инициализация
pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

high_level = 1

def place_food(snake):
    while True:
        x = random.randint(1, (width - cell_size*2) // cell_size) * cell_size
        y = random.randint(1, (height - cell_size*2) // cell_size) * cell_size
        if (x, y) not in snake:
            return (x, y)

def reset_game():
    snake = [(100, 100)]
    dx, dy = cell_size, 0
    food = place_food(snake)
    speed = 10
    score = 0
    level = 1
    return snake, dx, dy, food, speed, score, level

running = True
snake, dx, dy, food, speed, score, level = reset_game()

while running:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and dy == 0:
        dx, dy = 0, -cell_size
    if keys[pygame.K_DOWN] and dy == 0:
        dx, dy = 0, cell_size
    if keys[pygame.K_LEFT] and dx == 0:
        dx, dy = -cell_size, 0
    if keys[pygame.K_RIGHT] and dx == 0:
        dx, dy = cell_size, 0

    # Передвижение змейки
    head = (snake[0][0] + dx, snake[0][1] + dy)

    # Проверка на столкновение со стеной и самопересечение
    if (head[0] < cell_size or head[0] >= width - cell_size or
        head[1] < cell_size or head[1] >= height - cell_size or
        head in snake):
        win.fill(black)
        game_over_text = font.render("Game Over", True, red)
        win.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//2))
        pygame.display.update()
        time.sleep(3)
        if level > high_level:
            high_level = level
        snake, dx, dy, food, speed, score, level = reset_game()
        continue

    snake.insert(0, head)
    if head == food:
        score += 1
        if score % 4 == 0:
            level += 1
            speed += 2
        food = place_food(snake)
    else:
        snake.pop()

    # Отрисовка экрана
    win.fill(black)
    pygame.draw.rect(win, gray, (0, 0, width, height), cell_size)  # граница
    for segment in snake:
        pygame.draw.rect(win, green, (*segment, cell_size, cell_size))
    pygame.draw.rect(win, red, (*food, cell_size, cell_size))

    # Отображение очков и уровня
    score_text = font.render(f"Score: {score}  Level: {level}  High Level: {high_level}", True, white)
    win.blit(score_text, (30, 30))

    pygame.display.update()

pygame.quit()
