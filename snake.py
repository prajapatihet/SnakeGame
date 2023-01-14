import pygame
import random
import os
pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game By Het")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)
path = './hiscore.txt'
isExist = os.path.exists(path)
if not isExist:
    with open("hiscore.txt", "x") as f:
        f = open("hiscore.txt", "w")
        f.write("30")
        f.close()

def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

def plot_snake(gamewindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        screen_score("Welcome to My Game", black, 260, 250)
        screen_score("Press Space Bar to Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
        pygame.display.update()
        clock.tick(60)

def game_loop():
    exit_game = False
    game_over = False
    init_velocity = 5
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)
    score = 0
    snake_size = 20
    fps = 60
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            screen_score("Game Over! Press enter to continue", red, 120, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = +init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = +init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x) < 8 and abs(snake_y-food_y) < 8:
                score += 10
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snk_length += 3
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            screen_score("Score " + str(score) + "  Hi-Score " + str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)
            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()
game_loop()
