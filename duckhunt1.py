import pygame
from pygame.locals import *
from sys import exit
import os
import pickle
from random import randint

pygame.init()

pre = (0, 0, 0)
color = (0, 0, 0)
screen = pygame.display.set_mode((890, 550), 0, 32)
pygame.display.set_caption("Duck Hunt")

x_pos = 0
y_pos = 0

x_click = 0
y_click = 0

x_duck = 0
y_duck = randint(0, 450)

points = 0
velocity = 1
error = False
start_game = False
pause = False

pygame.mixer.init(44100, -16, 2, 1024)
pygame.mixer.music.set_volume(0.8)
game_font = pygame.font.SysFont("Times", 30)
score_font = pygame.font.SysFont("Times", 35, bold=True)

high_score_file = "highscore.dat"

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "rb") as file:
            return pickle.load(file)
    else:
        return 0

def save_high_score(score):
    with open(high_score_file, "wb") as file:
        pickle.dump(score, file)

high_score = load_high_score()

def game_over():
    global high_score
    pygame.mouse.set_visible(True)
    game_over_image = pygame.image.load("gameover.jpg")
    game_over_image = pygame.transform.scale(game_over_image, (890, 550))
    screen.blit(game_over_image, (0, 0))
    screen.blit(score_font.render("Points: " + str(points), True, color), (200, 460))
    screen.blit(score_font.render("High Score: " + str(high_score), True, color), (200, 500))

    dog_image = pygame.image.load("dog.gif")
    dog_rect = dog_image.get_rect()
    dog_rect.midbottom = (445, 100)
    screen.blit(dog_image, dog_rect)

    restart_font = pygame.font.SysFont("Courier New", 30)
    restart_text = restart_font.render("Play Again", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(600, 500))
    screen.blit(restart_text, restart_rect)

    border_rect = pygame.Rect(restart_rect.x - 1, restart_rect.y - 1, restart_rect.width + 2, restart_rect.height + 2)
    pygame.draw.rect(screen, (0, 0, 0), border_rect)

    pygame.draw.rect(screen, (0, 102, 51), restart_rect)
    screen.blit(restart_text, restart_rect)

    x_pos, y_pos = pygame.mouse.get_pos()
    if restart_rect.collidepoint(x_pos, y_pos):
        if pygame.mouse.get_pressed()[0]:
            restart_game()

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(x_pos, y_pos):
                restart_game()

def restart_game():
    global x_duck, y_duck, points, velocity, error
    x_duck = 0
    y_duck = randint(0, 450)
    points = 0
    velocity = 1
    error = False

def start_screen():
    global start_game

    background_image = pygame.image.load("bg.jpg")
    background_image = pygame.transform.scale(background_image, (890, 550))
    screen.blit(background_image, (0, 0))
    start_font = pygame.font.SysFont("Comic Sans MS", 50, bold=True)
    start_text = start_font.render("WELCOME TO DUCK HUNT", True, (0, 102, 159))
    text_rect = start_text.get_rect(center=(430, 195))
    screen.blit(start_text, text_rect)

    additional_font = pygame.font.SysFont("Courier New", 30)
    additional_text = additional_font.render("Play!", True, (10, 0, 225))
    additional_rect = additional_text.get_rect(center=(420, 270))

    pygame.draw.rect(screen, (51, 153, 225), (additional_rect.x - 15, additional_rect.y - 10, additional_rect.width + 25, additional_rect.height + 20))
    screen.blit(additional_text, additional_rect)

    x_pos, y_pos = pygame.mouse.get_pos()
    if additional_rect.collidepoint(x_pos, y_pos):
        pygame.draw.rect(screen, (0, 102, 159), (additional_rect.x - 15, additional_rect.y - 10, additional_rect.width + 25, additional_rect.height + 20), 2)

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if text_rect.collidepoint(x_pos, y_pos):
                start_game = True
            elif additional_rect.collidepoint(x_pos, y_pos):
                start_game = True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            save_high_score(high_score)
            exit()
        elif event.type == MOUSEMOTION:
            x_pos, y_pos = pygame.mouse.get_pos()
        elif event.type == MOUSEBUTTONDOWN:
            x_click, y_click = pygame.mouse.get_pos()
        elif event.type == KEYDOWN:
            if event.key == K_p:
                pause = not pause  # Toggle pause state
                pygame.time.delay(200)  # Delay to avoid unintentional toggles

    pos = (x_pos - 50, y_pos - 50)

    if pause:
        # Display a simple pause message
        pause_font = pygame.font.SysFont("Courier New", 50, bold=True)
        pause_text = pause_font.render("Game Paused", True, (255, 255, 255))
        screen.blit(pause_text, (300, 250))
    else:
        if not start_game:
            start_screen()
        elif not error:
            x_duck += 1

            if x_duck * velocity > 890 and not error:
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()

                if points > high_score:
                    high_score = points

                error = True

            pygame.mouse.set_visible(False)

            screen.blit(pygame.image.load("background.png"), (0, 0))
            screen.blit(game_font.render("Points: " + str(points), True, color), (600, 50))

            if int(x_click) in range(int(x_duck * velocity) - 30, int(x_duck * velocity) + 30) and \
                    int(y_click) in range(int(y_duck - 30), int(y_duck + 30)):
                pygame.mixer.music.load("hit.mp3")
                pygame.mixer.music.play()

                points += 1
                velocity += 0.25
                x_duck = 0
                y_duck = randint(50, 500)

            screen.blit(pygame.image.load("duck.gif"), (x_duck * velocity, y_duck))
            screen.blit(pygame.image.load("aim.gif").convert(), pos)
        else:
            game_over()

    pygame.display.update()